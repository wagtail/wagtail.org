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
    $( '#body' ).on( 'scroll', function( ){

        var $footer = $( 'footer' );

        if ( $footer.is( ':in-viewport' ) ) {
            $( 'body' ).addClass( 'footer-in' );
        } else {
            $( 'body' ).removeClass( 'footer-in' );
        }

    });

});