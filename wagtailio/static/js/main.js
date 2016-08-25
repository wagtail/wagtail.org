/* Modernizr 2.8.3 (Custom Build) | MIT & BSD
 * Build: http://modernizr.com/download/#-flexbox-csstransforms3d-shiv-cssclasses-teststyles-testprop-testallprops-prefixes-domprefixes
 */
;window.Modernizr=function(a,b,c){function z(a){j.cssText=a}function A(a,b){return z(m.join(a+";")+(b||""))}function B(a,b){return typeof a===b}function C(a,b){return!!~(""+a).indexOf(b)}function D(a,b){for(var d in a){var e=a[d];if(!C(e,"-")&&j[e]!==c)return b=="pfx"?e:!0}return!1}function E(a,b,d){for(var e in a){var f=b[a[e]];if(f!==c)return d===!1?a[e]:B(f,"function")?f.bind(d||b):f}return!1}function F(a,b,c){var d=a.charAt(0).toUpperCase()+a.slice(1),e=(a+" "+o.join(d+" ")+d).split(" ");return B(b,"string")||B(b,"undefined")?D(e,b):(e=(a+" "+p.join(d+" ")+d).split(" "),E(e,b,c))}var d="2.8.3",e={},f=!0,g=b.documentElement,h="modernizr",i=b.createElement(h),j=i.style,k,l={}.toString,m=" -webkit- -moz- -o- -ms- ".split(" "),n="Webkit Moz O ms",o=n.split(" "),p=n.toLowerCase().split(" "),q={},r={},s={},t=[],u=t.slice,v,w=function(a,c,d,e){var f,i,j,k,l=b.createElement("div"),m=b.body,n=m||b.createElement("body");if(parseInt(d,10))while(d--)j=b.createElement("div"),j.id=e?e[d]:h+(d+1),l.appendChild(j);return f=["&#173;",'<style id="s',h,'">',a,"</style>"].join(""),l.id=h,(m?l:n).innerHTML+=f,n.appendChild(l),m||(n.style.background="",n.style.overflow="hidden",k=g.style.overflow,g.style.overflow="hidden",g.appendChild(n)),i=c(l,a),m?l.parentNode.removeChild(l):(n.parentNode.removeChild(n),g.style.overflow=k),!!i},x={}.hasOwnProperty,y;!B(x,"undefined")&&!B(x.call,"undefined")?y=function(a,b){return x.call(a,b)}:y=function(a,b){return b in a&&B(a.constructor.prototype[b],"undefined")},Function.prototype.bind||(Function.prototype.bind=function(b){var c=this;if(typeof c!="function")throw new TypeError;var d=u.call(arguments,1),e=function(){if(this instanceof e){var a=function(){};a.prototype=c.prototype;var f=new a,g=c.apply(f,d.concat(u.call(arguments)));return Object(g)===g?g:f}return c.apply(b,d.concat(u.call(arguments)))};return e}),q.flexbox=function(){return F("flexWrap")},q.csstransforms3d=function(){var a=!!F("perspective");return a&&"webkitPerspective"in g.style&&w("@media (transform-3d),(-webkit-transform-3d){#modernizr{left:9px;position:absolute;height:3px;}}",function(b,c){a=b.offsetLeft===9&&b.offsetHeight===3}),a};for(var G in q)y(q,G)&&(v=G.toLowerCase(),e[v]=q[G](),t.push((e[v]?"":"no-")+v));return e.addTest=function(a,b){if(typeof a=="object")for(var d in a)y(a,d)&&e.addTest(d,a[d]);else{a=a.toLowerCase();if(e[a]!==c)return e;b=typeof b=="function"?b():b,typeof f!="undefined"&&f&&(g.className+=" "+(b?"":"no-")+a),e[a]=b}return e},z(""),i=k=null,function(a,b){function l(a,b){var c=a.createElement("p"),d=a.getElementsByTagName("head")[0]||a.documentElement;return c.innerHTML="x<style>"+b+"</style>",d.insertBefore(c.lastChild,d.firstChild)}function m(){var a=s.elements;return typeof a=="string"?a.split(" "):a}function n(a){var b=j[a[h]];return b||(b={},i++,a[h]=i,j[i]=b),b}function o(a,c,d){c||(c=b);if(k)return c.createElement(a);d||(d=n(c));var g;return d.cache[a]?g=d.cache[a].cloneNode():f.test(a)?g=(d.cache[a]=d.createElem(a)).cloneNode():g=d.createElem(a),g.canHaveChildren&&!e.test(a)&&!g.tagUrn?d.frag.appendChild(g):g}function p(a,c){a||(a=b);if(k)return a.createDocumentFragment();c=c||n(a);var d=c.frag.cloneNode(),e=0,f=m(),g=f.length;for(;e<g;e++)d.createElement(f[e]);return d}function q(a,b){b.cache||(b.cache={},b.createElem=a.createElement,b.createFrag=a.createDocumentFragment,b.frag=b.createFrag()),a.createElement=function(c){return s.shivMethods?o(c,a,b):b.createElem(c)},a.createDocumentFragment=Function("h,f","return function(){var n=f.cloneNode(),c=n.createElement;h.shivMethods&&("+m().join().replace(/[\w\-]+/g,function(a){return b.createElem(a),b.frag.createElement(a),'c("'+a+'")'})+");return n}")(s,b.frag)}function r(a){a||(a=b);var c=n(a);return s.shivCSS&&!g&&!c.hasCSS&&(c.hasCSS=!!l(a,"article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}mark{background:#FF0;color:#000}template{display:none}")),k||q(a,c),a}var c="3.7.0",d=a.html5||{},e=/^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i,f=/^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i,g,h="_html5shiv",i=0,j={},k;(function(){try{var a=b.createElement("a");a.innerHTML="<xyz></xyz>",g="hidden"in a,k=a.childNodes.length==1||function(){b.createElement("a");var a=b.createDocumentFragment();return typeof a.cloneNode=="undefined"||typeof a.createDocumentFragment=="undefined"||typeof a.createElement=="undefined"}()}catch(c){g=!0,k=!0}})();var s={elements:d.elements||"abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output progress section summary template time video",version:c,shivCSS:d.shivCSS!==!1,supportsUnknownElements:k,shivMethods:d.shivMethods!==!1,type:"default",shivDocument:r,createElement:o,createDocumentFragment:p};a.html5=s,r(b)}(this,b),e._version=d,e._prefixes=m,e._domPrefixes=p,e._cssomPrefixes=o,e.testProp=function(a){return D([a])},e.testAllProps=F,e.testStyles=w,g.className=g.className.replace(/(^|\s)no-js(\s|$)/,"$1$2")+(f?" js "+t.join(" "):""),e}(this,this.document);

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

    /************************************************************
    *
    * Equal heights for when no flexbox browsers
    *
    */
    function equalheight( item ){

        var tallestInRow    = 0,
            lastItemXPos    = 0,
            itemXPos        = 0,
            rowDivs         = [];

        $( item ).each(function( ){

            var $el = $( this ); // current element
            $el.height( 'auto' ); // Ensure height is auto to ensure we fetching the automatic calculate height
            itemXPos = $el.position().top; // Find the top position so we can determin which row we are on

            // Create new row if:
            if( lastItemXPos != itemXPos ){

                // Find the tallest item in current row and set the height of the current item
                for( currentDiv = 0; currentDiv < rowDivs.length; currentDiv++ ){
                    rowDivs[currentDiv].height( tallestInRow ); // Set height on all divs in row
                }

                lastItemXPos = itemXPos; // Set lastItemTop
                tallestInRow = $el.height(); // ?
                rowDivs = []; // empty array
                rowDivs.push($el); // push item to array

            // Otherwise assume we in the same row
            } else {
                rowDivs.push($el); // push item to array
                tallestInRow = ( tallestInRow < $el.height() ) ? ( $el.height() ) : ( tallestInRow ); // calculate tallest in row
            }

            // TODO: Remove this or justify it?
            for (currentDiv = 0 ; currentDiv < rowDivs.length ; currentDiv++) {
                rowDivs[currentDiv].height(tallestInRow);
            }
        });

    };

    // If we have no flexbox...
    if( $( 'html' ).hasClass( 'no-flexbox' ) ){

        $(window).load(function() {
            equalheight('.flex-list > li a');
        });

        $(window).resize(function(){
            // console.log( ' ====== resize =======' );
            equalheight('.flex-list > li a');
        });
    }

    // FB sharing popup
    // Facebook sharing dialog (assumes FB.init has run)
    $( '.share .fa-facebook' ).on('click', function( e ){
        e.preventDefault();
        FB.ui({
            method: 'share',
            href: document.location.href
        }, function(response){});
    });

    // Facebook code
    window.fbAsyncInit = function() {
        FB.init({
            appId: {{ FB_APP_ID }},
            xfbml: true,
            version: 'v2.1'
        });
    };

    (function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

});
