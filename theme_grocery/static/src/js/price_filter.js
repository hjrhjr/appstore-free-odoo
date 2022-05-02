odoo.define('theme_grocery.price_filter', function(require) {
"use strict";
    var sAnimations = require('website.content.snippets.animation');
    var core = require('web.core');
    var _t = core._t;


    sAnimations.registry.KzSelectedAttributes = sAnimations.Class.extend({
        selector: '.tp-selected-attributes',
        events: {
            'click .tp-attribute': '_onClickAttribute'
        },
        _onClickAttribute: function (ev) {
            const $form = $('.js_attributes');
            const type = $(ev.currentTarget).data('type');
            if (type === 'price') {
                $form.find('input[name=min_price]').remove();
                $form.find('input[name=max_price]').remove();
                const $input = $form.find('input[id=' + $(ev.currentTarget).data('id') + ']');
                $input.prop('checked', false);
                $form.submit();
            } else if (type === 'attribute') {
                const $input = $form.find('input[value=' + $(ev.currentTarget).data('id') + ']');
                $input.prop('checked', false);
                const $select = $form.find('option[value=' + $(ev.currentTarget).data('id') + ']').closest('select');
                $select.val('');
                $form.submit();
            } else if (type === 'brand') {
                const $input = $form.find('input[name=brand][value=' + $(ev.currentTarget).data('id') + ']');
                $input.prop('checked', false);
                $form.submit();
            } else if (type === 'item_location') {
                const $input = $form.find('input[name=item_location][value=' + $(ev.currentTarget).data('id') + ']');
                $input.prop('checked', false);
                $form.submit();
            }
        },
    });
    sAnimations.registry.KzPriceFilter = sAnimations.Class.extend({
        selector: '.tp-price-filter',
        events: {
            'change input.min_price': '_onChangePrice',
            'change input.max_price': '_onChangePrice',
            'click .apply': '_onClickApply',
        },
        start: function () {
            const $priceSlider = this.$('.tp-price-slider');
            $priceSlider.ionRangeSlider({
                skin: 'square',
                prettify_separator: ',',
                type: 'double',
                hide_from_to: true,
                onChange: ev => {
                    this.$('input.min_price').val(ev.from);
                    this.$('input.max_price').val(ev.to);
                    this.$('.tp-price-validate').text('');
                    this.$('.apply').removeClass('d-none');
                },
            });
            this.priceSlider = $priceSlider.data('ionRangeSlider');
            return this._super.apply(this, arguments);
        },
        _onChangePrice: function (ev) {
            ev.preventDefault();
            const minValue = this.$('input.min_price').val();
            const maxValue = this.$('input.max_price').val();

            if (isNaN(minValue) || isNaN(maxValue)) {
                this.$('.tp-price-validate').text(_t('Enter valid price value'));
                this.$('.apply').addClass('d-none');
                return false;
            }
            if (parseInt(minValue) > parseInt(maxValue)) {
                this.$('.tp-price-validate').text(_t('Max price should be greater than min price'));
                this.$('.apply').addClass('d-none');
                return false;
            }
            this.priceSlider.update({
                from: minValue,
                to: maxValue,
            });
            this.$('.tp-price-validate').text('');
            this.$('.apply').removeClass('d-none');
            return false;
        },
        _onClickApply: function (ev) {
            this.$('input[name=min_price]').remove();
            this.$('input[name=max_price]').remove();
            //theme Modify
            //Investigar para herencia de funciones javascript cambiar !== por <= o >= donde aplique
            if (this.priceSlider.result.from >= this.priceSlider.result.min) {
                this.$el.append($('<input>', {type: 'hidden', name:'min_price', value: this.priceSlider.result.from}));
            }
            if (this.priceSlider.result.to <= this.priceSlider.result.max) {
                this.$el.append($('<input>', {type: 'hidden', name:'max_price', value: this.priceSlider.result.to}));
            }
        },
    });
});