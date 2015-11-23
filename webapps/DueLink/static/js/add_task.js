/**
 * Created by changyilong on 11/22/15.
 */

function addTask() {
    var div = $(event.target).parent().prev();
    var taskForm = div.parent();
    var eventID = div.val();
    $.post('/duelink/add_task', taskForm.serialize()).done(
        function (data) {
            if (data.type == 'task') { // Comment success, return the new comment
                taskForm.parent().before(data.html);
                var len = $('div[id^=task_]').length;
                taskForm.parent().prev().prev().find('h3').html("Task "+len);
                // Clear the text area
                var taskText = taskForm.find('[name="description"]');
                taskText.val("");
               $('#progress').attr('aria-valuenow',data.progress)
                .attr('style',"width:"+data.progress+"%")
                .html(data.progress+"% complete");
            }else{
                //to-jie pan
            }
        });
}

function updateTask() {
    var task_id = $(event.target).prev().val();
    $.post('/duelink/update_task/'+task_id).done(
        function (data) {
            //$('#task_'+task_id).
            if (data.type == 'task') { // Comment success, return the new comment
                $('#task_status_'+task_id).html($(data.html).find("#task_status_"+task_id).html());
               $('#progress').attr('aria-valuenow',data.progress)
                .attr('style',"width:"+data.progress+"%")
                .html(data.progress+"% complete");
            }else{
                //to-jie pan
            }
        });
}

$(document).ready(function () {
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