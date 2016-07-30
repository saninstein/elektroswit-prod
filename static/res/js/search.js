/**
 * Created by Alex on 14.07.2016.
 */

$(document).ready(function(){
    $("#search").keyup(function(){
        var value = $(this).val();
            if(value.length >= 2){
                var search_str = '/ajax_search/' + value;
                $("#search-list").load(search_str, function(){
                    $(this).show(function(){
                        $("#search").focusout(function(){
                            $("#search-list").hide(function(){
                            $(this).html("");
                            });
                        });
                    });
                });

            } else{
                $("#search-list").hide(function(){
                    $(this).html("");
                });
            }

    });
    $("#search").keydown(function(){
        if(event.keyCode == 13){
            if($(this).val().length){
                document.location.replace('/search/' + $(this).val(), true);
            }
        };
    });
});


