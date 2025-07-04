import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    product_standard_price = fields.Float(
        string="Standard Cost",
        related='product_id.standard_price',
        store=True
    )
