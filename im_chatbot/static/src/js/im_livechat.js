odoo.define('im_chatbot.im_livechat', function (require) {
"use strict";

require('bus.BusService');
var core = require('web.core');
var utils = require('web.utils');
var session = require('web.session');

var WebsiteLivechatWindow = require('im_livechat.WebsiteLivechatWindow');

// ChatBot Extension
var LivechatButton = require('im_livechat.im_livechat').LivechatButton;

var _t = core._t;


LivechatButton.include({
    /**
     * @private
     * @param {OdooEvent} ev
     * @param {Object} ev.data.messageData
     */
    _onPostMessageChatWindow: function (ev) {
        ev.stopPropagation();
        var self = this;
        var messageData = ev.data.messageData;
        // Ivastanin
        this._sendMessage(messageData).then(function () {
        		//chatbot response
            	self._chatbotResponse(messageData).fail(function (error, e) {
                    e.preventDefault();
                    return self._chatbotResponse(messageData);
                }
            );
            }).fail(function (error, e) {
                e.preventDefault();
                return self.send_message(messageData).then(function () { // try again just in case
            		//chatbot response
                	self._chatbotResponse(messageData).fail(function (error, e) {
                        e.preventDefault();
                        return self._chatbotResponse(messageData);
                    })
                });
            });
    },

    _chatbotResponse: function (message) {
        var self = this;
        var cookie = utils.get_cookie('im_livechat_session');
        var channel = JSON.parse(cookie);
        return session
            .rpc("/mail/chatbot_post", {uuid: channel.uuid, message_content: message.content, channel_id: this.options.channel_id})
            .then(function () {
                self._chatWindow.thread.scroll_to();
            });
    },

});

return {
    LivechatButton: LivechatButton,
};

});