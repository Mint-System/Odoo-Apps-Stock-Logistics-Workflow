odoo.define('demand_planner.action_refresh', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var _t = core._t;

    ListController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.container_last_updated_on').addClass('d-none');
                this.set_last_update_date();
                this.$buttons.find('.oe_action_button').click(this.proxy('action_refresh'));
            }
         },
        action_refresh: function () {
            var self =this;
            var user = session.uid;
            rpc.query({
                model: 'stock.critical_forecast',
                method: 'get_data',
                context: session.user_context,
                args: [[user]],
            }).then(function (e) {
                self.set_last_update_date();
                self.trigger_up('reload');
            });
        },
        set_last_update_date: function () {
            return this._rpc({
                model: this.modelName,
                method: 'search_read',
                args: [[], ['create_date']],
                kwargs: {
                    limit: 1,
                },
            }).then((result) => {
                if (result.length) {
                    this.$buttons.find('.container_last_updated_on').removeClass('d-none');
                    this.$buttons.find('.container_last_updated_date').text(moment(result[0].create_date).format('lll'));
                } else {
                    this.$buttons.find('.container_last_updated_on').addClass('d-none');
                }
            });
        },
    });
});
