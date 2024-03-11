import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockProductionLot(models.Model):
    _inherit = "stock.lot"

    product_qty = fields.Float(store=True, readonly=True)
