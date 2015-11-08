$(document).ready(function() {
         console.log($.datepicker.formatDate('yyyy-mm-dd', new Date()));
		$('#calendar').fullCalendar({

			defaultDate: $.datepicker.formatDate('yyyy-mm-dd', new Date()),
			editable: true,
			eventLimit: true, // allow "more" link when too many events
			events: {
                url: '/duelink/get_schedule/',
                error: function() {
					$('#script-warning').show();
				}
            },
            loading: function(bool) {
				$('#loading').toggle(bool);
			}
		});

	});/**
 * Created by pimengfu on 11/7/15.
 */

function get_schedule(){

}