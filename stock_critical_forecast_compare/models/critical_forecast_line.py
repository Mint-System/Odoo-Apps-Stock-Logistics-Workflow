import logging
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.tools.misc import get_lang

_logger = logging.getLogger(__name__)


class CriticalForecastLine(models.Model):
    """Standalone re-implementation, for comparison against another module.

    Deliberate design choices, each addressing a specific issue found while
    debugging the other implementation:

    1. Products are collected once per *product*, not once per *move*. A
       product referenced by several open moves (pickings or MOs) is only
       looked up once in the forecast report, instead of being re-fetched
       and re-appended for every move that references it.

    2. The forecast report is always queried with ``product_ids`` (variant
       level), never ``product_template_ids``. Passing a template id makes
       the report aggregate every variant of that template into one
       ``lines`` list, which can attribute another variant's late/unfilled
       line to the wrong product. Since this is meant to report on one
       specific product.product, it is always scoped that way.

    3. A record is only created/kept for a product if a critical date was
       actually found. The other implementation appended a line
       unconditionally (even when ``critical_date`` was ``None``), so every
       product with any open picking/MO move ended up with a
       "critical forecast" record regardless of whether it was actually
       critical.

    4. Cleanup (unlink) is based on "no longer critical", not "no longer
       has an open move". A product that stops being critical while still
       having an open picking/MO would never have been cleaned up by the
       other implementation's unlink domain.

    5. The critical date is the *earliest* problematic line's date, not
       whichever line happens to be first in the (unsorted) list.
    """

    _name = "critical.forecast.line"
    _description = "Critical Forecast Line (comparison implementation)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product", required=True, index=True)
    product_type = fields.Selection(related="product_id.type")
    critical_date = fields.Datetime()
    action_date = fields.Datetime()
    replenish_delay = fields.Integer()
    qty_available = fields.Float(digits="Product Unit of Measure")
    virtual_available = fields.Float(digits="Product Unit of Measure")
    qty_in = fields.Float(digits="Product Unit of Measure")
    qty_out = fields.Float(digits="Product Unit of Measure")
    min_qty = fields.Integer()
    product_min_qty = fields.Integer()
    route_id = fields.Many2one("stock.route")
    seller_id = fields.Many2one("res.partner")
    source = fields.Selection([("picking", "Delivery"), ("production", "Manufacturing")])
    trigger_document = fields.Char(
        help="Reference of the first open document encountered that surfaced this product. "
        "Kept for debugging only; a product can be driven by several documents."
    )
    problematic_line_count = fields.Integer()

    _sql_constraints = [
        ("product_uniq", "unique(product_id)", "Only one critical forecast line per product."),
    ]

    # ---------------------------------------------------------------
    # Collection of candidate products
    # ---------------------------------------------------------------

    def _get_candidate_products(self):
        """Return {product.product: (source, trigger_document_str)} for every
        product appearing on an open outgoing delivery move or an unfinished
        MO raw-material move. Only the first document encountered per
        product is kept as a reference; the actual criticality computation
        below looks at the product's full forecast, not just this one move.
        """
        candidates = {}  # product.product record -> (source, trigger_document)

        pickings = self.env["stock.picking"].search([
            ("state", "not in", ("cancel", "draft", "done")),
            ("picking_type_id.code", "=", "outgoing"),
            ("company_id", "=", self.env.company.id),
        ])
        picking_moves = pickings.move_ids.filtered(
            lambda m: m.product_id and m.state not in ("cancel", "done")
        )
        for move in picking_moves:
            candidates.setdefault(move.product_id, ("picking", move.picking_id.display_name))

        productions = self.env["mrp.production"].search([
            ("state", "in", ("confirmed", "progress", "to_close")),
            ("company_id", "=", self.env.company.id),
        ])
        production_moves = productions.move_raw_ids.filtered(
            lambda m: m.product_id and m.state not in ("cancel", "done")
        )
        for move in production_moves:
            candidates.setdefault(
                move.product_id, ("production", move.raw_material_production_id.display_name)
            )

        return candidates

    # ---------------------------------------------------------------
    # Forecast lookup / critical date computation
    # ---------------------------------------------------------------

    def _get_replenish_data(self, product):
        """Fetch forecast report data scoped strictly to this one variant."""
        warehouse_id = self.env["stock.warehouse"]._get_warehouse_id_from_context() \
            or self.env["stock.warehouse"].search([("active", "=", True)], limit=1).id
        return self.env["stock.forecasted_product_product"].with_context(
            warehouse=warehouse_id
        )._get_report_data(product_ids=[product.id])

    def _compute_critical_date(self, replenish_data):
        """Return (earliest_critical_date_or_None, problematic_lines)."""
        problematic_lines = [
            line for line in replenish_data.get("lines", [])
            if not line["replenishment_filled"] or line["is_late"]
        ]
        if not problematic_lines:
            return None, []

        lang = get_lang(self.env)
        date_time_format = lang.date_format + " " + lang.time_format
        parsed_dates = []
        for line in problematic_lines:
            raw_date = line.get("delivery_date") or line.get("receipt_date")
            if not raw_date:
                continue
            parsed = self._parse_report_date(raw_date, date_time_format, lang.date_format)
            if parsed:
                parsed_dates.append(parsed)

        if not parsed_dates:
            # Lines were flagged problematic but had no parseable date at all.
            _logger.warning(
                "Product with %d problematic line(s) but no parseable date: %s",
                len(problematic_lines), problematic_lines,
            )
            return None, problematic_lines

        return min(parsed_dates), problematic_lines

    @staticmethod
    def _parse_report_date(raw_date, date_time_format, date_format):
        try:
            return datetime.strptime(raw_date, date_time_format)
        except ValueError:
            pass
        try:
            return datetime.strptime(raw_date, date_format)
        except ValueError:
            _logger.warning("Could not parse report date %r", raw_date)
            return None

    def _compute_replenish_delay(self, product):
        if product.seller_ids:
            return product.seller_ids[0].delay
        if product.bom_ids:
            return product.bom_ids[0].produce_delay
        return 0

    def _prepare_vals(self, product, source, trigger_document, replenish_data, critical_date, problematic_lines):
        replenish_delay = self._compute_replenish_delay(product)
        return {
            "product_id": product.id,
            "critical_date": critical_date,
            "action_date": critical_date - timedelta(days=replenish_delay) if critical_date else None,
            "replenish_delay": replenish_delay,
            "qty_available": product.qty_available,
            "virtual_available": product.virtual_available,
            "min_qty": product.seller_ids[0].min_qty if product.seller_ids else 0,
            "product_min_qty": product.orderpoint_ids[0].product_min_qty if product.orderpoint_ids else 0,
            "qty_in": replenish_data.get("qty", {}).get("in", 0.0),
            "qty_out": replenish_data.get("qty", {}).get("out", 0.0),
            "route_id": product.route_ids[0].id if product.route_ids else False,
            "seller_id": product.seller_ids[0].partner_id.id if product.seller_ids else False,
            "source": source,
            "trigger_document": trigger_document,
            "problematic_line_count": len(problematic_lines),
        }

    # ---------------------------------------------------------------
    # Entry point
    # ---------------------------------------------------------------

    @api.model
    def get_data(self):
        candidates = self._get_candidate_products()
        critical_vals = []

        for product, (source, trigger_document) in candidates.items():
            replenish_data = self._get_replenish_data(product)
            critical_date, problematic_lines = self._compute_critical_date(replenish_data)
            if not critical_date:
                continue  # not actually critical: don't create/keep a record for it
            vals = self._prepare_vals(
                product, source, trigger_document, replenish_data, critical_date, problematic_lines
            )
            critical_vals.append(vals)
            _logger.info(
                "critical.forecast.line: product_id=%s (%s) critical_date=%s problematic_lines=%d source=%s",
                product.id, product.display_name, critical_date, len(problematic_lines), source,
            )

        critical_product_ids = {v["product_id"] for v in critical_vals}
        existing = self.search([])
        existing_by_product = {rec.product_id.id: rec for rec in existing}

        created = self.env["critical.forecast.line"]
        for vals in critical_vals:
            rec = existing_by_product.get(vals["product_id"])
            if rec:
                rec.write(vals)
            else:
                created |= self.create(vals)

        stale = existing.filtered(lambda r: r.product_id.id not in critical_product_ids)
        stale.unlink()

        _logger.info(
            "critical.forecast.line.get_data(): %d candidates scanned, %d critical, %d created, %d unlinked",
            len(candidates), len(critical_vals), len(created), len(stale),
        )
        return critical_vals

    def action_product_forecast_report(self):
        """Open product forecast report"""
        self.ensure_one()
        action = self.product_id.action_product_forecast_report()
        action["context"] = {
            "active_id": self.product_id.id,
            "active_ids": [self.product_id.id],
            "default_product_id": self.product_id.id,
            "active_model": "product.product",
        }
        return action

    def calculate(self):
        action = self.sudo().env.ref("stock_critical_forecast.calculate_action")
        action.method_direct_trigger()
        # threaded_calculation = threading.Thread(target=self.get_data, args=())
        # threaded_calculation.start()
        return {"type": "ir.actions.client", "tag": "reload"}