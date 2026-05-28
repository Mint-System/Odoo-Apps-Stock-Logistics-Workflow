from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    has_partial_lot = fields.Boolean(
        compute='_compute_lot_display', store=True,
    )
    lot_badges_html = fields.Html(
        compute='_compute_lot_display', store=False, sanitize=False,
    )


    @api.depends(
        'move_line_ids.lot_id',
        'picking_id.picking_type_id.pick_all_lot_qty',
    )
    def _compute_lot_display(self):
        for move in self:
            pick_all = move.picking_id.picking_type_id.pick_all_lot_qty
            parts = []

            for line in move.move_line_ids:
                if not line.lot_id:
                    continue
                name = line.lot_id.name
                parts.append(
                        f'<span class="badge text-bg-warning">{name}</span>'
                    )


            move.lot_badges_html = ' '.join(parts) or ''
        

    def _action_done(self, cancel_backorder=False):
        for move in self:
            if not move.picking_id.picking_type_id.pick_all_lot_qty:
                continue
            for line in move.move_line_ids:
                if not line.lot_id or line.product_id.tracking != 'lot':
                    continue
                line.quantity = line.lot_id.product_qty
        return super()._action_done(cancel_backorder)





    


