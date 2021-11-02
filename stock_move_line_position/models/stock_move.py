from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    position = fields.Integer("Pos", compute='_compute_get_position')

    def _compute_get_position(self):
        for rec in self:
            if rec.picking_id.sale_id:
                rec.position = rec.picking_id.sale_id.get_position(rec.product_id, rec.product_uom_qty)
            elif rec.picking_id.purchase_id:
                rec.position = rec.picking_id.purchase_id.get_position(rec.product_id, rec.product_uom_qty)
            else:
                rec.position = 0