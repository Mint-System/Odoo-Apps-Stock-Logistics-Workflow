from datetime import datetime, timedelta
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request


class CriticalForecast(models.Model):
    _name = 'stock.critical_forecast'
    _description = 'Critical Forecast'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    # Report fields
    product_id = fields.Many2one('product.product', 'Product')
    type_description = fields.Char()
    action_date = fields.Date()
    critical_date = fields.Date()
    # origin = fields.Char('Source Document')
    # source_model = fields.Char()
    # source_ref = fields.Many2oneReference(model_field='source_model')
    # default_code = fields.Char('Internal Reference')
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
    # activity_ids = fields.One2many(related='product_id.activity_ids', string='Activities')

    def _prepare_move_data(self, move):
        """Generate entry based on move data"""

        # Get data from replenishment report
        replenish_data = move.env['report.stock.report_product_product_replenishment']._get_report_data([move.product_tmpl_id.id])
        # Look for unfilled lines and set as critical date
        unfilled_lines = list(filter(lambda l: not l['replenishment_filled'], replenish_data['lines']))
        replenish_delay = move.product_id.seller_ids[0].delay if move.product_id.seller_ids else move.product_id.produce_delay
        critical_date = datetime.strptime(unfilled_lines[0]['delivery_date'], '%d.%m.%Y %H:%M:%S') if unfilled_lines else None
        # _logger.warning(critical_date) if request.session.debug and move.product_id.id == 39 else {}
        return {
            'product_id': move.product_id.id,
            'type_description': move.product_id.type_description,
            # 'default_code': move.product_id.default_code,
            'critical_date': critical_date,
            'action_date': critical_date - timedelta(days=replenish_delay) if critical_date else None,
            'qty_available': move.product_id.qty_available,
            'replenish_delay': replenish_delay,
            'virtual_available': move.product_id.virtual_available,
            'min_qty': move.product_id.seller_ids[0].min_qty if move.product_id.seller_ids else 0,
            'product_min_qty': move.product_id.orderpoint_ids[0].product_min_qty if move.product_id.orderpoint_ids else 0,
            'qty_in': replenish_data['qty']['in'],
            'qty_out': replenish_data['qty']['out'],
            'promised_qty': sum(self.env['sale.blanket.order.line'].search([('product_id', '=', move.product_id.id)]).mapped('remaining_uom_qty')) if move.product_id.sale_ok else 0,
            'agreed_qty': sum(self.env['purchase.requisition.line'].search([('product_id', '=', move.product_id.id)]).mapped(lambda l: l.product_qty - l.qty_ordered)) if move.product_id.purchase_ok else 0,
            'route_id': move.product_id.route_ids[0].id if move.product_id.route_ids else False,
            'seller_id': move.product_id.seller_ids[0].name.id if move.product_id.seller_ids else False,
        }

    def _get_picking_data(self, data=[], product_ids=[]):
        """Get data delivery orders"""
        
        self.env['stock.picking'].clear_caches()
        picking_ids = self.env['stock.picking'].search([
            ('state', 'not in', ('cancel', 'draft', 'done')),
            ('picking_type_id.code', '=', 'outgoing'),
            ('company_id', '=', self.env.company.id),
        ])
        # _logger.warning([picking_ids]) if request.session.debug else {}

        for picking in picking_ids:
            for move in picking.move_lines.filtered(lambda m: m.product_id.id not in product_ids):
                rec1 = self._prepare_move_data(move)
                rec2 = {
                    # 'origin': picking.name,
                    # 'source_model':  picking._name,
                    # 'source_ref': picking.id,
                }
                data.append({**rec1, **rec2})
                product_ids.append(move.product_id.id)

        return data, product_ids

    def _get_production_data(self, data=[], product_ids=[]):
        """Get data for manufacturing orders"""

        production_ids = self.env['mrp.production'].search([
            ('state', 'in', ['draft', 'confirmed']),
            ('company_id', '=', self.env.company.id)
        ])

        # _logger.warning(production_ids) if request.session.debug else {}

        for mo in production_ids:
            for move in mo.move_raw_ids.filtered(lambda m: m.product_id.id not in product_ids):
                record = self._prepare_move_data(move)
                rec1 = self._prepare_move_data(move)
                rec2 = {
                    # 'origin': mo.name,
                    # 'source_model':  mo._name,
                    # 'source_ref': mo.id,
                }
                data.append({**rec1, **rec2})
                product_ids.append(move.product_id.id)

        return data, product_ids

    def get_data(self):
        """Generate report data"""

        # Get current data
        current_ids = self.search([])
        current_product_ids = current_ids.mapped('product_id.id')

        # Reset data
        data=[]
        product_ids=[]

        # Get manufacturing order data
        data, product_ids = self._get_production_data(data, product_ids)

        # Get delivery order data
        data, product_ids = self._get_picking_data(data, product_ids)

        # _logger.warning([current_product_ids, product_ids]) if request.session.debug else {}

        # Remove all data from critical forecast model
        # _logger.warning("Remove all data") if request.session.debug else {}
        # self.search([]).unlink()
        # self.env.cr.execute('''
        #     DELETE FROM stock_critical_forecast
        # ''')

        # Create entries
        # _logger.warning("Create entries") if request.session.debug else {}
        self.create(list(filter(lambda d: d['product_id'] not in current_product_ids, data)))

        # Update entries
        # _logger.warning("Update all data") if request.session.debug else {}
        for curr in current_ids:
            vals = list(filter(lambda d: d['product_id'] == curr.product_id.id, data))
            if vals:
                curr.write(vals[0])

        # Unlink entries
        # _logger.warning("Remove entries") if request.session.debug else {}
        self.search([('product_id','not in', product_ids)]).unlink()
        # self.create(data)

    def action_product_forecast_report(self):
        """Open forecast report"""
        self.ensure_one()
        action = self.product_id.action_product_forecast_report()
        action['context'] = {'active_id': self.product_id.id, 'active_ids': [self.product_id.id], 'default_product_id': self.product_id.id, 'active_model': 'product.product'} 
        # _logger.warning(action) if request.session.debug else {}
        return action

    # def action_open_origin(self):
    #     """Open source document"""
    #     self.ensure_one()
    #     action = {
    #         "type": "ir.actions.act_window",
    #         "res_model": self.source_model,
    #         "views": [[False, "form"]],
    #         "res_id": self.source_ref,
    #     }
    #     _logger.warning(action) if request.session.debug else {}
    #     return action

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # _logger.warning(domain) if request.session.debug else {}
        # if domain:
        #     domain[0].append(['type_description', 'ilike', domain[0][0] ])
        return super(CriticalForecast, self).search_read(domain, fields, offset, limit, order)
