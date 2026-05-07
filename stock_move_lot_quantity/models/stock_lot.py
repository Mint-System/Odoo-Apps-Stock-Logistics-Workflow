from odoo import models

class StockLot(models.Model):
    _inherit = 'stock.lot'

    def _get_fields_stock_barcode(self):
        fields = super()._get_fields_stock_barcode()
        if 'product_qty' not in fields:
            fields.append('product_qty')
        return fields