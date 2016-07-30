$(document).ready(function(){
   $('#buy-btn').click(function(){
       var count = Math.abs($('#buy-count').val());
       if(!count){
           count = 1;
       }
       var price;
       if(count > 1){
           if(parseFloat($('#buy-btn').data('price_opt'))){
               price = parseFloat($('#buy-btn').data('price_opt'));
           } else{
               price = parseFloat($('#buy-btn').data('price'));
           }
       } else{
           price = parseFloat($('#buy-btn').data('price'));
       }
       var item = parseInt($('#buy').data('item'));
       var basket = $.cookie('basket-price');
       if(basket){
           basket = JSON.parse(basket);
           if(basket.item.indexOf(item) != -1){
               var pos = basket.item.indexOf(item);
               basket.count[pos] = count;
               basket.price[pos] = price;
           } else{
               basket.item.push(item);
               basket.count.push(count);
               basket.price.push(price);
           }
           $.cookie('basket-price', JSON.stringify(basket),{
               path: '/'
           });
       } else{
           basket = {
               item: [item],
               count: [count],
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
               item: $('#buy').data('item'),
               count: count
           },
           function(){
               $.cookie('message', 'Товар добавлен в корзину');
               $.cookie('message_type', 'good');
               $(document).trigger('message');
           }
       );
   });
});
