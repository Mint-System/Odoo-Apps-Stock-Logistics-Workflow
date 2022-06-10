odoo.define('stock_critical_forecast.show_last_updated_date', function (require) {
    "use strict"

    var ListController = require('web.ListController')
    var session = require('web.session')
    var ulang = session.user_context['lang'].replace('_','-')
    
    ListController.include({
        renderButtons: function($node) {
            this._super(...arguments)
            if(this.$buttons.find('.container_last_updated_on')) {
                this.set_last_update_date()
            }
         },
         updateButtons() {
            this._super(...arguments)
            if(this.$buttons.find('.container_last_updated_on')) {
                this.set_last_update_date()
            }
        },
        set_last_update_date: function () {
            return this._rpc({
                model: this.modelName,
                method: 'search_read',
                args: [[], ['write_date']],
                kwargs: {
                    limit: 1,
                },
            }).then((result) => {
                if (result.length > 0) {
                    var write_date = new Date(result[0].write_date)
                    write_date = new Date(write_date.setMinutes(write_date.getMinutes() - write_date.getTimezoneOffset()))
                    if (result.length) {
                        this.$buttons.find('.container_last_updated_on').removeClass('d-none')
                        this.$buttons.find('.container_last_updated_date').text(write_date.toLocaleString(ulang))
                    } else {
                        this.$buttons.find('.container_last_updated_on').addClass('d-none')
                    }
                }
            })
        },
    })
})
