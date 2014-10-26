/**
 * Project common javascript.
 */

$(document).ready(function() {

    $('.answer').toggle();

    $('.show-answer').click(function(){
        $(this).children().toggle();
    })
});

