from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        vals = super()._prepare_procurement_values(group_id=group_id)
        if self.name:
            vals["product_description_variants"] = self.name
        return vals