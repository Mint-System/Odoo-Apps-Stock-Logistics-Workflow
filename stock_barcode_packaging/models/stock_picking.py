from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'barcodes.barcode_events_mixin']

    @api.model
    def _get_move_line_ids_fields_to_read(self):
        res = super(StockPicking, self)._get_move_line_ids_fields_to_read()
        res.extend(['product_packaging'])
        return res