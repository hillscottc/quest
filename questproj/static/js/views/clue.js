var app = app || {};

app.ClueView = Backbone.View.extend({
    tagName: 'div',
    className: 'clueContainer',

    template: _.template( $('#clueTemplate').html() ),

    events: {
        'click .clue': 'clueClick',
        'click .guess-btn': 'guessClick',
        'click .tellme-btn': 'tellmeClick'
    },

    guessClick: function(e) {
        var targ_el = $(e.currentTarget);
        var guess_el = targ_el.siblings('.guess-text');
        var results_el = targ_el.siblings('.results');

        if (guess_el.val().toLowerCase() == this.model.attributes['answer'].toLocaleLowerCase()) {
            results_el.text("Right!");
        } else {
            results_el.text("Wrong!")
        }

    },

    tellmeClick: function(e) {
        var guess_el = $(e.currentTarget).siblings('.guess-text');
        guess_el.val(this.model.attributes['answer']);
        e.preventDefault();
    },

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



