from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    available_location_ids = fields.One2many('stock.location', string='Available Picking Locations', compute='_compute_available_location_ids')

    def _compute_available_location_ids(self):
        for rec in self:
            rec.available_location_ids = self.env['stock.quant']._get_available_location_ids(rec.move_ids_without_package.mapped('product_id').ids)