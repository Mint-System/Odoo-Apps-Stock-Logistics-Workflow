from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _get_available_location_ids(self, product_ids):
        picking_location_ids = self.env['stock.location'].search([('picking_location','=',True)])
        quant_ids = self.search([
            ('product_id', 'in', [product_ids]),
            ('location_id.usage','=', 'internal')
        ]).filtered(lambda q: q.available_quantity > 0)
        available_location_ids = quant_ids.mapped('location_id') + picking_location_ids
        return available_location_ids