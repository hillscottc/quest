
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

//
//// Increment the number text display of given el.
//function incrementDisplay(num_el) {
//    var count = num_el.text();
//    num_el.text(++count);
//}


function checkGuess(clue_el) {
    var answer = clue_el.find('.hidden-answer').val();
    var questionid = clue_el.find('.hidden-questionid').val();
    var userid = $('#hidden-userid').val();
    var results_el = clue_el.find('.results');
    var guess_el = clue_el.find('.guess-text');

   if (fuzzyMatch(guess_el.val(), answer)) {
        results_el.text("Right!");
        guess_el.val(answer);
       if($('#scoring-mode').is(':checked')) {
           ajaxPost('/userlog/post',
               {'userid': userid, 'questionid': questionid, 'correct': true});
       }
       guess_el.prop("readonly", true);
    } else {
       if($('#scoring-mode').is(':checked')) {
           results_el.text("Sorry, no.");
           ajaxPost('/userlog/post',
               {'userid': userid, 'questionid': questionid, 'correct': false});
       }
    }
}

// Check guess click if in tracking mode.
$(".guess-btn").click(function(e) {
    checkGuess($(e.target).parent());
    e.preventDefault();
});


// Live checking if not scoring.
$(".guess-text").on('input', function() {
    if($('#scoring-mode').is(':checked') == false) {
        checkGuess($(this).parent());
    }
});


$("#scoring-mode").change(function() {
    if(this.checked) {
        $('.guess-btn').show();
    } else {
        $('.guess-btn').hide();
    }
});


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
