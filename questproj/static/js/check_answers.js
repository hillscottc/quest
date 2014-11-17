
// unused, atm.

// answer item checking
$(document).ready(function() {


    // fill-in answer check when text changes
    $('.UL_answer').each(function() {
        var elem = $(this);
        var q_id = this.name.replace( /^\D+/g, '');
        // Save current value of element
        elem.data('oldVal', elem.val());
        // Look for changes in the value
        elem.bind("propertychange keyup input paste", function(event){
            // If value has changed...
            if (elem.data('oldVal') != elem.val()) {
                // Updated stored value
                elem.data('oldVal', elem.val());

                // Do action.
                var hid_elem = $('#ans_' + q_id + '_hid')
                var res_el = $("#result_" + q_id);
                // Erase if its blank.
                if (elem.val() == ''){
                    res_el.attr('class', '');
                    res_el.html("");
                    $("#hidden_" + q_id).val("");
                // If it's correct.
                } else if (elem.val().toLowerCase() == hid_elem.val().toLowerCase()) {
                    res_el.attr('class', 'alert alert-success');
                    res_el.html("Correct!");
                    $("#hidden_" + q_id).val("CORRECT");
                    checkAnswers();
                // Its wrong.
                } else {
                    res_el.attr('class', 'alert alert-danger');
                    res_el.html("Wrong.");
                    $("#hidden_" + q_id).val("Wrong.");
                }
            }
        });
    });
});

