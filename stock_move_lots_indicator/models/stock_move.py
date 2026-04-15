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
                continue

            move_lines = move.move_line_ids

            if not move_lines:
                move.lot_generated_status = "-"
                continue

            all_assigned = True
            all_available = True

            _logger.warning(f"move_lines: {move_lines}")

            for line in move_lines:
                lot = line.lot_id
                _logger.warning(f"lot: {lot}")

                if not (line.lot_name or lot):
                    all_assigned = False
                    all_available = False
                    continue

                if lot:
                    # other_reserved = self.env['stock.move.line'].search([
                    #     ('product_id', '=', product.id),
                    #     ('lot_id', '=', lot.id),
                    #     ('id', 'not in', move_lines.ids),
                    #     ('state', 'in', ['assigned', 'partially_available']),
                    # ], limit=1)
                    other_reserved = self.env['stock.move.line'].search([
                        ('product_id', '=', product.id),
                        ('lot_id', '=', lot.id),
                        ('id', 'not in', move_lines.ids),
                        ('state', 'in', ['assigned', 'partially_available']),
                        ('location_id.usage', '=', 'internal'),
                        ('location_id', '=', line.location_id.id),
                    ], limit=1)
                    _logger.warning(f"other_reserved: {other_reserved}")

                    if other_reserved:
                        all_available = False

            if not all_assigned:
                move.lot_generated_status = "❌"
            elif not all_available:
                move.lot_generated_status = "⚠️"
            else:
                move.lot_generated_status = "✅"


