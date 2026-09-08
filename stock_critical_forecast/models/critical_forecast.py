import logging
import pprint

from odoo import api, fields, models

_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta

from odoo.tools.misc import get_lang

# import threading


class CriticalForecast(models.Model):
    _name = "critical.forecast"
    _description = "Critical Forecast"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "product_id"

    product_id = fields.Many2one("product.product", "Product")
    action_date = fields.Date()
    critical_date = fields.Date()
    product_type = fields.Selection(related="product_id.type")
    qty_available = fields.Float(digits="Product Unit of Measure")
    virtual_available = fields.Float(digits="Product Unit of Measure")
    replenish_delay = fields.Integer()
    min_qty = fields.Integer()
    product_min_qty = fields.Integer()
    qty_in = fields.Float(digits="Product Unit of Measure")
    qty_out = fields.Float(digits="Product Unit of Measure")
    route_id = fields.Many2one("stock.route", "Route")
    seller_id = fields.Many2one("res.partner", "Vendor")





    def log_replenish_data_if_matched(self, replenish_data, target_product_id, use_template_id=False):
        """Log replenish/forecast data only if target_product_id matches this entry.

        :param replenish_data: dict as returned per-product by the replenishment report
                                (contains 'product_templates_ids' / 'product_variants_ids')
        :param target_product_id: int, the product.product (variant) id to match
                                   (or product.template id if use_template_id=True)
        :param use_template_id: match against product_templates_ids instead of variants
        """
        id_list = (
            replenish_data.get('product_templates_ids', [])
            if use_template_id
            else replenish_data.get('product_variants_ids', [])
        )

        if target_product_id not in id_list:
            return False

        display_name = (
            replenish_data.get('product_templates', [{}])[0].get('display_name')
            if replenish_data.get('product_templates')
            else 'Unknown'
        )

        _logger.info(
            "Replenish data matched for product_id=%s (%s):\n%s",
            target_product_id,
            display_name,
            pprint.pformat(replenish_data, width=120),
        )
        return True


    def _compute_critical_date(self, replenish_data):
        TARGET_PRODUCT_ID = 23183
        # TARGET_PRODUCT_ID = 27
        match = self.log_replenish_data_if_matched(replenish_data, TARGET_PRODUCT_ID, use_template_id=False)
        
        problematic_lines = list(
            filter(
                lambda l: not l["replenishment_filled"] or l["is_late"],
                replenish_data["lines"],
            )
        )
        if not problematic_lines:
            return None
        
        if match:
            _logger.warning(f"########  problematic_lines: {problematic_lines}")
        lang = get_lang(self.env)
        date_time_format = lang.date_format + " " + lang.time_format
        delivery_date = problematic_lines[0]["delivery_date"]
        try:
            delivery_date = datetime.strptime(delivery_date, date_time_format)
        except:
            delivery_date = datetime.strptime(delivery_date, lang.date_format)
        return delivery_date

    def _compute_replenish_delay(self, move):
        if move.product_id.seller_ids:
            return move.product_id.seller_ids[0].delay
        elif move.product_id.bom_ids:
            return move.product_id.bom_ids[0].produce_delay
        else:
            return 0

    def _prepare_report_line(self, move, replenish_data):
        replenish_delay = self._compute_replenish_delay(move)
        critical_date = self._compute_critical_date(replenish_data)
        return {
            "product_id": move.product_id.id,
            "critical_date": critical_date,
            "action_date": critical_date - timedelta(days=replenish_delay) if critical_date else None,
            "replenish_delay": replenish_delay,
            "qty_available": move.product_id.qty_available,
            "virtual_available": move.product_id.virtual_available,
            "min_qty": move.product_id.seller_ids[0].min_qty if move.product_id.seller_ids else 0,
            "product_min_qty": move.product_id.orderpoint_ids[0].product_min_qty
            if move.product_id.orderpoint_ids
            else 0,
            "qty_in": replenish_data["qty"]["in"],
            "qty_out": replenish_data["qty"]["out"],
            "route_id": move.product_id.route_ids[0].id if move.product_id.route_ids else False,
            "seller_id": move.product_id.seller_ids[0].partner_id.id if move.product_id.seller_ids else False,
        }

    def _get_picking_data(self, data=[], product_ids=[]):
        """Get data delivery orders"""

        # Clear cache
        self.env["stock.picking"].clear_caches()

        # Lookup unfinished outgoing delivery ordrers
        picking_ids = self.env["stock.picking"].search(
            [
                ("state", "not in", ("cancel", "draft", "done")),
                ("picking_type_id.code", "=", "outgoing"),
                ("company_id", "=", self.env.company.id),
            ]
        )

        for picking in picking_ids:
            for move in picking.move_ids.filtered(lambda m: m.product_id.id not in product_ids):
                replenish_data = self.env["stock.forecasted_product_product"]._get_report_data(
                    [move.product_tmpl_id.id]
                )
                data.append(self._prepare_report_line(move, replenish_data))
                product_ids.append(move.product_id.id)

        return data, product_ids

    def _get_production_data(self, data=[], product_ids=[]):
        """Get data for manufacturing orders"""

        # Lookup unfinished manufacturing orders
        production_ids = self.env["mrp.production"].search(
            [
                ("state", "in", ["confirmed", "progress", "to_close"]),
                ("company_id", "=", self.env.company.id),
            ]
        )

        for mo in production_ids:
            for move in mo.move_raw_ids.filtered(lambda m: m.product_id.id not in product_ids):
                replenish_data = self.env["stock.forecasted_product_product"]._get_report_data(
                    [move.product_tmpl_id.id]
                )
                data.append(self._prepare_report_line(move, replenish_data))
                product_ids.append(move.product_id.id)

        return data, product_ids

    @api.model
    def get_data(self):
        """Generate critical forecast data"""

        # Get current data
        current_ids = self.search([])
        current_product_ids = current_ids.mapped("product_id.id")

        # Reset data
        data = []
        product_ids = []

        # Get manufacturing order data
        data, product_ids = self._get_production_data(data, product_ids)

        # Get delivery order data
        data, product_ids = self._get_picking_data(data, product_ids)

        # Create entries
        self.create(list(filter(lambda d: d["product_id"] not in current_product_ids, data)))

        # Update entries
        for curr in current_ids:
            vals = list(filter(lambda d: d["product_id"] == curr.product_id.id, data))
            if vals:
                curr.write(vals[0])

        # Unlink entries
        self.search([("product_id", "not in", product_ids)]).unlink()

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
