var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .show-answer': 'showAnswer'
    },

    showAnswer: function() {
//        console.log("ok " + $(this).attr("className"));
//        console.log(this.model.attributes['id']);
        $("#ans_" + this.model.attributes['id']).toggle();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});