var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .clue': 'clueClick',
        'click .guess-btn': 'guessClick'
    },

    guessClick: function(e) {
        console.log("guess!");
    },

    clueClick: function(e) {
        // Set target el class to active and write to answer el.

        var targ_el = $(e.currentTarget);
        var ans_el = $(e.currentTarget).find('.answer');

        if (targ_el.hasClass("active")) {
            // Remove active class, erase answer text
            targ_el.removeClass("active");
            ans_el.text('');
        } else {
            // Add active class, write answer text
            targ_el.addClass("active");
            ans_el.text(this.model.attributes['answer']);
        }
        e.preventDefault();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});



