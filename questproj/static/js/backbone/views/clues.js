var app = app || {};

app.CluesView = Backbone.View.extend({

    el: '#clues',

    initialize: function( initialClues ) {
        this.collection = new app.Clues( initialClues );
        this.collection.fetch({reset: true});
        this.render();
        this.listenTo( this.collection, 'add', this.renderItem );
        this.listenTo( this.collection, 'reset', this.render );
    },

    // render by rendering each item in the collection
    render: function() {
        this.collection.each(function( item ) {
            this.renderItem( item );
        }, this );
    },

    renderItem: function( item ) {
        var clueView = new app.ClueView({
            model: item
        });
        this.$el.append( clueView.render().el );
    }
});