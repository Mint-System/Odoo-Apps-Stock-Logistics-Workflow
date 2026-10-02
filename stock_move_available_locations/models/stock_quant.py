import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_available_location_ids(self, product_id):
        product_ids = self._normalize_product_ids(product_id)
        picking_location_ids = self.env["stock.location"].search([("picking_location", "=", True)])
        self._set_zero_quant(picking_location_ids, product_ids)
        _logger.warning(f"##### product_ids: {product_ids}")
        quant_ids = self.search(
            [
                ("product_id", "in", product_ids),
                ("location_id.usage", "=", "internal"),
            ]
        ).filtered(lambda q: q.available_quantity > 0)
        return quant_ids.location_id | picking_location_ids

    def _set_zero_quant(self, location_ids, product_ids):
        """creates stock quant with zero quantity for always available locations"""
        for loc in location_ids:
            for pid in product_ids:
                if not self.env["stock.quant"].search_count([("product_id", "=", pid), ("location_id", "=", loc.id)], limit=1):
                    self.env["stock.quant"].create({
                        "product_id": pid,
                        "location_id": loc.id,
                        "quantity": 0.0,
                        "company_id": loc.company_id.id,
                    })


    @api.model
    def _normalize_product_ids(self, product_id):
        if isinstance(product_id, models.BaseModel):
            return product_id.ids
        if isinstance(product_id, (list, tuple)):
            return [int(p) for p in product_id]
        return [int(product_id)]

