odoo.define('theme_grocery.script', function (require) {
    "use strict";

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var wSaleUtils = require('website_sale.utils');
    var publicWidget = require('web.public.widget');
    var sAnimations = require('website.content.snippets.animation');
    var core = require('web.core');
    var _t = core._t;

    $(".home-slider .owl-carousel").owlCarousel({
        items:1,
        autoplay: false,
        loop: true,
        nav : true, 
        dots: true,
        autoplaySpeed : 500,
        navSpeed : 500,
        dotsSpeed : 500,
        autoplayHoverPause: true,
        margin:1,
    });
    $(".best-seller .owl-carousel").owlCarousel({
        loop: false,
        nav: false,
        dots: true,
        autoplay: false,
        autoplayHoverPause: true,
        margin: 30,
        responsive: {0: {items: 1}, 480: {items: 1}, 768: {items: 1}, 991: {items: 1}, 1200: {items: 1}}
    });
    $(".review-slider .owl-carousel").owlCarousel({
        loop: true,
        nav: false,
        dots: true,
        autoplay: 1500,
        autoplayHoverPause: true,
        margin: 30,
        responsive: {0: {items: 1}, 480: {items: 1}, 768: {items: 1}, 991: {items: 1}, 1200: {items: 1}}
    });
    $("#featured .owl-carousel, #latest .owl-carousel, #bestseller .owl-carousel").owlCarousel({
        loop: true,
        nav: false,
        dots: true,
        autoplay: 3000,
        autoplayHoverPause: true,
        margin: 15,
        responsive: {0: {items: 1}, 320: {items: 2}, 420: {items: 2}, 768: {items: 3}, 991: {items: 3}, 1200: {items: 4}}
    });
    $(".homepage-blogs .owl-carousel").owlCarousel({
        loop: true,
        nav: false,
        dots: true,
        autoplay: false,
        autoplayHoverPause: true,
        margin: 15,
        responsive: {0: {items: 1}, 480: {items: 2}, 768: {items: 2}, 991: {items: 3}, 1200: {items: 3}}
    });

    // Product hover show few button
    $("#products_grid .oe_product").mouseenter(function(){
        $(this).find(".hover-button").css({"display": "block"});
        $(this).find(".oe_product_image").css({"opacity": "0.2","transition": "1s"});
        $(this).find(".hover-button").addClass("hover-btn-anim");
    });
    $("#products_grid .oe_product").mouseleave(function(){
        $(this).find(".hover-button").css({"display": "none"});
        $(this).find(".oe_product_image").css({"opacity": "1", "transition": "1s"});
        $(this).find(".hover-button").removeClass("hover-btn-anim").css({"transition": "2s"});
    });

    // Shop category hide/show
    $('#products_grid_before').on('click', '.fa-angle-right.open_close_sub_category',function(){
        $(this).removeClass('fa-angle-right').addClass('fa-angle-down');
        $(this).parents('li').find('ul:first').show();
        $(this).parents('li').css("height", "auto");
    });
    $('#products_grid_before').on('click', '.fa-angle-down.open_close_sub_category',function(){
        $(this).removeClass('fa-angle-down').addClass('fa-angle-right');
        $(this).parent().find('ul:first').hide();
        $(this).parents('li').css("height", "28px");
    });

    // Toogle view filter component
    $('.view-apply-filter').click(function(){
        $(".filter_view").slideToggle('slow');
    });

    $('.open-filter').click(function(){
        if ($("#products_grid_before").hasClass('hidden-xs'))
            $("#products_grid_before").removeClass('hidden-xs').style({'display': 'none'});
        $("#products_grid_before").slideToggle('slow');
    });

    // Remove filter attribute value
    $(".att-remove-btn").click(function(){
        var value = $(this).attr("data-att-val-id");
        if(value){
            $("form.js_attributes input[value="+value+"]").removeAttr("checked");
            $("form.js_attributes input").closest("form").submit();
        }
    });

    // Product page rating
    // var $star_rating = $('.star-rating .fa');
    var SetRatingStar = function() {
        $('.star-rating').each(function(){
            var $star_rating = $(this).find('.fa');
            return $star_rating.each(function() {
                var avg = $star_rating.parent().find('input.rating-value').val() || '0';
                if (parseInt(avg) >= parseInt($(this).data('rating'))) {
                    return $(this).removeClass('fa-star-o').addClass('fa-star');
                } else {
                    return $(this).removeClass('fa-star').addClass('fa-star-o');
                }
            });
        });
    };
    SetRatingStar();

    if ($(window).width() < 767) {
        $(".main_menu").mCustomScrollbar({
            axis:"y", // horizontal scrollbar
            theme:"dark",
            scrollTo: $('.homepage.o_rtl').length ? "right" : "left"
        });
    }

    if ($('.homepage.o_rtl').length) {
        $('.owl-carousel').css('direction', 'ltr');
    }

    $(".hover-button .a-submit").click(function(){
        $(this).closest('form').submit();
    });


    publicWidget.registry.WebsiteSale.include({
        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
            _.each($dom_optional, function (elem) {
                $(elem).find('.js_quantity').text(value);
                productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
            });
            $input.data('update_change', true);

            this._rpc({
                route: "/shop/cart/update_json",
                params: {
                    line_id: line_id,
                    product_id: parseInt($input.data('product-id'), 10),
                    set_qty: value
                },
            }).then(function (data) {
                $input.data('update_change', false);
                var check_value = parseInt($input.val() || 0, 10);
                if (isNaN(check_value)) {
                    check_value = 1;
                }
                if (value !== check_value) {
                    $input.trigger('change');
                    return;
                }
                if (!data.cart_quantity) {
                    return window.location = '/shop/cart';
                }
                
                wSaleUtils.updateCartNavBar(data);
                $(".extend-section").first().before(data['farmaoffers_design.extend_table_cart']).end().remove();
                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);

                $("#my_cart").html(data.cart_quantity).hide().fadeIn(600);
                $(".price-minicart .price").html(data.cart_amount).hide().fadeIn(600);

                if (data.warning) {
                    var cart_alert = $('.oe_cart').parent().find('#data_warning');
                    if (cart_alert.length === 0) {
                        $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                    }
                    else {
                        cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                    }
                    $input.val(data.quantity);
                }
            });
        },
        _onModalSubmit: function (goToShop) {
            var productAndOptions = JSON.stringify(
                this.optionalProductsModal.getSelectedProducts()
            );
            ajax.post('/shop/cart/update_option', {
                product_and_options: productAndOptions
            }).then(function (data) {
                if (goToShop) {
                    var path = "/shop/cart";
                    window.location.pathname = path;
                }
                var res = JSON.parse(data);
                $("#my_cart").html(res.cart_quantity).hide().fadeIn(600);
                $(".price-minicart .price").html(res.cart_amount).hide().fadeIn(600);
            });
        },
    });

    sAnimations.registry.ProductWishlist.include({
        _addNewProducts: function ($el) {
            var self = this;
            var productID = $el.data('product-product-id');
            if ($el.hasClass('o_add_wishlist_dyn')) {
                productID = $el.parent().find('.product_id').val();
                if (!productID) { // case List View Variants
                    productID = $el.parent().find('input:checked').first().val();
                }
                productID = parseInt(productID, 10);
            }
            var $form = $el.closest('form');
            var templateId = $form.find('.product_template_id').val();
            // when adding from /shop instead of the product page, need another selector
            if (!templateId) {
                templateId = $el.data('product-template-id');
            }
            $el.prop("disabled", true).addClass('disabled');
            var productReady = this.selectOrCreateProduct(
                $el.closest('form'),
                productID,
                templateId,
                false
            );

            productReady.then(function (productId) {
                productId = parseInt(productId, 10);

                if (productId && !_.contains(self.wishlistProductIDs, productId)) {
                    return self._rpc({
                        route: '/shop/wishlist/add',
                        params: {
                            product_id: productId,
                        },
                    }).then(function () {
                        var $navButton = $('#my_wish');
                        self.wishlistProductIDs.push(productId);
                        self._updateWishlistView();
                        wSaleUtils.animateClone($navButton, $el.closest('form'), 25, 40);
                    }).guardedCatch(function () {
                        $el.prop("disabled", false).removeClass('disabled');
                    });
                }
            }).guardedCatch(function () {
                $el.prop("disabled", false).removeClass('disabled');
            });
        },
        _addOrMoveWish: function (e) {
            var $navButton = $('#my_cart');
            var tr = $(e.currentTarget).parents('tr');
            var product = tr.data('product-id');
            $('.o_wsale_my_cart').removeClass('d-none');
            wSaleUtils.animateClone($navButton, tr, 25, 40);

            if ($('#b2b_wish').is(':checked')) {
                return this._addToCart(product, tr.find('add_qty').val() || 1);
            } else {
                var adding_deffered = this._addToCart(product, tr.find('add_qty').val() || 1);
                this._removeWish(e, adding_deffered);
                return adding_deffered;
            }
        },
        _addToCart: function (productID, qty_id) {
            return this._rpc({
                route: "/shop/cart/update_json",
                params: {
                    product_id: parseInt(productID, 10),
                    add_qty: parseInt(qty_id, 10),
                    display: false,
                },
            }).then(function (resp) {
                if (resp.warning) {
                    if (! $('#data_warning').length) {
                        $('.wishlist-section').prepend('<div class="mt16 alert alert-danger alert-dismissable" role="alert" id="data_warning"></div>');
                    }
                    var cart_alert = $('.wishlist-section').parent().find('#data_warning');
                    cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + resp.warning);
                }
                $('.my_cart_quantity').html(resp.cart_quantity || '<i class="fa fa-warning" /> ');
                $(".price-minicart .price").html(resp.cart_amount).hide().fadeIn(600);
            });
        },
    });

});
