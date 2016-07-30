/**
 * Created by шаша on 24.07.2016.
 */
var first;
var second;
var discount;
var val;
$(document).ready(function () {
    $('input[type=submit]').click(function(){
        discount = $('#discount').val();
        if(!first || !second){
            $.cookie('message', 'Товар не выбран');
            $.cookie('message_type', 'bad');
            $(document).trigger('message');
            return false;
        }
        if(!discount){
            $.cookie('message', 'Введите скидку');
            $.cookie('message_type', 'bad');
            $(document).trigger('message');
            return false;
        }
        $.post(
            '/adminpanel/add_share/',
            {
                first: first,
                second: second,
                discount: discount,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            function(data){
                if(data){
                    $.cookie('message', 'Скидка добавлена');
                    $.cookie('message_type', 'good');
                    $(document).trigger('message');
                    setTimeout(function () {
                        document.location.replace('/adminpanel/');
                    }, 1000);
                } else{
                    $.cookie('message', 'Данные некорректны');
                    $.cookie('message_type', 'bad');
                    $(document).trigger('message');
                }
            }
        );

        return false;
    });
    $('#first-item').keyup(function(){
        if($(this).val().length >= 2){
            var value = $(this).val();
            var search_str = '/adminpanel/ajax_adm_search/' + value;
            $('#ci1').load(search_str, function(){
                $(this).show();
                $('#ci1 li').click(function(){
                    first = $(this).data('inv');
                    val = $(this).data('name');
                    $('#first-item').val(val);
                    console.log(first)
                });
                $('#first-item').focusout(function(){
                    $('#ci1').hide(function(){
                        $(this).html("");
                    });
                });
            });
        } else{
           $('#ci1').hide(function(){
               $(this).html("");
           });
        }
        return false;
    });
    $('#second-item').keyup(function(){
        if($(this).val().length >= 2){
            var value = $(this).val();
            var search_str = '/adminpanel/ajax_adm_search/' + value;
            $('#ci2').load(search_str, function(){
                $(this).show();
                $('#ci2 li').click(function(){
                    second = $(this).data('inv');
                    val = $(this).data('name');
                    $('#second-item').val(val);
                    console.log(second)
                });
                $('#second-item').focusout(function(){
                    $('#ci2').hide(function(){
                        $(this).html("");
                    });
                });
            });
        } else{
           $('#ci2').hide(function(){
               $(this).html("");
           });
        }
        return false;
    });
});
