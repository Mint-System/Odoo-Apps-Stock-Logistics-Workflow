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

    def _get_move_line_data(self, data=[], set_ids=[], to_date=False, location_usage_internal=True, location_id=False):
        """Get stock move line data"""
        
        # Apply filter and load data
        domain = []
        if location_usage_internal:
            domain = [
                ('location_id.usage', '=', 'internal')
            ]
        if location_id:
            domain = expression.AND([[('location_id', 'child_of', location_id.id)], domain])
        quants = self.env['stock.quant'].search(domain)
        domain = []
        if location_usage_internal:
            domain = [
                '|',
                    ('location_id.usage', '=', 'internal'),
                    ('location_dest_id.usage', '=', 'internal')
            ]
        if location_id:
            domain = expression.AND([[
                '|',
                    ('location_id', 'child_of', location_id.id),
                    ('location_dest_id', 'child_of', location_id.id)
            ], domain])
        lines = self.env['stock.move.line'].search(domain)

        # For each quant get the corresponding move lines    
        for quant in quants:

            # If date is set filter move lines
            if to_date:                
                quant_lines = lines.filtered(lambda l:
                    l.date <= to_date and
                    l.product_id.id == quant.product_id.id and
                    (l.location_id.id == quant.location_id.id or l.location_dest_id.id == quant.location_id.id)
                )
            else:
                quant_lines = lines.filtered(lambda l:
                    l.product_id.id == quant.product_id.id and
                    (l.location_id.id == quant.location_id.id or l.location_dest_id.id == quant.location_id.id)
                )
            
            # Calculate quantity from lines
            in_lines = quant_lines.filtered(lambda l: l.location_dest_id == quant.location_id)
            out_lines = quant_lines.filtered(lambda l: l.location_id == quant.location_id)
            # Convert to base unit
            in_quantities = in_lines.mapped(lambda l: l.product_uom_id._compute_quantity(l.qty_done, l.product_id.uom_id))
            out_quantities = in_lines.mapped(lambda l: l.product_uom_id._compute_quantity(l.qty_done, l.product_id.uom_id))
            quantity = sum(in_quantities) - sum(out_quantities)
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

    @api.model
    def get_data(self, to_date=False, location_usage_internal=True, location_id=False):
        """Generate inventory summary data"""

        # Get current data
        # curr_ids = self.search([])
        # curr_set_ids = [(d.location_id.id, d.product_id.id) for d in curr_ids]

        # Reset data
        data=[]
        set_ids=[]

        # Get stock move line data
        data, set_ids = self._get_move_line_data(data, set_ids, to_date, location_usage_internal, location_id)

        # Clear data and create records
        self.env.cr.execute('DELETE FROM inventory_summary')
        self.create(data)

        # # Create new records
        # records = list(filter(lambda d: (d['location_id'], d['product_id']) not in curr_set_ids, data))
        # self.create(records)

        # # Update existing records
        # for curr in curr_ids:
        #     t = (curr.location_id.id, curr.product_id.id)
        #     vals = list(filter(lambda d: (d['location_id'], d['product_id']) == t, data))
        #     if vals:
        #         curr.write(vals[0])

        # # Remove records
        # records = self.search([])
        # records = records.filtered(lambda d: (d.location_id.id, d.product_id.id) not in set_ids)
        # records.unlink()