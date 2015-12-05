function populate() {
    var course_table = $('#course-subscription-list');
    // Remove all children
    course_table.empty();
    var data = $.get('/duelink/display_user_course')
        .done(function (data) {
            console.log(data.courses.length);
            console.log(data.courses[0].html);
            for (var i = 0; i < data.courses.length; i++) {
                course_table.append(data.courses[i].html);
            }
        })
        .fail(function (data) {
            alert("fail to populate data");
        })
}

function subscribe() {
    var course_id = $('#id_course').val();
    $.post('/duelink/subscribe_course', {'course': course_id})
        .done(function (data) {
            alert("Successfully subscribed course");
            var course_table = $('#course-subscription-list');
            for (var i = 0; i < data.courses.length; i++) {
                course_table.append(data.courses[i].html);
            }
        })
        .fail(function () {
            alert("Unable to subscribe course, duplicated or invalid.");
        });
}

function unsubscribe(target) {
    var trigger = target;
    var course_id = trigger.parent().attr('course_id');
    $.post('/duelink/unsubscribe_course', {'course_id': course_id})
        .done(function (data) {
            populate();
        })
        .fail(function (data) {
            alert("Fail to un-subscribe course");
        });
}


$(document).ready(function () {
    populate();
    $('#submit-subscribe-course').click (function (e) {
        e.preventDefault();
        subscribe();
    });

    $('#course-subscription-list').on('click', '.delete-trigger', function (e) {
        e.preventDefault();
        var target = $(event.target);
        $.confirm({
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            confirm: function () {
                unsubscribe(target);
            },
            cancel: function () {
                alert("Something wrong happened, please contact the admin");
            }
        });
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
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});