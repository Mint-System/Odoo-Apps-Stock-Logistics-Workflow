import logging
from datetime import timedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CriticalForecast(models.Model):
    _inherit = "critical.forecast"

    def _compute_orderpoint_date(self, product_id, product_min_qty):
        """
        Read data from the forecast report.
        Extract orderpoint date from read group result.
        """
        today = fields.Datetime.today()
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
            # aggregates=["date:sum"],
            order="date:day",
            limit=1,
        )

        orderpoint_date = False
        if forecast_report:
            orderpoint_date = forecast_report[0][0]
        return orderpoint_date

    def _compute_critical_date(self, replenish_data):
        """
        Compute critical date based on orderpoint and forecast report.
        """
        critical_date = super()._compute_critical_date(replenish_data)

        product_id = replenish_data["product_templates"][0].get("id")
        product_tmpl = self.env["product.template"].search([("id", "=", product_id)])
        product_var = product_tmpl.product_variant_id
        orderpoint_id = self.env["stock.warehouse.orderpoint"].search(
            [("product_id", "=", product_var.id), ("product_min_qty", ">", 0.0)],
            limit=1,
        )
        if orderpoint_id:
            _logger.warning(f"product {product_var.name} has orderpoint")
            orderpoint_date = self._compute_orderpoint_date(product_var.id, orderpoint_id.product_min_qty)
            if not orderpoint_date and not critical_date:
                return False
            elif orderpoint_date and not critical_date:
                if orderpoint_date:
                    _logger.warning(f"orderpoint date: {orderpoint_date}")
                return orderpoint_date
            elif orderpoint_date and orderpoint_date < critical_date.date():
                if orderpoint_date:
                    _logger.warning(f"orderpoint date: {orderpoint_date}")
                return orderpoint_date
            else:
                if critical_date:
                    _logger.warning(f"critical date: {critical_date}")
                return critical_date
        else:
            if critical_date:
                _logger.warning(f"critical date: {critical_date}")
            return critical_date or False

    def _get_order_data(self, data=[], product_ids=[]):
        """Add products with active orderpoint to data list."""

        # Lookup orderpoints with reorder filter
        orderpoint_ids = self.env["stock.warehouse.orderpoint"].search([("qty_to_order", ">", 0.0)])

        for orderpoint in orderpoint_ids.filtered(lambda o: o.product_id.id not in product_ids):
            replenish_data = self.env["report.stock.report_product_product_replenishment"]._get_report_data(
                [orderpoint.product_tmpl_id.id]
            )
            data.append(self._prepare_report_line(orderpoint.product_id, replenish_data))
            product_ids.append(orderpoint.product_id.id)

        return data, product_ids

    def action_product_replenish(self):
        """Open product replenish view."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_orderpoint_replenish")
        action["domain"] = [("product_id", "=", self.product_id.id)]
        return action
