var Backbone = require("backbone");
var $ = require('jquery');
Backbone.$ = $;
require('../lib/backbone-tastypie');

var CluesView = require('./views/clues');

$(function() {
    new CluesView();
});


$(document).on({
    ajaxStart: function() { $('body').addClass("loading"); },
    ajaxStop: function() { $('body').removeClass("loading"); }
});