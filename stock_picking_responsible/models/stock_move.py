from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        user_id = self.sale_line_id.order_id.user_id
        if user_id:
            vals.update({"user_id": user_id.id})
        return vals
