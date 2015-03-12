var Backbone = require("backbone");
var $ = require('jquery');
Backbone.$ = $;
require('../lib/backbone-tastypie');

require('./models/clue');
require('./collections/clues');
require('./views/clue');

var CluesView = require('./views/clues');

$(function() {

    //app.vent = _.extend({}, Backbone.Events);
    //new app.CluesView({vent: app.vent});

    new CluesView();

});