from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    lot_badges_html = fields.Html(
        string='Lots',
        compute='_compute_lot_badges_html',
        store=False,
        sanitize=False,
    )


    def _action_assign(self, force_qty=False):
        res = super()._action_assign(force_qty=force_qty)

        for move in self:
            if not move.picking_id.picking_type_id.pick_all_lot_qty:
                continue

            for line in move.move_line_ids:
                if not line.lot_id or line.product_id.tracking != 'lot':
                    continue

                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('lot_id', '=', line.lot_id.id),
                    ('location_id', '=', line.location_id.id),
                ])
                reserved = sum(quants.mapped('reserved_quantity'))
                lot_qty = line.lot_id.product_qty

                is_partial = 0 < reserved < lot_qty
                line.write({
                    'quantity': lot_qty,
                    'is_partial_lot': is_partial,
                })

        return res


    @api.depends('move_line_ids.lot_id', 'move_line_ids.is_partial_lot')
    def _compute_lot_badges_html(self):
        for move in self:
            parts = []
            for line in move.move_line_ids:
                if not line.lot_id:
                    continue
                name = line.lot_id.name
                if line.is_partial_lot:
                    parts.append(
                        f'<span class="badge text-bg-warning">{name}</span>'
                    )
                else:
                    parts.append(
                        f'<span class="badge text-bg-secondary">{name}</span>'
                    )
            move.lot_badges_html = ' '.join(parts) or ''