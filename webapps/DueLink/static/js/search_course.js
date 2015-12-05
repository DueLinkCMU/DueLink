/**
 * Created by pimengfu on 12/3/15.
 */




void function(){
    $('#id_course').attr('data-placeholder','Choose a course')
        .attr('class','chosen-select')
        .attr('style','width: 420px;')
        .attr('tabindex',"1");
     if($('#team_id').length > 0){
        //is team
        $('#id_course').prop('disabled','disabled');
     }
}();


//function search_course(){
//
//    'use strict';
//    //var courses;
//    //$.get('/duelink/search_course').done(function (data){
//    //    courses = data;
//    //});
//    horsey(document.querySelector('#search_course'), {
//        suggestions: [
//            { value: 1, text: 'Bananas from Amazon Rainforest' },
//            { value: 2, text: 'Banana Boat' },
//            { value: 3, text: 'Red apples from New Zealand' },
//            { value: 4, text: 'Red apple cider beer' },
//            { value: 5, text: 'Oranges from Moscow' }
//        ],
//        limit: 2
//    });
//
//    function events (el, type, fn) {
//    if (el.addEventListener) {
//      el.addEventListener(type, fn);
//    } else if (el.attachEvent) {
//      el.attachEvent('on' + type, wrap(fn));
//    } else {
//      el['on' + type] = wrap(fn);
//    }
//    function wrap (originalEvent) {
//      var e = originalEvent || global.event;
//      e.target = e.target || e.srcElement;
//      e.preventDefault  = e.preventDefault  || function preventDefault () { e.returnValue = false; };
//      e.stopPropagation = e.stopPropagation || function stopPropagation () { e.cancelBubble = true; };
//      fn.call(el, e);
//    }
//  }
//}