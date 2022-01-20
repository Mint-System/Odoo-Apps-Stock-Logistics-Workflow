from datetime import datetime, timedelta
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class CriticalForecast(models.Model):
    _name = 'stock.critical_forecast'
    _description = 'Critical Forecast'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', 'Product')
    critical_date = fields.Date()

    def get_data(self):

        # Remove all data from critical forecast model
        self.env.cr.execute('''
            DELETE FROM stock_critical_forecast
        ''')

        return {}
