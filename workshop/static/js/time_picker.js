$(document).ready(function () {
    $('.timepicker').timepicker({
        timeFormat: 'H:mm',
        interval: 30,
        minTime: '00:00',
        maxTime: '23:59',
        defaultTime: '12:00',
        startTime: '00:00',
        dynamic: false,
        dropdown: true,
        scrollbar: false
    });
});