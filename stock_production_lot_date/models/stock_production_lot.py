from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    date = fields.Datetime()

    @api.constrains('name', 'date', 'product_id', 'company_id')
    def _check_unique_lot(self):
        """
        OVERWRITE: Lot is unique in combination with date 
        odoo/addons/stock/models/stock_production_lot.py
        """
        domain = [('product_id', 'in', self.product_id.ids),
                  ('company_id', 'in', self.company_id.ids),
                  ('name', 'in', self.mapped('name')),
                  ('date', '=', self.date)]
        fields = ['company_id', 'product_id', 'name', 'date']
        groupby = ['company_id', 'product_id', 'name', 'date']
        records = self.read_group(domain, fields, groupby, lazy=False)
        error_message_lines = []
        for rec in records:
            if rec['__count'] != 1:
                product_name = self.env['product.product'].browse(rec['product_id'][0]).display_name
                error_message_lines.append(_(" - Product: %s, Serial Number: %s, Date: %s", product_name, rec['name'], rec['date']))
        if error_message_lines:
            raise ValidationError(_('The combination of serial number and product must be unique across a company.\nFollowing combination contains duplicates:\n') + '\n'.join(error_message_lines))


    @api.onchange('date', 'product_id')
    def _onchange_date(self):
        """
        Map exipiration date fields wit lot date
        """
        mapped_fields = {
            'expiration_date': 'expiration_time',
            'use_date': 'use_time',
            'removal_date': 'removal_time',
            'alert_date': 'alert_time'
        }
        product = self.product_id
        if product:
            for field in mapped_fields:
                duration = getattr(product, mapped_fields[field])
                if duration:
                    date = (self.date or datetime.now()) + timedelta(days=duration)
                    self[field] = fields.Datetime.to_string(date)

    def _format_date(self, date):
        """
        Format date field in user language.
        """
        lang_model = self.env['res.lang']
        lang = lang_model._lang_get(self.env.user.lang)
        date_format = lang.date_format
        return date.strftime(date_format)

    def name_get(self):
        res = []
        for rec in self:
            if rec.date:
                res.append((rec.id, '%s (%s)' % (rec.name, self._format_date(rec.date))))
            else:
                res.append((rec.id, rec.name))
        return res
