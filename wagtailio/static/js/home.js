$(function( ){

    // Features tabs
    $('.pane--vertical-tabs .tabs ul li').click(function(){
        var tab_id = $(this).attr('data-tab');

        $('.pane--vertical-tabs .tabs ul li').removeClass('current');
        $('.pane--vertical-tabs .tab-content').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });

    // User groups tabs
    $('.user-groups .tabs ul li').click(function(){
        var tab_id = $(this).attr('data-tab');

        $('.user-groups .tabs ul li').removeClass('current');
        $('.user-groups .tab-content').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });

    // Case studies tabs
    $('.case-studies .tabs ul li').click(function(){
        var tab_id = $(this).attr('data-tab');

        $('.case-studies .tabs ul li').removeClass('current');
        $('.case-studies .tab-content').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });

    $('.tabs ul li a').click(function( e ) {
        e.preventDefault();
    });

    $(window).on('scroll', function () {

        // Fadeout effect
        $('.js-fade').css('opacity', 1 - $(window).scrollTop() / 250);

    });

    /***

    Plugins

    ***/

    // headroom
    // http://wicky.nillia.ms/headroom.js/
    $("header.global").headroom({
        tolerance : {
            up : 0,
            down : 10
        },
    });

    // Owl carousel
    $(".pane--logo-list .carousel").owlCarousel({
        navigation : false,
        slideSpeed      : 500,
        paginationSpeed : 500,
        transitionStyle : "fade",
        items : 6,
        itemsDesktop : [1199,3],
        itemsDesktopSmall : [979,3]
    });

});
