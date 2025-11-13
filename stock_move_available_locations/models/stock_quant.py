import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_available_location_ids(self, product_id):
        picking_location_ids = self.env["stock.location"].search([("picking_location", "=", True)])
        self._set_zero_quant(picking_location_ids, product_id)
        quant_ids = self.search(
            [
                ("product_id", "in", [product_id]),
                ("location_id.usage", "=", "internal"),
            ]
        ).filtered(lambda q: q.available_quantity > 0)
        available_location_ids = quant_ids.mapped("location_id") + picking_location_ids
        return available_location_ids

    def _set_zero_quant(self, location_ids, product_id):
        """creates stock quant with zero quantity for always available locations"""
        for loc_id in location_ids:
            if not self.env["stock.quant"].search([("product_id", "=", product_id), ("location_id", "=", loc_id.id)]):
                self.env["stock.quant"].create(
                    {
                        "product_id": product_id,
                        "location_id": loc_id.id,
                        "quantity": 0.0,
                        "reserved_quantity": 0.0,
                        "company_id": loc_id.company_id.id,
                    }
                )
