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
    *
    */

    // function is called imediately after definition
    var homePageCarousel = function( ){

        var time = 10, // time in seconds
            $progressBar,
            $bar,
            $elem,
            isPause,
            tick,
            percentTime;

        // Carousel
        $("#hero.carousel").owlCarousel({

            // navigation : true, // Show next and prev buttons
            slideSpeed      : 500,
            paginationSpeed : 500,
            singleItem      : true,
            transitionStyle : "fade"
            // afterInit       : progressBar,
            // afterMove       : moved,
            // startDragging   : pauseOnDragging
          
        });

        //Init progressBar where elem is $("#owl-demo")
        function progressBar( elem ){
            $elem = elem;
            //build progress bar elements
            buildProgressBar();
            //start counting
            start();
        }

        //create div#progressBar and div#bar then prepend to $("#owl-demo")
        function buildProgressBar( ){
            $progressBar = $("<div>",{
                id:"progressBar"
            });
            $bar = $("<div>",{
                id:"bar"
            });
            $progressBar.append($bar).prependTo($elem);
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
            percentTime += 1 / time;
            $bar.css({
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

});