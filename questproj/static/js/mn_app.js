'use strict';
var Backbone = require("backbone");
var Marionette = require("backbone.marionette");

window.MnApp = new Marionette.Application();

(function () {
  var filterState = new Backbone.Model({
    filter: 'all'
  });

  MnApp.reqres.setHandler('filterState', function () {
    return filterState;
  });
})();

MnApp.addRegions({
	header: '#header',
	main: '#main',
	footer: '#footer'
});

MnApp.on('start', function () {
	Backbone.history.start();
});
