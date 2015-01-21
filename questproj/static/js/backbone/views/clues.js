var app = app || {};

app.CluesView = Backbone.View.extend({

    el: '#clues',

    initialize: function( initialClues ) {
        this.collection = new app.Clues( initialClues );
        this.collection.fetch({reset: true});
        //this.model = new app.Stats();
        this.render();
        this.listenTo( this.collection, 'add', this.renderClue );
        this.listenTo( this.collection, 'reset', this.render );
        //this.listenTo(Backbone, 'change:rights', this.rightsChange);
    },

    // render by rendering each item in the collection
    render: function() {
        this.collection.each(function( item ) {
            this.renderClue( item );
        }, this );
    },

    renderClue: function( item ) {
        var clueView = new app.ClueView({
            model: item
        });
        this.$el.append( clueView.render().el );
    }
});