function parseDate(str) {
    return moment(str).utc().format();
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
    var m_d_y = dl_date.split("/");
    var year = m_d_y[2];
    var month = m_d_y[0];
    var day = m_d_y[1];
    var dl_time = get_time() + ":00";
    var dl_name = $('#id_name').val();
    var dl_course = $('#id_course').val();
    var date_time_draft = year + "-" + month + "-" + day + " " + dl_time;
    var dl_datetime = moment(date_time_draft).toISOString();
    $.post("add_event", {deadline_datetime: dl_datetime, name: dl_name, course: dl_course})
        .done(function() {
            alert("Success: new evnet added");
            document.location.href = "home";

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
    $('#submit_request').click(function() {send_form()});
    //$('.button').on('click', send_form);

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

    //load course
    loadCourse();
});
