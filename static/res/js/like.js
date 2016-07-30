/**
 * Created by шаша on 18.07.2016.
 */
$(document).ready(function(){
    if($.cookie('liked')){
        $('.fa-heart').css("color", "#ffd506");
    }
    $('.fa-heart').mouseover(function(){
        $('.fa-heart').css("color", "#ffd506");
    });
    $('.fa-heart').mouseout(function(){
        if($.cookie('liked')){
            $('.fa-heart').css("color", "#ffd506");
        } else{
            $('.fa-heart').css("color", "#BBBBBB");
        }
    });
    $('.fa-heart').click(function(){
        if(!$.cookie('liked')){
            $.cookie('liked', "true", {
                expires: 100
            });
            $.get('/ajax_like/' + $('#buy').data('item') + '/');
        }


    });
});

