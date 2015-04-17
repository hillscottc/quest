
// Init the timer
$(function () {
    $('#timer').countdown({format: 'mS',
        // expiryText: '<div class="timesup">Time is up!</div>',
        onExpiry: liftOff
    });
});

$('#timerGo').click(function() {
    var startTime = new Date();
    var secs = parseInt($('#timerChoice').val());
    startTime.setSeconds(startTime.getSeconds() + secs);
    $('#timer').countdown('option', {until: startTime});
});

function liftOff() {
    console.log('Do something!!!');
}

