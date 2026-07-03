# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"


    def split_and_validate_automatically(self):
        _logger.warning("split_and_validate_automatically called")
        auto_pick_moves = self.move_ids.filtered(
                lambda m: m.product_id.pick_and_validate_automatically and m.state not in ('done', 'cancel')
            )
        if not auto_pick_moves:
            return False

        if auto_pick_moves == self.move_ids:
            # all moves are autmatically picked => no need to split
            new_picking = self
        else:
            new_picking = self.copy({
                'move_ids': [],
                'origin': self.origin,
            })
            auto_pick_moves.write({'picking_id': new_picking.id})
            auto_pick_moves.move_line_ids.write({'picking_id': new_picking.id})
            self.invalidate_recordset(['move_ids', 'move_line_ids'])
            new_picking.action_confirm()

        # set qty_done and validate immediately
        for move in new_picking.move_ids:
            move.quantity = move.product_uom_qty
        new_picking.with_context(skip_immediate=True).button_validate()

