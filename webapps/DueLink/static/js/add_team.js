/**
 * Created by pimengfu on 12/4/15.
 */
function create_team() {
    var name = $('#id_name').val();
    var course = $('#id_course').val();
    $.post("add_team", {name: name , course: course})
        .done(function() {
            alert("Success: new team added");
           // document.location.href = "team_stream";

        })
        .fail(function(){
            alert("Fail to add new event");
        });
}

$(document).ready(function () {
    $('#submit_request').click(function() {create_team()});
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

});