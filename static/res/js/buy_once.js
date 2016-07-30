/**
 * Created by шаша on 29.07.2016.
 */
$(document).ready(function(){
    $(document).on('click', '.btn',function(){
        var price = parseFloat($(this).data('price'));
        var item = parseInt($(this).data('item'));
        var basket = $.cookie('basket-price');
        if(basket){
            basket = JSON.parse(basket);
            if(basket.item.indexOf(item) != -1){
                var pos = basket.item.indexOf(item);
                basket.count[pos] = 1;
                basket.price[pos] = price;
            } else{
                basket.item.push(item);
                basket.count.push(1);
                basket.price.push(price);
            }
            $.cookie('basket-price', JSON.stringify(basket),{
                path: '/'
            });
        } else{
            basket = {
                item: [item],
                count: [1],
                price: [price]
            };
            $.cookie('basket-price', JSON.stringify(basket),{
                path: '/'
            });
        }
        $(document).trigger('cookieUpdate');
        $.post(
           '/ajax_addbasket/',
           {
               item: item,
               count: 1
           },
           function(){
               $.cookie('message', 'Товар добавлен в корзину');
               $.cookie('message_type', 'good');
               $(document).trigger('message');
           }
       );

    });


});