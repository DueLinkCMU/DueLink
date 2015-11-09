function convertTextToUTCDate(str) {
    //refer to http://stackoverflow.com/questions/10181649/convert-iso-timestamp-to-date-format-with-javascript
    date = new Date(str);
    var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);

    var offset = date.getTimezoneOffset() / 60;
    var hours = date.getHours();

    newDate.setHours(hours + offset);
    return newDate.toISOString();
}

function get_date() {
    var dl_date = $("#datePicker");
    return dl_date.val();
}

function get_time() {
    $('#timePicker').timepicker('getTime', new Date());
    var dl_time = $('#timePicker');
    return dl_time.val();
}

function send_form() {
    var dl_date = get_date();
    var dl_time = get_time();
    var dl_name = $('#id_name').val();
    var dl_course = $('#id_course').val();
    var date_time_draft = dl_date + " " + dl_time + "+00:00";
    var dl_datetime = convertTextToUTCDate(date_time_draft);

    console.log(dl_time);
    console.log(dl_date);
    console.log(dl_name);
    console.log(dl_course);
    console.log(convertTextToUTCDate(date_time_draft));

    $.post("add_event", {deadline_datetime: dl_datetime, name: dl_name, course: dl_course})
        .done(function() {
            alert("Success: new evnet added");
        })
        .fail(function(){
            alert("Fail to add new event");
        });
}



$(document).ready(function () {
    $('#timePicker').timepicker();
    $('#timePicker').timepicker("setTime", Date.now());
    $('#datePicker').datepicker();
    $('#datePicker').datepicker('update', new Date(Date.now()));
    $('#testdate').click(get_date);
    $('#testtime').click(get_time);
    $('#submit_request').click(send_form);

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
