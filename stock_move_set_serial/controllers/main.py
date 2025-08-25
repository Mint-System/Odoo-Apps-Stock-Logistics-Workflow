import re
import random
from odoo import http
from odoo.http import request

class StockMoveSerialAutofillController(http.Controller):

    @http.route('/stock_move_set_serial/get_next_serial', type='json', auth='user')
    def get_next_serial(self, product_id):
        product = request.env['product.product'].browse(int(product_id))
        template = product.product_tmpl_id
        last_lot = request.env['stock.lot'].search(
            [('product_id', '=', product.id)], order='name desc', limit=1
        )
        if last_lot:
            match = re.search(r"(\d+)$", last_lot.name)
            if match:
                num = str(int(match.group(1)) + 1).zfill(len(match.group(1)))
                return last_lot.name[:match.start(1)] + num
            else:
                return f"{last_lot.name}-1"

        prefix = template.serial_prefix or ""
        if prefix:
            rand_num = str(random.randint(0, 999999)).zfill(6)
            return f"{prefix}{rand_num}"
        else:
            return ""
