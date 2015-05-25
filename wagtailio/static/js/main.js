$(function( ){

	// Menu button
	$('a[href=#primary_navigation]').on( 'click', function( ){
		$('body').toggleClass( 'mobile_nav-open' );
	});

	$( window ).on('resize', function( ){
		// Close nav on resize
		$('body').removeClass( 'mobile_nav-open' );
	});

});