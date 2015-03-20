var Backbone = require("backbone");
var $ = require('jquery');
Backbone.$ = $;
require('../lib/backbone-tastypie');

var CluesView = require('./views/clues');

var UserProfile = require('./models/user_profile');
var UserView = require('./views/user');



$(function() {

    // TODO: Dont specify a default, get logged in user.
    var user_profile = new UserProfile({id: 1});

    // Must wait for the fetch to complete before passing it on.
    user_profile.fetch().then(function(){
        new UserView({model: user_profile});
    });

    new CluesView();

});


$(document).on({
    ajaxStart: function() { $('body').addClass("loading"); },
    ajaxStop: function() { $('body').removeClass("loading"); }
});