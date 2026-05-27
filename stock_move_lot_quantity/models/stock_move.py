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

    # lot_badges_html = fields.Html(
    #     string='Lots',
    #     compute='_compute_lot_badges_html',
    #     store=False,
    #     sanitize=False,
    # )

    pick_quantity = fields.Float(
        string='Will Pick',
        compute='_compute_lot_display',
        digits='Product Unit of Measure',
        help='Total quantity that will physically be picked across all lots '
             'when the transfer is validated.',
    )


    @api.depends(
        'move_line_ids.lot_id',
        'move_line_ids.is_partial_lot',
        'move_line_ids.quantity',
        'move_line_ids.lot_id.product_qty',
        'picking_id.picking_type_id.pick_all_lot_qty',
    )
    def _compute_lot_display(self):
        for move in self:
            pick_all = move.picking_id.picking_type_id.pick_all_lot_qty
            parts = []
            total_pick_qty = 0.0

            for line in move.move_line_ids:
                if not line.lot_id:
                    continue
                name = line.lot_id.name
                # lot_qty = line.lot_id.product_qty
                # line_pick_qty = lot_qty if pick_all else line.quantity
                # total_pick_qty += line_pick_qty

                # if pick_all and line_pick_qty > line.quantity:
                #     parts.append(
                #         f'<span class="badge text-bg-warning" '
                #         f'title="Will pick {int(line_pick_qty)}, reserved {int(line.quantity)}">'
                #         f'{name} ({int(line_pick_qty)})</span>'
                #     )
                # elif line.is_partial_lot:
                #     parts.append(
                #         f'<span class="badge text-bg-warning">{name}</span>'
                #     )
                # else:
                #     parts.append(
                #         f'<span class="badge text-bg-secondary">{name}</span>'
                #     )
                parts.append(
                        f'<span class="badge text-bg-warning">{name}</span>'
                    )


            move.lot_badges_html = ' '.join(parts) or ''
            # move.pick_quantity = total_pick_qty
            # move.has_partial_lot = any(
            #     line.is_partial_lot for line in move.move_line_ids
            # )


    

    # def _action_assign(self, force_qty=False):
    #     res = super()._action_assign(force_qty=force_qty)
    #     for move in self:
    #         if not move.picking_id.picking_type_id.pick_all_lot_qty:
    #             continue
    #         for line in move.move_line_ids:
    #             if not line.lot_id or line.product_id.tracking != 'lot':
    #                 continue
    #             # Use line.quantity = what THIS move reserved from this lot
    #             # NOT quant.reserved_quantity which includes other moves too
    #             this_move_reserved = line.quantity
    #             lot_qty = line.lot_id.product_qty
    #             line.is_partial_lot = 0 < this_move_reserved < lot_qty
    #     return res

    def _action_done(self, cancel_backorder=False):
        for move in self:
            if not move.picking_id.picking_type_id.pick_all_lot_qty:
                continue
            for line in move.move_line_ids:
                if not line.lot_id or line.product_id.tracking != 'lot':
                    continue
                line.quantity = line.lot_id.product_qty
        return super()._action_done(cancel_backorder)





    # @api.depends(
    #     'move_line_ids.lot_id',
    #     'move_line_ids.is_partial_lot',
    #     'move_line_ids.quantity',
    #     'move_line_ids.lot_id.product_qty',
    #     'picking_id.picking_type_id.pick_all_lot_qty',
    # )
    # def _compute_lot_display(self):
    #     for move in self:
    #         pick_all = move.picking_id.picking_type_id.pick_all_lot_qty
    #         parts = []
    #         total_pick_qty = 0.0

    #         for line in move.move_line_ids:
    #             if not line.lot_id:
    #                 continue
    #             name = line.lot_id.name
    #             lot_qty = line.lot_id.product_qty
    #             reserved = line.quantity

    #             if pick_all:
    #                 # Full lot only if this move reserved the entire lot
    #                 # Partial → only pick what this move reserved
    #                 line_pick_qty = reserved if line.is_partial_lot else lot_qty
    #             else:
    #                 line_pick_qty = reserved

    #             total_pick_qty += line_pick_qty

    #             if pick_all and line_pick_qty > reserved:
    #                 # Worker picks more than reserved → orange badge with qty
    #                 parts.append(
    #                     f'<span class="badge text-bg-warning" '
    #                     f'title="Will pick {int(line_pick_qty)}, '
    #                     f'reserved {int(reserved)}">'
    #                     f'{name} ({int(line_pick_qty)})</span>'
    #                 )
    #             elif line.is_partial_lot:
    #                 # Partial lot — orange badge, pick only reserved
    #                 parts.append(
    #                     f'<span class="badge text-bg-warning">{name}</span>'
    #                 )
    #             else:
    #                 parts.append(
    #                     f'<span class="badge text-bg-secondary">{name}</span>'
    #                 )

    #         move.lot_badges_html = ' '.join(parts) or ''
    #         move.pick_quantity = total_pick_qty
    #         move.has_partial_lot = any(
    #             line.is_partial_lot for line in move.move_line_ids
    #         )

    # def _action_assign(self, force_qty=False):
    #     res = super()._action_assign(force_qty=force_qty)
    #     for move in self:
    #         if not move.picking_id.picking_type_id.pick_all_lot_qty:
    #             continue
    #         for line in move.move_line_ids:
    #             if not line.lot_id or line.product_id.tracking != 'lot':
    #                 continue
    #             # line.quantity = what THIS move reserved from this lot
    #             # (not quant.reserved_quantity which sums across all moves)
    #             this_move_reserved = line.quantity
    #             lot_qty = line.lot_id.product_qty
    #             line.is_partial_lot = 0 < this_move_reserved < lot_qty
    #     return res

    # def _action_done(self, cancel_backorder=False):
    #     for move in self:
    #         if not move.picking_id.picking_type_id.pick_all_lot_qty:
    #             continue
    #         for line in move.move_line_ids:
    #             if not line.lot_id or line.product_id.tracking != 'lot':
    #                 continue
    #             # Only take full lot if this move had the entire lot reserved
    #             # Partial lot → keep reserved qty as done qty
    #             if not line.is_partial_lot:
    #                 line.quantity = line.lot_id.product_qty
    #     return super()._action_done(cancel_backorder)


    # old code



    # @api.depends('move_line_ids.lot_id', 'move_line_ids.is_partial_lot')
    # def _compute_lot_badges_html(self):
    #     for move in self:
    #         parts = []
    #         for line in move.move_line_ids:
    #             if not line.lot_id:
    #                 continue
    #             name = line.lot_id.name
    #             if line.is_partial_lot:
    #                 parts.append(
    #                     f'<span class="badge text-bg-warning">{name}</span>'
    #                 )
    #             else:
    #                 parts.append(
    #                     f'<span class="badge text-bg-secondary">{name}</span>'
    #                 )
    #         move.lot_badges_html = ' '.join(parts) or ''

    # def _action_assign(self, force_qty=False):
    #     res = super()._action_assign(force_qty=force_qty)

    #     for move in self:
    #         if not move.picking_id.picking_type_id.pick_all_lot_qty:
    #             continue

    #         for line in move.move_line_ids:
    #             if not line.lot_id or line.product_id.tracking != 'lot':
    #                 continue

    #             quants = self.env['stock.quant'].search([
    #                 ('product_id', '=', line.product_id.id),
    #                 ('lot_id', '=', line.lot_id.id),
    #                 ('location_id', '=', line.location_id.id),
    #             ])
    #             reserved = sum(quants.mapped('reserved_quantity'))
    #             lot_qty = line.lot_id.product_qty

    #             is_partial = 0 < reserved < lot_qty
    #             # line.write({
    #             #     'quantity': lot_qty,
    #             #     'is_partial_lot': is_partial,
    #             # })
    #             line.is_partial_lot = is_partial

        # return res


