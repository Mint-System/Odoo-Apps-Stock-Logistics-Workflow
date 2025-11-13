import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def update_position(self):
        _logger.info("### update_position")
        for picking in self:
            moves = picking.move_ids.sorted("id")
            position = 1
            for move in moves:
                move.write({"position": position})
                position += 1

    def set_position(self):
        for picking in self:
            if not picking.origin:
                position = 0
                for move in picking.move_ids:
                    position += 1
                    # move.position = position
                    move.write({"position": position})
            else:
                position = 0
                for move in picking.move_ids:
                    if move.sale_line_id:
                        move.position = move.sale_line_id.position
                    elif move.purchase_line_id:
                        move.position = move.purchase_line_id.position

    @api.model
    def create(self, values):
        res = super().create(values)
        res.set_position()
        return res

    def write(self, values):
        res = super().write(values)
        self.set_position()
        return res
