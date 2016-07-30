/**
 * Created by шаша on 25.07.2016.
 */
$(document).ready(function () {
    $('.fa-times').click(function () {
        var item = parseInt($(this).data('item'));
        var basket = $.cookie('basket-price');
        alert(basket);
        basket = JSON.parse(basket);
        var pos = basket.item.indexOf(item);
        basket.item.splice(pos, 1);
        basket.count.splice(pos, 1);
        basket.price.splice(pos, 1);
        $.cookie('basket-price', JSON.stringify(basket),{
               expire: 30,
               path: '/'
        });
        alert($.cookie('basket-price'));
        var selectr = '.table_blur tr[data-item=' + item + ']';
        $(selectr).remove();
        $(document).trigger('cookieUpdate');
        $.post(
            '/ajax_remove_from_basket/',
            {
                item: item
            }
        );
        if(!basket.item.length){
            document.location.replace('/');
        }
    });
});