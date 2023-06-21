from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    position = fields.Integer('Pos', compute='_compute_get_position')

    def _compute_get_position(self):
        """Get position from sale, purchase or manufacturing order"""
        for move in self:
            if move.sale_line_id:
                move.position = move.sale_line_id.position
            elif move.purchase_line_id:
                move.position = move.purchase_line_id.position
            else:
                move.position = 0