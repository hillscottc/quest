var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .clue': 'showAnswer'
    },

    showAnswer: function(e) {
        console.log("ok " + $(this).attr("className"));
        var ans_id = this.model.attributes['id'];
        console.log(ans_id)
//        console.log($("#ans_" + ans_id).text);
//        $("#ans_" + ans_id).toggle();
        e.preventDefault();
    },

//        $( '#addClue div' ).children( 'input' ).each( function( i, el ) {
//            if( $( el ).val() != '' )
//            {
//                formData[ el.id ] = $( el ).val();
//            }
//            // Clear input field value
//            $( el ).val('');
//        });
//
//    <script type="text/javascript">
//        $(document).ready(function() {
//            $('.clue').click(function(e){
//                $(this).children('.answer').toggle();
//                if ($(this).hasClass("active")) {
//                    $(this).removeClass("active");
//                } else {
//                    $(this).addClass("active");
//                }
//                e.preventDefault(); // dont want href action
//            })
//        });
//    </script>


    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});