$(document).ready(function() {
    get_schedule(function(events){
        $('#calendar').fullCalendar({

        defaultDate: moment().format("YYYY-MM-DD"),
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: events,
    loading: function(bool) {
        $('#loading').toggle(bool);
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