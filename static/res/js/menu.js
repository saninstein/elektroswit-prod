$(document).ready(function () {
    $('#menu li').mouseenter(function () {
        $('#pod-menu').show();
        $('#pod-menu li').css({'visibility': 'hidden'});
        $($(this).data('pd')).css({'visibility': 'visible'});
        if($(this).data('pd') == '#pd4' || $(this).data('pd') == '#pd5'){
            $('.in-list ul li').css({'visibility': 'visible'});
            if($(this).data('pd') == '#pd4'){
                $('#pd5 .in-list ul li').css({'visibility': 'hidden'});
            } else {
                $('#pd4 .in-list ul li').css({'visibility': 'hidden'});
            }
        } else{
            $('#pod-menu').mouseleave(function () {
                $('#pod-menu').hide();
            });
        }


    });

});
