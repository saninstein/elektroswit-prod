/**
 * Created by шаша on 19.07.2016.
 */
$(document).ready(function(){
    if($('#basket').data('basket') == 'EMPTY'){
        $.cookie('basket-price', '',{
               path: '/'
           });
        $(document).trigger('cookieUpdate');
    }

    updateBasketPrice();
    $(document).on('cookieUpdate', function(){
        updateBasketPrice();
    });

    function updateBasketPrice(){
        if($.cookie('basket-price') == '' || !$.cookie('basket-price')){
            $('#basket-full').hide();
            $('#basket-empty').show();
            $('#basket a').css({'visibility': 'hidden'});
            return false;
        }
        var basket = JSON.parse($.cookie('basket-price'));
        var newprice = 0;
        for(var i in basket.item){
            newprice += basket.price[i] * basket.count[i];
        }
        if(newprice){
            $('#basket-empty').hide();
            $('#basket-full').show();
            newprice = String(newprice) + ' грн.';
            $('#basket a u').html(newprice);
            $('#basket a').css({'visibility': 'visible'});
        } else {
            $('#basket-full').hide();
            $('#basket-empty').show();
            $('#basket a').css({'visibility': 'hidden'});
        }
        return false;
    }
});