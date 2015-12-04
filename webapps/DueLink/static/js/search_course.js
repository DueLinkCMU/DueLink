/**
 * Created by pimengfu on 12/3/15.
 */
function loadCourse(){
    var courses;
    $.get('/duelink/search_course/').done(function (data){
        courses = data;
    });
    horsey(document.querySelector('#search_course'), {
        suggestions: [
            { value: 'banana', text: 'Bananas from Amazon Rainforest' },
            { value: 'banana-boat', text: 'Banana Boat' },
            { value: 'apple', text: 'Red apples from New Zealand' },
            { value: 'apple-cider', text: 'Red apple cider beer' },
            { value: 'orange', text: 'Oranges from Moscow' },
            { value: 'orange-vodka', text: 'Classic orange vodka cocktail' },
            { value: 'lemon', text: 'Juicy lemons from Amalfitan Coast' }
        ]
    });
}