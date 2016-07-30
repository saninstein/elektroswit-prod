/**
 * Created by шаша on 22.07.2016.
 */
$(document).ready(function(){
    $('#slides img').click(function(){
        document.location.replace($(this).data('link'));
    });
});