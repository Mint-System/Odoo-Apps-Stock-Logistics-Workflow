from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    is_partial_lot = fields.Boolean(
        string='Partial Lot',
        readonly=False,
        store=True,
    )


    @api.onchange('lot_id')
    def _onchange_lot_id_fill_quantity(self):
        for line in self:
            if line.lot_id and line.product_id.tracking == 'lot':

                line.quantity = line.lot_id.product_qty
                line.is_partial_lot = False