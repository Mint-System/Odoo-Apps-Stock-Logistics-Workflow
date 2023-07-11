import logging
from odoo import http, _
from odoo.http import request
from odoo.addons.stock_barcode.controllers.main import StockBarcodeController
_logger = logging.getLogger(__name__)


class StockBarcodeMRPController(StockBarcodeController):

    @http.route()
    def main_menu(self, barcode, **kw):
        ret_open_me = self.try_open_me(barcode)
        # _logger.warning(['ret_open_mo', ret_open_mo])
        if ret_open_me:
            return ret_open_me
        return super().main_menu(barcode)

    def try_open_me(self, barcode):
        """If barcode represents a maintenance equipment, open it"""
        corresponding_me = request.env['maintenance.equipment'].search([('barcode', 'like', barcode)], limit=1)

        # Return correnspondig me
        if corresponding_me:
            view_id = request.env.ref('maintenance.hr_equipment_view_form').id
            return {
                'action': {
                    'name': _('Open maintenance equipment form'),
                    'res_model': 'maintenance.equipment',
                    'view_mode': 'form',
                    'view_id': view_id,
                    'views': [(view_id, 'form')],
                    'type': 'ir.actions.act_window',
                    'res_id': corresponding_me.id,
                }
            }
            
        return False
