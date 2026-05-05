from odoo import api, models
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_assign(self, force_qty=False):
        """
        override each line's quantity with the lot's total product_qty
        """
        res = super()._action_assign(force_qty=force_qty)

        for move in self:
            for line in move.move_line_ids:
                if line.lot_id and line.product_id.tracking == 'lot':
                    new_qty = line.lot_id.product_qty
                    if new_qty > 0:
                        line.quantity = new_qty

        return res