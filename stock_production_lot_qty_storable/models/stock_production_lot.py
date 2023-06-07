from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_qty = fields.Float(store=True, readonly=True)
