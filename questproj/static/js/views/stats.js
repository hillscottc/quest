var app = app || {};

app.StatsView = Backbone.View.extend({

    el: '#stats',

    template: _.template( $('#statsTemplate').html() ),

    initialize: function() {
        this.model = new app.Stats();
        console.log("StatsView Initialized.")
        this.render();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }

});