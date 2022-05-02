odoo.define('server_info.auto_update', function (require) {
    "use strict";

    var session = require('web.session');
    var Widget = require('web.Widget');
    var widget_registry = require('web.widget_registry');

    var AutoUpdate = Widget.extend({
        template: 'auto_update',
        xmlDependencies: ['/server_info/static/xml/auto_update.xml'],

        init: function () {
            this._super.apply(this, arguments);
            this.auto_update_interval = null;
            this.interval = session.interval || 5000;
        },

        start: function () {
            var self = this;
            return this._super.apply(arguments).then(function(){
                setTimeout(function(){
                    self._update_fields(session);
                }, 500);
                self.auto_update_interval = self._get_interval(self, self.interval);
            });
        },

        destroy: function () {
            clearInterval(this.auto_update_interval);
        },

        _change_interval: function (widget, interval){
            /*
             * Swap interval for new if interval in settings is changed
             */
            if (interval != widget.interval && !isNaN(interval) && interval != null)
            {
                clearInterval(widget.auto_update_interval);
                widget.interval = interval;
                widget.auto_update_interval = widget._get_interval(widget, interval);
                return true;
            }
            return false;
        },

        _get_interval: function (widget, interval) {
            /*
             * Returns new interval
             */
            return setInterval(function (){
                widget._getCpuUsage().then(function (response){
                    widget._update_fields(response);
                    widget._change_interval(widget, response.interval);
                });
            }, interval);
        },

        _update_fields: function (response) {
            /*
             * Put values from response to corresponding elements in template
             */
            self.$('[name="cpu_usage"]').text(response.cpu_usage);
            self.$('[name="cpu_count"]').text(response.cpu_count);

            self.$('[name="mem_total"]').text(response.mem_total);
            self.$('[name="mem_used"]').text(response.mem_used);
            self.$('[name="mem_used_percent"]').text(response.mem_used_percent);
            self.$('[name="mem_free"]').text(response.mem_free);

            self.$('[name="disk_mem_total"]').text(response.disk_mem_total);
            self.$('[name="disk_mem_used"]').text(response.disk_mem_used);
            self.$('[name="disk_mem_used_percent"]').text(response.disk_mem_used_percent);
            self.$('[name="disk_mem_free"]').text(response.disk_mem_free);
        },

        _getCpuUsage: function () {
            return this._rpc({
                model: 'ir.http',
                method: 'session_info',
                args:[session.uid]
            });
        },
    });

    widget_registry.add('auto_update', AutoUpdate);

    return AutoUpdate;
});
