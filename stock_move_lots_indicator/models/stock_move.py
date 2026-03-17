import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    lot_generated_status = fields.Char(
        string="Lots/SN erfasst",
        compute='_compute_lot_generated_status',
        store=False,
        readonly=True
    )


    @api.depends('move_line_ids', 'move_line_ids.lot_name')
    def _compute_lot_generated_status(self):
        for move in self:
            move_lines = move.move_line_ids
            if not move_lines:
                move.lot_generated_status = "⚠️"
            elif all(line.lot_name for line in move_lines):
                move.lot_generated_status = "✅"
            else:
                move.lot_generated_status = "❌"
