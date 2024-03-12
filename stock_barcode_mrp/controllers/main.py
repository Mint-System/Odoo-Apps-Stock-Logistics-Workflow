import logging

from odoo import _, http
from odoo.http import request

from odoo.addons.stock_barcode.controllers import StockBarcodeController

_logger = logging.getLogger(__name__)


class StockBarcodeMRPController(StockBarcodeController):
    @http.route()
    def main_menu(self, barcode, **kw):
        ret_open_mo = self.try_open_mo(barcode)
        # _logger.warning(['ret_open_mo', ret_open_mo])
        if ret_open_mo:
            return ret_open_mo
        return super().main_menu(barcode)

    def try_open_mo(self, barcode):
        """If barcode represents a manufacturing order, open it"""
        corresponding_mo = request.env["mrp.production"].search(
            [("name", "like", barcode)], limit=1
        )
        # _logger.warning(['corresponding_mo', corresponding_mo])

        # If mo is done and backorders exist, set latest backorder as corrensponding mo
        backorder_ids = (
            corresponding_mo.procurement_group_id.mrp_production_ids.filtered(
                lambda o: o.state not in ["draft", "done", "cancel"]
            )
        )
        # _logger.warning(['backorder_ids', backorder_ids])
        if backorder_ids and corresponding_mo.state in ["draft", "done", "cancel"]:
            corresponding_mo = backorder_ids = backorder_ids[0]

        # Return workorder for mo if one exists
        ret_open_wo = self.try_open_wo(corresponding_mo)
        if ret_open_wo:
            return ret_open_wo

        # Otherwise return correnspondig mo
        if corresponding_mo:
            view_id = request.env.ref("mrp.mrp_production_form_view").id
            return {
                "action": {
                    "name": _("Open manufacturing order form"),
                    "res_model": "mrp.production",
                    "view_mode": "form",
                    "view_id": view_id,
                    "views": [(view_id, "form")],
                    "type": "ir.actions.act_window",
                    "res_id": corresponding_mo.id,
                }
            }

        return False

    def try_open_wo(self, corresponding_mo):
        workorder_id = corresponding_mo.workorder_ids.filtered(
            lambda o: o.state in ["ready", "progress"]
        )
        if workorder_id:
            # _logger.warning(['workorder_id', workorder_id])
            if (
                not workorder_id.is_user_working
                and workorder_id.working_state != "blocked"
                and workorder_id.state in ("ready", "progress", "pending")
            ):
                workorder_id.button_start()
            view_id = request.env.ref("mrp_workorder.mrp_workorder_view_form_tablet").id
            return {
                "action": {
                    "name": _("Open workorder form"),
                    "res_model": "mrp.workorder",
                    "view_mode": "form",
                    "view_id": view_id,
                    "views": [(view_id, "form")],
                    "type": "ir.actions.act_window",
                    "res_id": workorder_id.id,
                    "target": "fullscreen",
                    "flags": {
                        "withControlPanel": False,
                        "form_view_initial_mode": "edit",
                    },
                }
            }
