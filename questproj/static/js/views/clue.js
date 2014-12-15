var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .show-answer': 'showAnswer'
    },

    showAnswer: function(e) {
//        console.log("ok " + $(this).attr("className"));
//        console.log(this.model.attributes['id']);
        ans_id = this.model.attributes['id'];
        $("#ans_" + ans_id).toggle();
    },


//        $( '#addClue div' ).children( 'input' ).each( function( i, el ) {
//            if( $( el ).val() != '' )
//            {
//                formData[ el.id ] = $( el ).val();
//            }
//            // Clear input field value
//            $( el ).val('');
//        });


    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});