/**
 * Created by changyilong on 11/21/15.
 */


function searchPeople() {
    var searchTerm = $("#search-people-field").val();
    $.get("search_people/" + searchTerm, function (data) {
    })
        .done(function () {
            console.log(data.get());
        })
        .fail(function () {
            alert("fail");
        })

}


$(document).ready(function () {
    // Add event-handler
    $("#search-people-btn").click(function (e) {
        e.preventDefault();
        searchPeople();
    });
    $("#search-people-field").keypress(function (e) {
        if (e.which == 13) addItem();
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