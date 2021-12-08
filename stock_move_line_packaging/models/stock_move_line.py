from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move.line"

    product_packaging = fields.Many2one(related='move_id.product_packaging', string='Package')
