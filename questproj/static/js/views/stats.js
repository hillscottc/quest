var app = app || {};

app.StatsView = Backbone.View.extend({
    tagName: 'div',
    className: 'container stats',
    el: '#stats',

    initialize: function() {
        console.log("Initialized.")
    }

    //// render by rendering each item in the collection
    //render: function() {
    //    this.collection.each(function( item ) {
    //        this.renderClue( item );
    //    }, this );
    //},

});