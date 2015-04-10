
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

    // For debugging, allow this
    // Disable further edit
    //guess_el.prop("readonly", true);

    e.preventDefault();
});


$(".guess-text").on('input', function() {
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

        // Update user counts display
        var count_el = $('#count-user-today');
        var count = count_el.text();
        count_el.text(++count);

        count_el = $('#count-user-all');
        count = count_el.text();
        count_el.text(++count);

        // Disable further edit
        $(this).prop("readonly", true);

    } else {
        results_el.text("");
    }
});


