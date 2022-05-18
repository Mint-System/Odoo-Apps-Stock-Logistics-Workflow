import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)
from odoo.http import request
from datetime import datetime, timedelta


class CriticalForecast(models.Model):
    _inherit = 'critical.forecast'

    promised_qty = fields.Float(digits='Product Unit of Measure')
    agreed_qty = fields.Float(digits='Product Unit of Measure')

    def _compute_agreed_qty(self, move):
        if move.product_id.purchase_ok:
            requisition_ids = self.env['purchase.requisition.line'].search([('product_id', '=', move.product_id.id)])
            agreed_qty = sum(requisition_ids.mapped(lambda l: l.product_qty - l.qty_ordered))
        else:
            agreed_qty = 0
        return agreed_qty

    def _compute_promised_qty(self, move):
        if move.product_id.sale_ok:
            line_ids = self.env['sale.blanket.order.line'].search([('product_id', '=', move.product_id.id)])
            promised_qty = sum(line_ids.mapped('remaining_uom_qty'))
        else:
            promised_qty = 0
        return promised_qty

    def _prepare_report_line(self, move, replenish_data):
        data = super()._prepare_report_line(move, replenish_data)
        
        promised_qty = self._compute_promised_qty(move)
        agreed_qty = self._compute_agreed_qty(move)

        data.update({
            'promised_qty': promised_qty,
            'agreed_qty': agreed_qty,
        })
        
        return data