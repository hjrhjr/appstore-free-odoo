odoo.define('elearning_private_youtube_video.fullscreen', function (require) {
"use strict";

var core = require('web.core');
var QWeb = core.qweb;
var Fullscreen = require('website_slides.fullscreen');
var VideoPlayer = require('website_slides.fullscreen');
Fullscreen.include({
    xmlDependencies: (Fullscreen.prototype.xmlDependencies || []).concat(
        ["/elearning_private_youtube_video/static/website_slides_fullscreen.xml"]
    ),
      init: function (parent, slides, defaultSlideId, channelData){
            var result = this._super.apply(this,arguments);
            return result;
        },

});

});