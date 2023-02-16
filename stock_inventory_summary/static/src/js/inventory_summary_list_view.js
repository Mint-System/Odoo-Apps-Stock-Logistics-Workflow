odoo.define('stock.InventorySummaryListView', function (require) {
"use strict";

var ListView = require('web.ListView');
var InventorySummaryListController = require('stock.InventorySummaryListController');
var viewRegistry = require('web.view_registry');


var InventorySummaryListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: InventorySummaryListController,
    }),
});

viewRegistry.add('inventory_summary_list', InventorySummaryListView);

return InventorySummaryListView;

});
