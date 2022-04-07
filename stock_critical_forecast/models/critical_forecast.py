import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)
from odoo.http import request
from datetime import datetime, timedelta


class CriticalForecast(models.Model):
    _name = 'critical.forecast'
    _description = 'Critical Forecast'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Product')
    type_description = fields.Char()
    action_date = fields.Date()
    critical_date = fields.Date()
    product_type = fields.Selection(related='product_id.type')
    qty_available = fields.Float(digits='Product Unit of Measure')
    virtual_available = fields.Float(digits='Product Unit of Measure')
    replenish_delay = fields.Integer()
    min_qty = fields.Integer()
    product_min_qty = fields.Integer()
    qty_in = fields.Float(digits='Product Unit of Measure')
    qty_out = fields.Float(digits='Product Unit of Measure')
    promised_qty = fields.Float(digits='Product Unit of Measure')
    agreed_qty = fields.Float(digits='Product Unit of Measure')
    route_id = fields.Many2one('stock.location.route', 'Route')
    seller_id = fields.Many2one('res.partner', 'Vendor')

    def _compute_critical_date(self, replenish_data):
        problematic_lines = list(filter(lambda l: not l['replenishment_filled'] or l['is_late'], replenish_data['lines']))
        return datetime.strptime(problematic_lines[0]['delivery_date'], '%d.%m.%Y %H:%M:%S') if problematic_lines else None

    def _compute_replenish_delay(self, move):
        return move.product_id.seller_ids[0].delay if move.product_id.seller_ids else move.product_id.produce_delay

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
        replenish_delay = self._compute_replenish_delay(move)
        critical_date = self._compute_critical_date(replenish_data)
        promised_qty = self._compute_promised_qty(move)
        agreed_qty = self._compute_agreed_qty(move)
        return {
            'product_id': move.product_id.id,
            'type_description': move.product_id.type_description,
            'critical_date': critical_date,
            'action_date': critical_date - timedelta(days=replenish_delay) if critical_date else None,
            'replenish_delay': replenish_delay,
            'qty_available': move.product_id.qty_available,
            'virtual_available': move.product_id.virtual_available,
            'min_qty': move.product_id.seller_ids[0].min_qty if move.product_id.seller_ids else 0,
            'product_min_qty': move.product_id.orderpoint_ids[0].product_min_qty if move.product_id.orderpoint_ids else 0,
            'qty_in': replenish_data['qty']['in'],
            'qty_out': replenish_data['qty']['out'],
            'promised_qty': promised_qty,
            'agreed_qty': agreed_qty,
            'route_id': move.product_id.route_ids[0].id if move.product_id.route_ids else False,
            'seller_id': move.product_id.seller_ids[0].name.id if move.product_id.seller_ids else False,
        }

    def _get_picking_data(self, data=[], product_ids=[]):
        """Get data delivery orders"""
        
        # Clear cache
        self.env['stock.picking'].clear_caches()

        # Lookup unfinished outgoing delivery ordrers
        picking_ids = self.env['stock.picking'].search([
            ('state', 'not in', ('cancel', 'draft', 'done')),
            ('picking_type_id.code', '=', 'outgoing'),
            ('company_id', '=', self.env.company.id),
        ])
        _logger.warning([picking_ids]) if request.session.debug else {}

        for picking in picking_ids:
            for move in picking.move_lines.filtered(lambda m: m.product_id.id not in product_ids):
                replenish_data = self.env['report.stock.report_product_product_replenishment']._get_report_data([move.product_tmpl_id.id])              
                data.append(self._prepare_report_line(move, replenish_data))
                product_ids.append(move.product_id.id)

        return data, product_ids

    def _get_production_data(self, data=[], product_ids=[]):
        """Get data for manufacturing orders"""

        # Lookup unfinished manufacturing orders
        production_ids = self.env['mrp.production'].search([
            ('state', 'in', ['draft', 'confirmed']),
            ('company_id', '=', self.env.company.id)
        ])
        _logger.warning(production_ids) if request.session.debug else {}

        for mo in production_ids:
            for move in mo.move_raw_ids.filtered(lambda m: m.product_id.id not in product_ids):
                replenish_data = self.env['report.stock.report_product_product_replenishment']._get_report_data([move.product_tmpl_id.id])
                data.append(self._prepare_report_line(move, replenish_data))
                product_ids.append(move.product_id.id)

        return data, product_ids

    def get_data(self):
        """Generate critical forecast data"""

        # Get current data
        current_ids = self.search([])
        current_product_ids = current_ids.mapped('product_id.id')
        _logger.warning([current_ids]) if request.session.debug else {}

        # Reset data
        data=[]
        product_ids=[]

        # Get manufacturing order data
        data, product_ids = self._get_production_data(data, product_ids)

        # Get delivery order data
        data, product_ids = self._get_picking_data(data, product_ids)

        # Create entries
        self.create(list(filter(lambda d: d['product_id'] not in current_product_ids, data)))

        # Update entries
        for curr in current_ids:
            vals = list(filter(lambda d: d['product_id'] == curr.product_id.id, data))
            if vals:
                curr.write(vals[0])

        # Unlink entries
        self.search([('product_id','not in', product_ids)]).unlink()


    def action_product_forecast_report(self):
        """Open product forecast report"""
        self.ensure_one()
        action = self.product_id.action_product_forecast_report()
        action['context'] = {'active_id': self.product_id.id, 'active_ids': [self.product_id.id], 'default_product_id': self.product_id.id, 'active_model': 'product.product'} 
        _logger.warning(action) if request.session.debug else {}
        return action