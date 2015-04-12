
// Ajax-post a data dictionary.
function ajaxPost(url, data){
    var json_data =  JSON.stringify(data);
    var request = $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: json_data,
        dataType: 'text',
        success: function(result) {
            console.log("Posted " + json_data + ", to " + url + ", got " + request['statusText']);
        }
    });
}

// True if args match, according to rules.
function fuzzyMatch(guess, answer) {
    if (guess == "") return false;
    if (answer == guess) return true;

    var guess_re = new RegExp(guess, "gi");

    if (guess.length > 3 && guess_re.test(answer)) {
        return true;
    }
}


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

    // Disable further edit.
    guess_el.prop("readonly", true);

    // Only can click it once. Disable it.
    $(e.currentTarget).prop("disabled", true);

    // And disable the guess button
    $(e.currentTarget).siblings('.guess-btn').prop("disabled", true);

    e.preventDefault();
});

// Check guess click if not in practice mode.
$(".guess-btn").click(function(e) {
    var answer = $(this).siblings('.hidden-answer').val();
    var questionid = $(this).siblings('.hidden-questionid').val();
    var userid = $('#hidden-userid').val();
    var results_el = $(this).siblings('.results');
    var guess_el = $(this).siblings('.guess-text');

    if (fuzzyMatch(guess_el.val(), answer)) {
        results_el.text("Right!");
        guess_el.val(answer);

        // Post to the log
        var data = {'userid': userid, 'questionid': questionid};
        ajaxPost('/userlog/post', data);

        // Update user today display
        var count_el = $('#count-user-today');
        var count = count_el.text();
        count_el.text(++count);

        // Update user all display
        count_el = $('#count-user-all');
        count = count_el.text();
        count_el.text(++count);

        // Disable further edit
        guess_el.prop("readonly", true);

    } else {
        results_el.text("Sorry, no.");
    }

    e.preventDefault();
});

// Live checking if not scoring.
$(".guess-text").on('input', function() {

    if($('#scoring-mode').is(':checked')) {
        return;
    }

    var answer = $(this).siblings('.hidden-answer').val();
    var questionid = $(this).siblings('.hidden-questionid').val();
    var userid = $('#hidden-userid').val();
    var results_el = $(this).siblings('.results');

    if (fuzzyMatch($(this).val(), answer)) {
        results_el.text("Right!");
        $(this).val(answer);

        // Post to the log
        var data = {'userid': userid, 'questionid': questionid};
        ajaxPost('/userlog/post', data);

        // Update user today display
        var count_el = $('#count-user-today');
        var count = count_el.text();
        count_el.text(++count);

        // Update user all display
        count_el = $('#count-user-all');
        count = count_el.text();
        count_el.text(++count);

        // Disable further edit
        $(this).prop("readonly", true);

    } else {
        results_el.text("");
    }
});


$("#scoring-mode").change(function() {
    if(this.checked) {
        $('.guess-btn').show();
        $('#counts').show();
    } else {
        $('.guess-btn').hide();
        $('#counts').hide();
    }
});