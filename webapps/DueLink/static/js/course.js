function populate() {
    var course_table = $('#course-list-modal');
    // Remove all children
    course_table.empty();
    var data = $.get('/duelink/display_user_course')
        .done(function (data) {
            console.log(data.courses.length);
            console.log(data.courses[0]);
            for (var i = 0; i < data.courses.length; i++) {
                var new_li = $('<li>');
                new_li.text(data.courses[i].course_name + " " + data.courses[i].course_section);
                course_table.append(new_li);
            }
        })
        .fail(function (data) {
            alert("fail");
        })
}


$(document).ready(function () {
    //populate();
    $('#course-modal-trigger').on('click', populate);
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
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});