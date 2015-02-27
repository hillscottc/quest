var Backbone = require("backbone");
var _ = require('underscore');


var ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .clue': 'clueClick',
        'click .tellme-btn': 'tellmeClick',
        'input .guess-text' : 'guessChange',
        'propertychange .guess-text' : 'guessChange' // for IE
    },

    initialize: function(options) {
        this.model = options.model;
        this.vent = options.vent;
    },

    // Fuzzy matching of guess to answer.
    fuzzyMatch: function(guess, answer) {
        if (guess == "") return false;
        if (answer == guess) return true;

        var guess_re = new RegExp(guess, "gi");

        if (guess.length > 3 && guess_re.test(answer)) {
            return true;
        }

    },

    // Live checking if guess is correct.
    guessChange: function() {
        var answer = this.model.attributes['answer'];
        var results_el = this.$('.results');
        var guess_el = this.$('.guess-text');

        if (this.fuzzyMatch(guess_el.val(), answer)) {
            results_el.text("Right!");
            guess_el.val(answer);

            // Disable further edit
            guess_el.prop("readonly", true);

            this.vent.trigger("guessRight");
        } else {
            results_el.text("");
        }
    },

    // Show the answer.
    tellmeClick: function(e) {
        var guess_el = this.$('.guess-text');
        var answer = this.model.attributes['answer'];
        guess_el.val(answer);

        // For debugging, allow this
        // Disable further edit
        //guess_el.prop("readonly", true);

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
            controls_el.find(".guess-text").focus();
        }
        e.preventDefault();
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});

module.exports = ClueView;



