/**
 * Created by Alex on 16.07.2016.
 */

var arr = [];
var price = [];
var i = 0;
$(":checkbox").change(function(){
    if(this.checked){
        arr[i] = $(this).prop("name");
        i++;
    }else{
        var val = $(this).prop("name");
        var index = arr.indexOf(val);
        arr.splice(index, 1);
        i--;
    }
    $(".wrp").empty();
    $("#loading-img").show();

    var filter_str = "/ajax_notes_filter/";
    if(arr.length){
        arr.forEach(function(item, i, arr){
            filter_str += item;
            filter_str += "-";
        });
        filter_str += 'p' + price[0] + 'p' + price[1] + '/';
    } else{
        var filter_str = "/ajax_notes_filter/" + 'p' + price[0] + 'p' + price[1] + '/';
    }


    setTimeout(function () {
        $(".wrp").load(filter_str, function(){
            $("#loading-img").hide();
        });
    }, 500);

});

$("#price_slider").ionRangeSlider({
    onFinish: function(data){
        $(".wrp").empty();
        $("#loading-img").show();
        var filter_str = "/ajax_notes_filter/";
        if(arr.length){
            arr.forEach(function(item, i, arr){
                filter_str += item;
                filter_str += "-";
            });
            filter_str += 'p' + price[0] + 'p' + price[1] + '/';
        } else{
            var filter_str = "/ajax_notes_filter/" + 'p' + price[0] + 'p' + price[1] + '/';
        }


        setTimeout(function(){
            $(".wrp").load(filter_str, function(){
                $("#loading-img").hide();
            });
        }, 500);

    },
    onStart: function(data){
        price[0] = data['from'];
        price[1] = data['to'];
    },
    onChange: function(data){
        price[0] = data['from'];
        price[1] = data['to'];
    }

});