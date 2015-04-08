
$(".clue").click(function(e) {
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
});


$(".tellme-btn").click(function(e) {
    var guess_el = $(e.currentTarget).siblings('.guess-text');
    var answer = $(e.currentTarget).siblings('.hidden-answer').val();
    guess_el.val(answer);

    // For debugging, allow this
    // Disable further edit
    //guess_el.prop("readonly", true);

    e.preventDefault();
});


function fuzzyMatch(guess, answer) {
    if (guess == "") return false;
    if (answer == guess) return true;

    var guess_re = new RegExp(guess, "gi");

    if (guess.length > 3 && guess_re.test(answer)) {
        return true;
    }

}


$(".guess-text").on('input', function() {
    var answer = $(this).siblings('.hidden-answer').val();
    var results_el = $(this).siblings('.results');
    var guess_el = $(this);

    if (fuzzyMatch(guess_el.val(), answer)) {
        results_el.text("Right!");
        guess_el.val(answer);

        // Disable further edit
        guess_el.prop("readonly", true);

        //this.vent.trigger("guessRight", this);
    } else {
        results_el.text("");
    }
});