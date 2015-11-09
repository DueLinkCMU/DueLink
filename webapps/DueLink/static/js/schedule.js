$(document).ready(function() {
    get_schedule(function(events){
        $('#calendar').fullCalendar({

            defaultDate: moment().format("YYYY-MM-DD"),
            editable: true,
            eventLimit: true, // allow "more" link when too many events
            events: events
        });


        // CSRF set-up copied from Django docs
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    });

});/**
 * Created by pimengfu on 11/7/15.
 */

function get_schedule(callback){
    $.get('/duelink/get_schedule/').done(function (data){
        console.log("asd");
        var events = data.events;
        for (var i = 0; i < events.length; i++) {
            events[i].start = convertUTCDateToLocalDate(events[i].start); //change data format
        }
        callback(events);
    });
}

function convertUTCDateToLocalDate(str) {
    //refer to http://stackoverflow.com/questions/10181649/convert-iso-timestamp-to-date-format-with-javascript
    date = new Date(str);
    var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);

    var offset = date.getTimezoneOffset() / 60;
    var hours = date.getHours();

    newDate.setHours(hours - offset);
    return newDate.toISOString();
}