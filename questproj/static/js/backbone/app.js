var Backbone = require("backbone");
var $ = require('jquery');
Backbone.$ = $;
require('../../lib/backbone-tastypie');

require('./models/clue.js');
require('./collections/clues.js');
require('./views/clue.js');
var CluesView = require('./views/clues.js');

var app = app || {};

$(function() {

    //app.vent = _.extend({}, Backbone.Events);
    //new app.CluesView({vent: app.vent});

    new CluesView();

});

