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

    console.log(dl_time);
    console.log(dl_date);
    console.log(dl_name);
    console.log(dl_course);

    $.post("add_deadline", {deadline_date: dl_date, deadline_time: dl_time, deadline_name: dl_name, deadline_course: dl_course})
        .done(function() {
            alert("success");
        })
        .fail(function(){
            console.log("fail");
        });
}


$(document).ready(function () {
    $('#timePicker').timepicker();
    $('#datePicker').datepicker();
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
