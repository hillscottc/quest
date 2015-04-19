
$(function () {

    // Init the timer
    $('#timer').countdown({format: 'mS',
        // expiryText: '<div class="timesup">Time is up!</div>',
        onExpiry: liftOff
    });

    // Disable the pause
    $('#timerPause').prop("disabled", true);

});

$('#timerGo').click(function() {

    // Enable the pause
    $('#timerPause').prop("disabled", false);

    var startTime = new Date();
    var secs = parseInt($('#timerChoice').val());
    startTime.setSeconds(startTime.getSeconds() + secs);
    $('#timer').countdown('option', {until: startTime});
});

$('#timerPause').click(function() {

    var pause = $(this).text() === 'pause';
    $(this).text(pause ? 'resume' : 'pause');
    $('#timer').countdown(pause ? 'pause' : 'resume');

});

function liftOff() {
    console.log('The time is up!');
    $('#timerPause').prop("disabled", true);
}

