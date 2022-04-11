from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockRule(models.Model):

    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
    ):
        res = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )
        res.update({"description_picking": values.get("product_description_variants")})
        return res
