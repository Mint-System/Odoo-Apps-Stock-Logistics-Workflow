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


    @api.depends('move_line_ids', 'move_line_ids.lot_name', 'move_line_ids.lot_id')
    def _compute_lot_generated_status(self):
        for move in self:
            product = move.product_id
            if product.tracking == "none":
                move.lot_generated_status = "-"
            else:
                _logger.warning(f"product: {product}")
                move_lines = move.move_line_ids
                for line in move_lines:
                    _logger(f"lot name: {line.lot_name}, lot id: {line.lot_id}")
                if not move_lines:
                    move.lot_generated_status = "-"
                elif all(line.lot_name or line.lot_id for line in move_lines):
                    move.lot_generated_status = "✅"
                else:
                    move.lot_generated_status = "❌"
