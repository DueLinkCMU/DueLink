$(document).ready(function() {
    $('#calendar').fullCalendar({

        defaultDate: moment().format("YYYY-MM-DD"),
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: {
        url: '/duelink/get_schedule/',
            error: function() {
            $('#script-warning').show();
        }
    },
    loading: function(bool) {
        $('#loading').toggle(bool);
    }
});

});/**
 * Created by pimengfu on 11/7/15.
 */

function get_schedule(){

}