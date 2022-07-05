from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
import json


class StockMove(models.Model):
    _inherit = "stock.move.line"

    available_location_ids = fields.One2many(related='move_id.available_location_ids')
    location_id_domain = fields.Char(
        compute="_compute_location_id_domain",
        readonly=True,
        store=False,
    )

    @api.depends('product_id')
    def _compute_location_id_domain(self):
        for rec in self:            
            available_location_ids = self.env['stock.quant']._get_available_location_ids(rec.product_id.id)
            rec.location_id_domain = json.dumps(
                [('id', 'in', available_location_ids.ids)]
            )