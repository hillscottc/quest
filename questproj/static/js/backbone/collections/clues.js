var app = app || {};

app.Clues = Backbone.Collection.extend({

    model: app.Clue,

    url: '/api/v1/random_clues/',

    search: function(letters) {
        if(letters == "") return this;

        var pattern = new RegExp(letters,"gi");
        return _(this.filter(function(data) {
            return pattern.test(data.get("question"));
        }));
    }

});
