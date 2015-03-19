var Backbone = require("backbone");
var $ = require('jquery');
Backbone.$ = $;
require('../lib/backbone-tastypie');

var CluesView = require('./views/clues');

var UserProfile = require('./models/user_profile');
var UserView = require('./views/user');



$(function() {
    new CluesView();

    var user_profile = new UserProfile({id: 1});

    new UserView({model: user_profile});
});


$(document).on({
    ajaxStart: function() { $('body').addClass("loading"); },
    ajaxStop: function() { $('body').removeClass("loading"); }
});