import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    pick_all_lot_qty = fields.Boolean(
        string='Pick All Lot Quantity',
        default=False,
        help='If enabled, done quantity is set to the full on-hand quantity '
             'of each lot instead of the reserved quantity.',
    )