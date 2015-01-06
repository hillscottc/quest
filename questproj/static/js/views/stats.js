var app = app || {};

app.StatsView = Backbone.View.extend({

    template: _.template( $('#statsTemplate').html() )
});