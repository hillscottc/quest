var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .clue': 'clueClick',
        'click .tellme-btn': 'tellmeClick',
        'input .guess-text' : 'guessChange',
        'propertychange .guess-text' : 'guessChange' // for IE
    },

    // Live checking if guess is correct.
    guessChange: function() {
        var guess = this.$('.guess-text').val().toLowerCase();
        var answer = this.model.attributes['answer'].toLowerCase();
        var results_el = this.$('.results');

        if (guess == answer) {
            results_el.text("Right!");
        } else {
            results_el.text("");
        }
    },

    // Give the answer.
    tellmeClick: function(e) {
        var guess_el = this.$('.guess-text');
        var answer = this.model.attributes['answer'];
        guess_el.val(answer);
        e.preventDefault();
    },

    // Highlight the current clue.
    clueClick: function(e) {
        var targ_el = $(e.currentTarget);
        var controls_el = $(e.currentTarget).siblings('.clue-controls');

        if (targ_el.hasClass("active")) {
            targ_el.removeClass("active");
            controls_el.toggle(false);
        } else {
            targ_el.addClass("active");
            controls_el.toggle(true);
        }
        e.preventDefault();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});



