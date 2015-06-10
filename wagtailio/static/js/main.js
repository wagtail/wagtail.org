$(function( ){

    // TODO: make selectors variables for portability

    // Menu button
    $( 'a[href=#primary_navigation]' ).on( 'click', function( e ){
        e.preventDefault();
        $( 'body' ).toggleClass( 'mobile_nav-open' );
    });

    // Blog index for mobile button
    $( '.blog-index-button' ).on( 'click', function( e ){
        e.preventDefault();
        $( 'body' ).toggleClass( 'sidebar-open' );
    });

    // Window resize
    $( window ).on('resize', function( ){
        // Close nav on resize
        $( 'body' ).removeClass( 'mobile_nav-open' );
        $( 'body' ).removeClass( 'sidebar-open' );
    });

    $( window ).on('load', function( ){
        
    });

    /************************************************************
    *
    * Hero Carousel
    * mostly hacked together for speed, can be tideid up (relatively) painlessly
    *
    */

    // function is called imediately after definition (should put this call in a page/component specific check...)
    var heroCarousel = function( ){

        var time = 5, // time in seconds
            $currentBar,
            $elem,
            isPause,
            tick,
            percentTime;

        // Carousel
        $("#hero .carousel").owlCarousel({

            // navigation : true, // Show next and prev buttons
            slideSpeed      : 500,
            paginationSpeed : 400,
            singleItem      : true,
            afterInit       : progressBar,
            afterMove       : moved,
            startDragging   : pauseOnDragging
          
        });

        // Init progressBar
        // @elem is $("#owl-carousel")
        // TODO: change function name 
        function progressBar( elem ){

            // Pointer for carousel (should really have a better name)
            $elem = elem;

            // navigation stuff
            // Add carousel titles to pagination items
            var $items = $elem.find( '.owl-item' ),
                $pagination = $elem.find( '.owl-page' );

            $items.each(function( i ){
                var $item = $( this ),
                    $pageItem = $( $pagination[i] ),
                    title = $item.find( 'h1' ).clone(); // change this so it only clones the text of the h1

                $pageItem.append( title );

            });

            //build progress bar elements
            buildProgressBar( $pagination );
            //start counting
            start();

            // Add class to body so we can show the carousel (avoids flash of un-JS carousel)
            $( 'body' ).addClass( 'carousel-loaded' );

        }

        //create div#progressBar and div#bar then prepend to $("#owl-demo")
        function buildProgressBar( $pagination ){

            var $container = $("<div>",{
                    class:"progressBar"
                }),
                $bar = $("<div>",{
                    class:"bar"
                }),
                progressBar;

            // build it (could be neater to do this at the top TBH)
            progressBar = $container.append($bar); //.prependTo($elem);

            $pagination.each(function( ){
                var $item = $( this ),
                    $progressBar = progressBar.clone();

                $item.append( $progressBar );
            });

            // set first bar as currentBar
            $currentBar = $( $pagination[0] ).find( '.bar' );

        }

        function start( ){
            //reset timer
            percentTime = 0;
            isPause = false;
            //run interval every 0.01 second
            tick = setInterval(interval, 10);
        }

        function interval( ){

            if(isPause === false){
                percentTime += 1 / time
                $currentBar.css({
                    width: percentTime + "%"
                });
                //if percentTime is equal or greater than 100
                if( percentTime >= 100 ){
                    //slide to next item 
                    $elem.trigger('owl.next');
                }
            }

        }

        //pause while dragging 
        function pauseOnDragging( ){
            isPause = true;
        }

        //moved callback
        function moved( ){
            //clear interval
            clearTimeout(tick);
            // Set currentBar
            $currentBar = $elem.find( '.owl-page.active .bar');
            //start again
            start();
        }

        // uncomment this to make pause on mouseover 
        // img & text only plx
        // $elem.find('.image > *, .text > *').on( 'mouseover' ,function(){
        //     isPause = true;
        // })
        // $elem.find('.image > *, .text > *').on( 'mouseout' ,function(){
        //     isPause = false;
        // })

    }();

    /************************************************************
    *
    * Examples Carousel
    *
    */
    $("#examples .carousel").owlCarousel({

        // navigation : true, // Show next and prev buttons
        slideSpeed      : 500,
        paginationSpeed : 500,
        singleItem      : true,
        transitionStyle : "fade"
      
    });


    // Scroll behaviours
    // not currently used
    // $( '#body' ).on( 'scroll', function( ){

    //     var $footer = $( 'footer' );

    //     if ( $footer.is( ':in-viewport' ) ) {
    //         $( 'body' ).addClass( 'footer-in' );
    //     } else {
    //         $( 'body' ).removeClass( 'footer-in' );
    //     }

    // });

    function has3d() {
        if (!window.getComputedStyle) {
            return false;
        }

        var el = document.createElement('p'), 
            has3d,
            transforms = {
                'webkitTransform':'-webkit-transform',
                'OTransform':'-o-transform',
                'msTransform':'-ms-transform',
                'MozTransform':'-moz-transform',
                'transform':'transform'
            };

        // Add it to the body to get the computed style.
        document.body.insertBefore(el, null);

        for (var t in transforms) {
            if (el.style[t] !== undefined) {
                el.style[t] = "translate3d(1px,1px,1px)";
                has3d = window.getComputedStyle(el).getPropertyValue(transforms[t]);
            }
        }

        document.body.removeChild(el);

        return (has3d !== undefined && has3d.length > 0 && has3d !== "none");
    };

    if( !has3d() ){
        $( 'html' ).addClass( 'no-transform' );
    }

    // FB sharing popup
    // Facebook sharing dialog (assumes FB.init has run)
    $(document).on('click', '.share .fa-facebook', function(e){
        e.preventDefault();
        FB.ui({
            method: 'share',
            href: document.location.href
        }, function(response){});  
    });

});