odoo.define('zoom_integration.HideArchive', function (require) {
"use strict";
var session = require('web.session');
var BasicView = require('web.BasicView');
BasicView.include({
        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);

            var model = self.controllerParams.modelName in ['calendar.event'] ? 'True' : 'False';
            if(model) {
                        self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;

            }
        },
});
});
