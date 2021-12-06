from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    product_packaging = fields.Many2one('product.packaging', string='Package', compute="_compute_product_packaging")

    def _compute_product_packaging(self):
        for rec in self:
            if rec.sale_line_id and rec.sale_line_id.product_packaging:
                rec.product_packaging = rec.sale_line_id.product_packaging
