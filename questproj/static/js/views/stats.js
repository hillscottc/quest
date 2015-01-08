var app = app || {};

app.StatsView = Backbone.View.extend({

    el: '#stats',

    template: _.template( $('#statsTemplate').html() ),

    initialize: function(stats) {
        this.model = stats;
        this.model
        this.render();
        console.log("StatsView Initialized.");
    },

    events: {
        "click .": "open"
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }

});