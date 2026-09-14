import logging
from datetime import timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CriticalForecast(models.Model):

    _inherit = "critical.forecast"

    def _compute_orderpoint_date(self, product_id, product_min_qty):
        """Find the first day within the next 90 days on which the
        forecasted quantity report predicts stock for product_id to drop
        below product_min_qty."""
        today = fields.Date.context_today(self)
        to_date = today + timedelta(days=90)
        forecast_report = self.env["report.stock.quantity"]._read_group(
            domain=[
                ("date", ">=", today),
                ("date", "<=", to_date),
                ("product_id", "=", product_id),
                ("company_id", "=", self.env.company.id),
                ("product_qty", "<", product_min_qty),
            ],
            groupby=["date:day"],
            order="date:day",
            limit=1,
        )
        return forecast_report[0][0] if forecast_report else False

    def _compute_critical_date(self, replenish_data, product=None):
        """Extend the base computation with the minimum stock rule.

        The base result (from open picking/MO demand) and the orderpoint
        result (from the minimum stock rule) are two independent signals;
        whichever gives the earlier date wins, since that's the one that
        needs action first.
        """
        critical_date = super()._compute_critical_date(replenish_data, product=product)
        _logger.warning(f"##### PRODUCT: {product.name}, critcial date from MO/PC: {critical_date}")

        if not product:
            # Nothing to check against an orderpoint without a known product.
            return critical_date

        orderpoint_id = self.env["stock.warehouse.orderpoint"].search(
            [("product_id", "=", product.id), ("product_min_qty", ">", 0.0)],
            limit=1,
        )
        _logger.warning(f"##### ORDERPOINT ID: {orderpoint_id}")
        if not orderpoint_id:
            return critical_date

        orderpoint_date = self._compute_orderpoint_date(product.id, orderpoint_id.product_min_qty)
        if orderpoint_date:
            _logger.info("Orderpoint date for %s: %s", product.display_name, orderpoint_date)

        if not orderpoint_date:
            return critical_date
        if not critical_date:
            return orderpoint_date
        return orderpoint_date if orderpoint_date < critical_date.date() else critical_date

    def _get_order_data(self, data=None, product_ids=None):
        """Add products driven purely by an active reordering rule (Odoo has
        already computed a quantity to order), even with no open picking/MO
        move at all.
        """
        if data is None:
            data = []
        if product_ids is None:
            product_ids = []

        orderpoint_ids = self.env["stock.warehouse.orderpoint"].search([("qty_to_order", ">", 0.0)])

        for orderpoint in orderpoint_ids.filtered(lambda o: o.product_id.id not in product_ids):
            replenish_data = self.env["stock.forecasted_product_product"]._get_report_data(
                product_ids=[orderpoint.product_id.id]
            )
            # `orderpoint` duck-types as `move` here: _prepare_report_line
            # only ever accesses `.product_id` on what it's given.
            data.append(self._prepare_report_line(orderpoint, replenish_data))
            product_ids.append(orderpoint.product_id.id)

        return data, product_ids

    @api.model
    def get_data(self):
        """Extend to also scan active reordering rules, not just open
        picking/MO moves."""
        current_ids = self.search([])
        current_product_ids = current_ids.mapped("product_id.id")

        data = []
        product_ids = []

        data, product_ids = self._get_production_data(data, product_ids)
        data, product_ids = self._get_picking_data(data, product_ids)
        data, product_ids = self._get_order_data(data, product_ids)

        self.create(list(filter(lambda d: d["product_id"] not in current_product_ids, data)))

        for curr in current_ids:
            vals = list(filter(lambda d: d["product_id"] == curr.product_id.id, data))
            if vals:
                curr.write(vals[0])

        self.search([("product_id", "not in", product_ids)]).unlink()

    def action_product_replenish(self):
        """Open product replenish view."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_orderpoint_replenish")
        action["domain"] = [("product_id", "=", self.product_id.id)]
        return action
