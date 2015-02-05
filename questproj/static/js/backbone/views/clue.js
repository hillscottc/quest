var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .clue': 'clueClick',
        'click .tellme-btn': 'tellmeClick',
        'keyup .guess-text' : 'guessChange'
    },

   // Live checking if guess is correct.
   guessChange: function() {
        var guess_el = this.$('.guess-text');
        var results_el = this.$('.results');

        // If answer is correct
        if (guess_el.val().toLowerCase() == this.model.attributes['answer'].toLocaleLowerCase()) {
            results_el.text("Right!");
        } else {
            results_el.text("");
        }
    },

    // Give the answer.
    tellmeClick: function(e) {
        var guess_el = this.$('.guess-text');
        guess_el.val(this.model.attributes['answer']);
        e.preventDefault();
    },

    // Highlight the current clue.
    clueClick: function(e) {
        var targ_el = $(e.currentTarget);
        var controls_el = $(e.currentTarget).siblings('.clue-controls');

        if (targ_el.hasClass("active")) {
            targ_el.removeClass("active");
            controls_el.toggle(false)
        } else {
            targ_el.addClass("active");
            controls_el.toggle(true)
        }
        e.preventDefault();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});



