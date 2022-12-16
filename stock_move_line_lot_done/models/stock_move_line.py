from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('lot_name', 'lot_id')
    def _onchange_serial_number(self):
        """
        Set qty_done if lot is set.
        """
        res = super()._onchange_serial_number()
        # _logger.warning([self.product_id.tracking == 'lot', ])
        if self.product_id.tracking == 'lot':
            if not self.qty_done:
                self.qty_done = self.product_uom_qty if self.product_uom_qty else 0.0
        return res