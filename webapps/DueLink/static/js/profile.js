/**
 * Created by pimengfu on 11/22/15.
 */
/**
 * Created by changyilong on 11/22/15.
 */

function link(user_id) {
    var button_link = $(event.target);
    $.post('/duelink/link/' + user_id).done(
        function (data) {
            button_link.attr('onclick', 'unlink(' + user_id + ')')
                .html("Unlink");
        });
}

function unlink(user_id) {
    var button_link = $(event.target);
    $.post('/duelink/unlink/' + user_id).done(
        function (data) {
            button_link.attr('onclick', 'link(' + user_id + ')')
                .html("Link");
        });
}

function populate() {
    var course_table = $('#course-subscription-list');
    // Remove all children
    course_table.empty();
    var data = $.post('/duelink/display_user_course', {'skim': 1})
        .done(function (data) {
            for (var i = 0; i < data.courses.length; i++) {
                var tag = data.courses[i].html;
                course_table.append(tag);
            }
        })
        .fail(function (data) {
            alert("fail");
        })
}


$(document).ready(function () {
    // CSRF set-up copied from Django docs

    $('#course-modal-trigger').on('click', populate);


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