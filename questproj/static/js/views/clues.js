var app = app || {};

app.CluesView = Backbone.View.extend({

    el: '#clues',

    initialize: function( initialClues ) {
        this.collection = new app.Clues( initialClues );
        this.collection.fetch({reset: true});
        this.model = new app.Stats();
        this.render();
        this.listenTo( this.collection, 'add', this.renderClue );
        this.listenTo( this.collection, 'reset', this.render );
        //this.listenTo(Backbone, 'change:rights', this.rightsChange);
    },

    //rightsChange: function() {
    //  console.log("heard rights change")
    //},

    //events:{
    //    'click #add':'addClue'
    //},
    //
    //addClue: function( e ) {
    //    e.preventDefault();
    //    var formData = {};
    //    $( '#addClue div' ).children( 'input' ).each( function( i, el ) {
    //        if( $( el ).val() != '' ) { formData[ el.id ] = $( el ).val(); }
    //        $( el ).val('');
    //    });
    //    this.collection.create( formData );
    //},

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