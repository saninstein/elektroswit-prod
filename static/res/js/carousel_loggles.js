/**
 * Created by шаша on 18.07.2016.
 */
var key = 'new';
$(document).ready(function(){
    $('.btn-new').click(function(){
    key = 'new';
    switcher();
});

$('.btn-popular').click(function(){
    key = 'pop';
    switcher();
});
});

function switcher(){
  if(key == 'new'){
      $('#pop').hide();
      $('#news').show();
      $('.btn-popular').css('background-color', 'white');
      $('.btn-new').css('background-color', '#ffd506');
  } else if(key == 'pop'){
      $('#news').hide();
      $('#pop').show();
      $('.btn-new').css('background-color', 'white');
      $('.btn-popular').css('background-color', '#ffd506');
  }
};