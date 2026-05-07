/** @odoo-module **/
import BarcodeModel from "@stock_barcode/models/barcode_model";
import { patch } from "@web/core/utils/patch";

patch(BarcodeModel.prototype, {

    async _parseBarcode(barcode, filters) {
        const result = await super._parseBarcode(barcode, filters);

        if (result.lot) {
            const product = result.product ||
                this.cache.getRecord("product.product", result.lot.product_id);
            if (product?.tracking === "lot" && result.lot.product_qty > 0) {
                result.quantity = result.lot.product_qty;
            }
        }

        return result;
    },
});