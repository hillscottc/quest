var app = app || {};

app.Clues = Backbone.Collection.extend({

    model: app.Clue,

    url: '/api/v1/random_clues/'

});
