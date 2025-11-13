import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    available_location_ids = fields.One2many("stock.location", compute="_compute_available_location_ids")

    @api.depends("product_id")
    def _compute_available_location_ids(self):
        for rec in self:
            if rec.product_id:
                rec.available_location_ids = self.env["stock.quant"]._get_available_location_ids(rec.product_id.id)
            else:
                rec.available_location_ids = False
