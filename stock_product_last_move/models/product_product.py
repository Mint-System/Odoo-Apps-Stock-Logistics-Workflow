from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    last_incoming_line_id = fields.Many2one(
        comodel_name='stock.move.line',
        compute='_compute_last_incoming_line_id',
        string='Last Purchase Line',
    )
    last_incoming_date = fields.Datetime(
        compute='_compute_last_incoming_line_id',
        string='Last Incoming Date'
    )
    last_outgoing_line_id = fields.Many2one(
        comodel_name='stock.move.line',
        compute='_compute_last_outgoing_line_id',
        string='Last Outgoing Line',
    )
    last_ougtoing_date = fields.Datetime(
        compute='_compute_last_outgoing_line_id',
        string='Last Outgoing Date'
    )

    @api.depends('qty_available')
    def _compute_last_incoming_line_id(self):
        for product in self:
            domain = [
                ('product_id', '=', product.id),
                ('location_id.usage', '=', 'supplier'),
                ('state', '=', 'done'),
            ]
            last_line_id = self.env['stock.move.line'].search(domain, limit=1, order='date desc')
            # _logger.warning([product.name, last_line_id])
            product.last_incoming_line_id = last_line_id
            product.last_incoming_date = last_line_id.date if last_line_id else False

    @api.depends('qty_available')
    def _compute_last_outgoing_line_id(self):
        for product in self:
            domain = [
                ('product_id', '=', product.id),
                ('location_dest_id.usage', 'in', ['customer', 'production']),
                ('state', '=', 'done'),
            ]
            last_line_id = self.env['stock.move.line'].search(domain, limit=1, order='date desc')
            # _logger.warning([product.name, last_line_id])
            product.last_outgoing_line_id = last_line_id
            product.last_ougtoing_date = last_line_id.date if last_line_id else False
