var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .show-answer': 'showAnswer'
    },

    showAnswer: function() {
        //console.log("ok " + $(this).attr("className"));
        ans_id = this.model.attributes['id'];
        $("#ans_" + ans_id).toggle();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});