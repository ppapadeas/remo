$(document).ready(function () {
    $('#dashboard-mozillians-reps-grid-button').click(function () {
        $('#dashboard-mozillians-reps-grid-block').show('fast');
        $('#dashboard-mozillians-reps-reports-block').hide('fast');

        $(this).parent().addClass('active');
        $('#dashboard-mozillians-reps-reports-button').parent().removeClass('active');
    });

    $('#dashboard-mozillians-reps-reports-button').click(function () {
        $('#dashboard-mozillians-reps-reports-block').show('fast');
        $('#dashboard-mozillians-reps-grid-block').hide('fast');

        $(this).parent().addClass('active');
        $('#dashboard-mozillians-reps-grid-button').parent().removeClass('active');
    });

    $('#dashboard-events-future-button').click(function () {
        $('#dashboard-events-future-block').show('fast');
        $('#dashboard-events-past-block').hide('fast');

        $(this).parent().addClass('active');
        $('#dashboard-events-past-button').parent().removeClass('active');
    });

    $('#dashboard-events-past-button').click(function () {
        $('#dashboard-events-past-block').show('fast');
        $('#dashboard-events-future-block').hide('fast');

        $(this).parent().addClass('active');
        $('#dashboard-events-future-button').parent().removeClass('active');
    });



    $('table').each(function(index, item) { $(item).stupidtable(); });
    // Apply prettyDate on all elements with data-time attribute.
    $('*').find('*[data-time]').prettyDate({attribute:'data-time', interval: 60000, isUTC:true});
});
