
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    move_orig_state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')],
        string='Upstream Status', copy=False, readonly=True,
        compute='_compute_move_orig_state')

    @api.depends('move_orig_ids.state')
    def _compute_move_orig_state(self):
        for move in self:
            if move.move_orig_ids:
                move.move_orig_state = move.move_orig_ids[0].state
            else:
                move.move_orig_state = False