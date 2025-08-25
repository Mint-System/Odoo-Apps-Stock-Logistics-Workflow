/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { GenerateDialog } from "@stock/widgets/generate_serial";
import { rpc } from "@web/core/network/rpc";
import { onMounted } from "@odoo/owl";

patch(GenerateDialog.prototype, {
    setup() {
        super.setup();
        console.log("GenerateDialog setup", this.props);
        console.log("next serial", this.nextSerial);

        // if (this.props.mode === "generate" && this.props.move?.data?.product_id) {
        //     console.log("next serial will be set");
        //     const productId = this.props.move.data.product_id[0];
        //     try {
        //         // const nextSerial = await rpc("/purchase_serial_autofill/get_next_serial", {
        //         //     product_id: productId,
        //         // });
        //         // const nextSerial = "test123456789"; // for first test
        //         // if (nextSerial && this.nextSerial?.el) {
        //         //     this.nextSerial.el.value = nextSerial;
        //         // }
        //         this.nextSerial.el.value = "test123456789";
        //     } catch (err) {
        //         console.warn("Failed to get next serial", err);
        //     }
        // }
        onMounted(async () => {
            if (this.props.mode === "generate" && this.props.move?.data?.product_id) {
                const productId = this.props.move.data.product_id[0];
                console.log("productId", productId);
                try {
                    const nextSerial = await rpc("/stock_move_set_serial/get_next_serial", {
                        product_id: productId,
                    });
                    if (nextSerial && this.nextSerial?.el) {
                        this.nextSerial.el.value = nextSerial;
                    }
                } catch (err) {
                    console.warn("Failed to fetch next serial", err);
                }
            }
        });
    },
});