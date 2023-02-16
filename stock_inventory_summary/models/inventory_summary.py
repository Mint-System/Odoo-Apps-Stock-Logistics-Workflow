from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import get_lang
from odoo.osv import expression


class InventorySummary(models.Model):
    _name = 'inventory.summary'
    _description = 'Inventory Summary'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    location_id = fields.Many2one('stock.location')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float()
    standard_price = fields.Float('Cost')
    value = fields.Monetary()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    last_in_date = fields.Datetime()
    last_out_date = fields.Datetime()

    def _get_move_line_data(self, data=[], set_ids=[], to_date=False):
        """Get stock move line data"""
        
        # For each quant get the corresponding move lines      
        quants = self.env['stock.quant'].search([])
        for quant in quants:

            # Domain from action_view_stock_moves
            domain = [
                ('product_id', '=', quant.product_id.id),
                '|',
                    ('location_id', '=', quant.location_id.id),
                    ('location_dest_id', '=', quant.location_id.id),
            ]
            # If date is set filter move lines
            if to_date:                
                domain = expression.AND([[('date', '<=', to_date)], domain])
            lines = self.env['stock.move.line'].search(domain)

            # Calculate quantity from lines
            in_lines = lines.filtered(lambda l: l.location_dest_id == quant.location_id)
            out_lines = lines.filtered(lambda l: l.location_id == quant.location_id)
            quantity = sum(in_lines.mapped('qty_done')) - sum(out_lines.mapped('qty_done'))
            standard_price = quant.product_id.with_company(quant.company_id).standard_price

            data.append({
                'location_id': quant.location_id.id,
                'product_id': quant.product_id.id,
                'last_in_date': max(in_lines.mapped('date')) if in_lines else False,
                'last_out_date': max(out_lines.mapped('date')) if out_lines else False,
                'quantity': quantity,
                'standard_price': standard_price,
                'value': quantity * standard_price if quantity > 0.0 else 0.0,
            })
            set_ids.append((quant.location_id.id, quant.product_id.id))

        return data, set_ids

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        to_date = self._context.get('to_date', False)
        self.get_data(to_date)
        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.model
    def get_data(self, to_date=False):
        """Generate inventory summary data"""

        # Get current data
        curr_ids = self.search([])
        curr_set_ids = [(d.location_id.id, d.product_id.id) for d in curr_ids]

        # Reset data
        data=[]
        set_ids=[]

        # Get stock move line data
        data, set_ids = self._get_move_line_data(data, set_ids, to_date)

        # Create new records
        records = list(filter(lambda d: (d['location_id'], d['product_id']) not in curr_set_ids, data))
        self.create(records)

        # Update existing records
        for curr in curr_ids:
            t = (curr.location_id.id, curr.product_id.id)
            vals = list(filter(lambda d: (d['location_id'], d['product_id']) == t, data))
            if vals:
                curr.write(vals[0])

        # Remove records
        records = self.search([])
        records = records.filtered(lambda d: (d.location_id.id, d.product_id.id) not in set_ids)
        records.unlink()