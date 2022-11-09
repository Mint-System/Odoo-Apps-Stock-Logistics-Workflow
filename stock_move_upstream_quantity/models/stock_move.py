
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        for move in self:
            if move.quantity_done != move.product_uom_qty:
                move.move_orig_ids.write({'quantity_done': move.quantity_done})
        return super()._action_done(cancel_backorder)