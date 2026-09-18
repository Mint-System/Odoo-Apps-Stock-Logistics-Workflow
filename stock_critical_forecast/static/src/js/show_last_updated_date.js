/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { onWillStart } from "@odoo/owl";
import { deserializeDateTime } from "@web/core/l10n/dates";

patch(ListController.prototype, {
    setup() {
        super.setup();
        onWillStart(async () => {
            if (this.props.resModel === "critical.forecast") {
                const result = await this.orm.searchRead(
                    this.props.resModel,
                    [],
                    ["write_date"],
                    { limit: 1, order: "write_date desc" }
                );

                this.lastUpdated = result.length
                    ? deserializeDateTime(result[0].write_date).toLocaleString(
                          luxon.DateTime.DATETIME_MED
                      )
                    : null;
            }
        });
    },
});
