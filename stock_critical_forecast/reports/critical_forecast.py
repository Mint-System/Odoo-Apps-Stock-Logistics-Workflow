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
    origin = fields.Char('Source Document')
    source_model = fields.Char()
    source_ref = fields.Many2oneReference(model_field='source_model')
    default_code = fields.Char('Internal Reference')
    product_type = fields.Selection(related='product_id.type')
    qty_available = fields.Float(digits='Product Unit of Measure')
    virtual_available = fields.Float(digits='Product Unit of Measure')

    def _get_picking_data(self):

        data = []

        picking_ids = self.env['stock.picking'].search([
            ('state', 'not in', ('cancel', 'draft', 'done')),
            ('picking_type_id.code', '=', 'outgoing'),
            ('company_id', '=', self.env.company.id),
        ])
        _logger.warning(picking_ids) if request.session.debug else {}

        for picking in picking_ids:
            for move in picking.move_lines:
                data.append({
                    'product_id': move.product_id.id,
                    'type_description': move.product_id.type_description,
                    'default_code': move.product_id.default_code,
                    'critical_date': move.date_deadline,
                    'action_date': move.date_deadline,
                    'qty_available': move.product_id.qty_available,
                    'virtual_available': move.product_id.virtual_available,
                    'origin': picking.name,
                    'source_model': picking._name,
                    'source_ref': picking.id,
                })

        return data

    def _get_production_data(self):

        data = []

        production_ids = self.env['mrp.production'].search([
            ('state', 'in', ['draft', 'confirmed']),
            ('company_id', '=', self.env.company.id)
        ])

        _logger.warning(production_ids) if request.session.debug else {}

        for mo in production_ids:
            for move in mo.move_raw_ids:
                data.append({
                    'product_id': move.product_id.id,
                    'type_description': move.product_id.type_description,
                    'default_code': move.product_id.default_code,
                    'critical_date': move.date_deadline,
                    'action_date': move.date_deadline,
                    'qty_available': move.product_id.qty_available,
                    'virtual_available': move.product_id.virtual_available,
                    'origin': move.name,
                    'source_model': mo._name,
                    'source_ref': mo.id,
                })

        return data

    def get_data(self):

        # Remove all data from critical forecast model
        self.env.cr.execute('''
            DELETE FROM stock_critical_forecast
        ''')

        # Get manufacturing order data
        mo_data = self._get_production_data()

        # Get delivery order data
        do_data = self._get_picking_data()
        mo_data.extend(do_data)

        # Create Entry in demand planner
        return self.sudo().create(mo_data)

    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     self.get_data()
    #     return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    def action_product_forecast_report(self):
        self.ensure_one()
        action = self.product_id.action_product_forecast_report()
        action['context'] = {'active_id': self.product_id.id, 'active_ids': [self.product_id.id], 'default_product_id': self.product_id.id, 'active_model': 'product.product'} 
        _logger.warning(action) if request.session.debug else {}
        return action


    def action_open_origin(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "res_model": self.source_model,
            "views": [[False, "form"]],
            "res_id": self.source_ref,
        }
        _logger.warning(action) if request.session.debug else {}
        return action