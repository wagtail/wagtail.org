$(function( ){

    // tabs
    $('.js-tabs').each(function(){
        // For each set of tabs, we want to keep track of
        // which tab is active and its associated content
        var $active, $content, $links = $(this).find('a');

        // If the location.hash matches one of the links, use that as the active tab.
        // If no match is found, use the first link as the initial active tab.
        $active = $($links.filter('[href="'+location.hash+'"]')[0] || $links[0]);
        $active.addClass('current');

        $content = $($active[0].hash);

        // Hide the remaining content
        $links.not($active).each(function () {
            $(this.hash).hide();
        });

        // Bind the click event handler
        $(this).on('click', 'a', function(e){
            // Make the old tab inactive.
            $active.removeClass('current');
            $content.removeClass('current');
            $content.hide();

            // Update the variables with the new link and content
            $active = $(this);
            $content = $(this.hash);

            // Make the tab active.
            $active.addClass('current');
            $content.addClass('current');
            $content.show();

            // Prevent the anchor's default click action
            e.preventDefault();
        });
    });

    // Slow scroll on anchors
    function anchorScroll(event) {

        // prevent default link action
        event.preventDefault();

        // make some vars so it is easy to understand what we are doing
        var $clicked    = $(this);
        var id          = $clicked.attr('href');
        var $target     = $(id);

        // if there is no target, fail silently
        if ($target.length === 0) {
            // TODO: this breaks the django debug toolbar and possibly some other event handlers too
            return false;
        }

        // animate html & body scrollTop property to the top position of the $target element
        $('html, body').animate({
            scrollTop: $target.offset().top,
        }, 500);

    }

    $(window).on('scroll', function () {

        // Fadeout effect
        $('.js-fade').css('opacity', 1 - $(window).scrollTop() / 250);

    });

    // Slow scroll on anchor links
    $('a[href*=#]').on('click', anchorScroll);

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
        items : 8,
        itemsDesktop : [1025,6],
        itemsDesktopSmall : [979,4],
        itemsTablet : [768,4],
        itemsMobile : [481,2]
    });


});
