var app = app || {};

app.UserView = Backbone.View.extend({

    el: '#user-stats',
    template: _.template( $('#userTemplate').html() ),

    initialize: function( initialUser ) {
        this.model = initialUser
        this.render();
        //this.listenTo( this.collection, 'add', this.renderClue );
        //this.listenTo( this.collection, 'reset', this.render );
        //this.listenTo(Backbone, 'change:rights', this.rightsChange);
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }

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


});