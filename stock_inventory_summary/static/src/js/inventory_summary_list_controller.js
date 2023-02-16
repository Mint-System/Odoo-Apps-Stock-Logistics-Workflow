odoo.define('stock.InventorySummaryListController', function (require) {
"use strict";

var core = require('web.core');
var ListController = require('web.ListController');

var qweb = core.qweb;


var InventorySummaryListController = ListController.extend({

    // -------------------------------------------------------------------------
    // Public
    // -------------------------------------------------------------------------

    init: function (parent, model, renderer, params) {
        this.context = renderer.state.getContext();
        return this._super.apply(this, arguments);
    },

    /**
     * @override
     */
    renderButtons: function ($node) {
        this._super.apply(this, arguments);
        if (this.context.no_at_date) {
            return;
        }
        var $buttonToDate = $(qweb.render('InventorySummary.Buttons'));
        $buttonToDate.on('click', this._onOpenWizard.bind(this));
        this.$buttons.prepend($buttonToDate);
    },

    // -------------------------------------------------------------------------
    // Handlers
    // -------------------------------------------------------------------------

    /**
     * Handler called when the user clicked on the 'Inventory at Date' button.
     * Opens wizard to display, at choice, the products inventory or a computed
     * inventory at a given date.
     */
    _onOpenWizard: function () {
        this.do_action({
            res_model: 'inventory.summary.history',
            views: [[false, 'form']],
            target: 'new',
            type: 'ir.actions.act_window',
        });
    },
});

return InventorySummaryListController;

});
