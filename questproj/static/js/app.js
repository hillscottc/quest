var app = app || {};

$(function() {
    new app.CluesView();
    var stats = new app.Stats();
    new app.StatsView(stats);
});

