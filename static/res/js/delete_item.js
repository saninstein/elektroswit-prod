/**
 * Created by шаша on 22.07.2016.
 */
$(document).ready(function(){
    $('.fa-times').click(function(){
        var item = $(this).data('item');
        var csrf = $('input[name=csrfmiddlewaretoken]').val()


        $.post(
            "/adminpanel/ajax_delete/",
            {
                item: item,
                csrfmiddlewaretoken: csrf
            },
            function(data){
                if(data){
                    $.cookie('message', 'Успешно удалено');
                    $.cookie('message_type', 'good');
                    $(document).trigger('message');
                    setTimeout(function(){
                        location.reload(true);
                    }, 1000);
                } else {
                    $.cookie('message', 'Ошибка удаления');
                    $.cookie('message_type', 'bad');
                    $(document).trigger('message');
                }

            }

        );
    });
});