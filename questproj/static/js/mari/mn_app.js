'use strict';
var Backbone = require("backbone");
Backbone.$ = require("jquery");
var Marionette = require("backbone.marionette");

var app = new Marionette.Application();


var AppView = Backbone.Marionette.LayoutView.extend({
  template: "#clues-view",

  regions: {
    menu: "#clues-list-controls",
    content: "#clues-list"
  }
});

app.appView = new AppView();


app.on('start', function () {
	Backbone.history.start();
});
