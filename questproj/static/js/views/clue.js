var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

//    template: _.template( $('#clueTemplate').html() ),

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});