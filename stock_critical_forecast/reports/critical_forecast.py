from datetime import datetime, timedelta
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request


class CriticalForecast(models.Model):
    _name = 'stock.critical_forecast'
    _description = 'Critical Forecast'
    _rec_name = 'product_id'

    # Report fields
    product_id = fields.Many2one('product.product', 'Product')
    type_description = fields.Char()
    action_date = fields.Date()
    critical_date = fields.Date()
    # origin = fields.Char('Source Document')
    # source_model = fields.Char()
    # source_ref = fields.Many2oneReference(model_field='source_model')
    default_code = fields.Char('Internal Reference')
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
            'default_code': move.product_id.default_code,
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
            'agreed_qty': move.product_id.purchased_product_qty,
            'route_id': move.product_id.route_ids[0].id if move.product_id.route_ids else 0,
            'seller_id': move.product_id.seller_ids[0].name.id if move.product_id.seller_ids else 0,
        }

    def _get_picking_data(self, data=[], product_ids = []):
        """Get data delivery orders"""
        
        picking_ids = self.env['stock.picking'].search([
            ('state', 'not in', ('cancel', 'draft', 'done')),
            ('picking_type_id.code', '=', 'outgoing'),
            ('company_id', '=', self.env.company.id),
        ])

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

    def _get_production_data(self, data=[], product_ids = []):
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

        # Remove all data from critical forecast model
        self.env.cr.execute('''
            DELETE FROM stock_critical_forecast
        ''')

        # Get manufacturing order data
        data, product_ids = self._get_production_data()

        # Get delivery order data
        data, product_ids = self._get_picking_data(data, product_ids)

        # Create Entry in demand planner
        return self.sudo().create(data)

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