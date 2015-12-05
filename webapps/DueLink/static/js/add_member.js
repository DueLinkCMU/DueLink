/**
 * Created by pimengfu on 12/4/15.
 */
function add_member() {
    var member = $('#id_member').val();
    var team_id = $('#team_id').val();
    $.post("/duelink/add_member/"+team_id,{'member':member})
        .done(function() {
            alert("Success: new member added");
            document.location.href = "/duelink/get_team_stream/"+team_id;

        })
        .fail(function(){
            alert("Fail to add new member");
        });
}

$(document).ready(function () {
    $('#add_member').click(function() {add_member()});
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