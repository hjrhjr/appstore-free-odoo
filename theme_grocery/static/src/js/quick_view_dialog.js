odoo.define('theme_grocery.product_quick_view', function (require) {
'use strict';

    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;
    var ajax = require('web.ajax');
    var sAnimations = require('website.content.snippets.animation');
    require('website_sale.website_sale');


    sAnimations.registry.WebsiteSale.include({
        events: _.extend({}, sAnimations.registry.WebsiteSale.prototype.events || {}, {
            'click .p_quick_view, .tp-product-quick-view-small-btn' : 'onQuickView',
        }),
        onQuickView: function(event){
            var product_id = $(event.currentTarget).attr('data-product-id');
            $.blockUI({
                'message': '<h3 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/></h3>'
            });
            ajax.jsonRpc('/add/quick/views/popup', 'call', {
                product_id: parseInt(product_id),
            }).then(function(data) {
                $('.quick_view_pop_up_p_detail').html(data.data);
                $('.quick_view_pop_up_p_detail .js_main_product [data-attribute_exclusions]').trigger('change')
                $("#product_quick_views_popup").modal('show');
                $.unblockUI();
            });
        },
    });

});
