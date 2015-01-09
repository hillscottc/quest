var app = app || {};

app.StatsView = Backbone.View.extend({

    el: '#stats',

    template: _.template( $('#statsTemplate').html() ),

    initialize: function(stats) {
        this.model = stats;
        this.render();
        //this.listenTo( this.model, 'change', this.render );
        console.log("StatsView Initialized.");
    },


    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }

});