import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)


class CriticalForecast(models.Model):
    _inherit = 'critical.forecast'

    def _compute_critical_date(self, product_id, replenish_data):
        """Check if active orderpoint for this product exists."""
        res = super()._compute_critical_date(product_id, replenish_data)
        if not res:
            oderpoint_id = self.env['stock.warehouse.orderpoint'].search([
                ('product_id', '=', product_id.id),
                ('qty_to_order', '>', 0.0)
            ], limit=1)
            if oderpoint_id:
                return oderpoint_id.lead_days_date
        return res

    def _get_order_data(self, data=[], product_ids=[]):
        """Add products with active orderopint to data list.""" 

        # Lookup orderpoints with reorder filter
        oderpoint_ids = self.env['stock.warehouse.orderpoint'].search([('qty_to_order', '>', 0.0)])

        for orderpoint in oderpoint_ids.filtered(lambda o: o.product_id.id not in product_ids):
            replenish_data = self.env['report.stock.report_product_product_replenishment']._get_report_data([orderpoint.product_tmpl_id.id])
            data.append(self._prepare_report_line(orderpoint.product_id, replenish_data))
            product_ids.append(orderpoint.product_id.id)

        return data, product_ids

    def action_product_replenish(self):
        """Open product replenish view."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id('stock.action_orderpoint_replenish')
        action['domain'] = [('product_id', '=', self.product_id.id)]
        return action