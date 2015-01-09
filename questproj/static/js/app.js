var app = app || {};

$(function() {
    new app.CluesView();

    new app.StatsView(new app.Stats());
});

