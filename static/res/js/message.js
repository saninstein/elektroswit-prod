/**
 * Created by шаша on 24.07.2016.
 */

$(document).ready(function(){
   $(this).on('message', function () {
       var text = $.cookie('message');
       var type = $.cookie('message_type');
       if(type == 'bad'){
           $('#message').css({'border-color': '#ed5565'});
           $('#message-text').css({'color': '#ed5565'})
           text += ' ' + '<i class="fa fa-times" aria-hidden="true"></i>';

       } else{
           $('#message').css({'border-color': '#9ad717'});
           $('#message-text').css({'color': '#9ad717'})
           text += ' ' + '<i class="fa fa-check" aria-hidden="true"></i>';
       }
       $('#message-text').html(text);
       $('#message').slideDown();
       setTimeout(function(){
            $('#message').slideUp();

       }, 2500);
   });
});