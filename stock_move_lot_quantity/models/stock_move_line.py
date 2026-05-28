from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'


    @api.onchange('lot_id')
    def _onchange_lot_id_fill_quantity(self):
        for line in self:
            if not line.lot_id or line.product_id.tracking == 'lot':
                continue
            if line.picking_id.picking_type_id.pick_all_lot_qty:
                line.quantity = line.lot_id.product_qty
