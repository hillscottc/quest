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
        var stats_el = $('#stats');

        if (guess_el.val().toLowerCase() == this.model.attributes['answer'].toLocaleLowerCase()) {
            results_el.text("Right!");
            var rights_el = stats_el.find('#rights');
            var old_rights = parseInt(rights_el.text());
            rights_el.text(old_rights + 1);
        } else {
            results_el.text("Wrong!")
            var wrongs_el = stats_el.find('#wrongs');
            var old_wrongs = parseInt(wrongs_el.text());
            wrongs_el.text(old_wrongs + 1);
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



