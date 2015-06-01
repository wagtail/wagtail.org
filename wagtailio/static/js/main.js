$(function( ){

    // Menu button
    $('a[href=#primary_navigation]').on( 'click', function( ){
        $('body').toggleClass( 'mobile_nav-open' );
    });

    // Window resize
    $( window ).on('resize', function( ){
        // Close nav on resize
        $('body').removeClass( 'mobile_nav-open' );
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

    /************************************************************
    *
    * Hero Carousel
    * mostly hacked together for speed, can be tideid up (relatively) painlessly
    *
    */

    // function is called imediately after definition (should put this call in a page/component specific check...)
    var heroCarousel = function( ){

        var time = 3.5, // time in seconds
            $currentBar,
            $elem,
            isPause,
            tick,
            percentTime;

        // Carousel
        $("#hero.carousel").owlCarousel({

            // navigation : true, // Show next and prev buttons
            slideSpeed      : 500,
            paginationSpeed : 400,
            singleItem      : true,
            transitionStyle : "fade",
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
                    title = $item.find( 'h3' ).clone();

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

        //uncomment this to make pause on mouseover 
        // $elem.on('mouseover',function(){
        //     isPause = true;
        // })
        // $elem.on('mouseout',function(){
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

});