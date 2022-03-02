$(function() {
  // FB sharing popup
  // Facebook sharing dialog (assumes FB.init has run)
  $(".share .fa-facebook").on("click", function(e) {
    e.preventDefault();
    FB.ui(
      {
        method: "share",
        href: document.location.href
      },
      function(response) {}
    );
  });

  // tabs
  $(".js-tabs").each(function() {
    // For each set of tabs, we want to keep track of
    // which tab is active and its associated content
    var $active,
      $content,
      $links = $(this).find("a");

    // If the location.hash matches one of the links, use that as the active tab.
    // If no match is found, use the first link as the initial active tab.
    $active = $(
      $links.filter('[href="' + location.hash + '"]')[0] || $links[0]
    );
    $active.addClass("current");

    $content = $($active[0].hash);

    // Hide the remaining content
    $links.not($active).each(function() {
      $(this.hash).hide();
    });

    // Bind the click event handler
    $(this).on("click", "a", function(e) {
      // Make the old tab inactive.
      $active.removeClass("current");
      $content.removeClass("current");
      $content.hide();

      // Update the variables with the new link and content
      $active = $(this);
      $content = $(this.hash);

      // Make the tab active.
      $active.addClass("current");
      $content.addClass("current");
      $content.show();

      // Prevent the anchor's default click action
      e.preventDefault();
    });
  });

  $(".js-tabs-proxy-link").on("click", function(e) {
    var $targetElement = $(this.hash);
    var $proxyTo = $(".js-tabs").find('a[href="' + this.hash + '"]')[0];

    // This links already have all required logic to switch tabs,
    // so just generate a click event to activate the logic
    $proxyTo.click();

    $("html, body").animate(
      {
        scrollTop: $targetElement.offset().top - $("header.global").height()
      },
      500
    );

    e.preventDefault();
  });

  // Menu button
  $(".menu-toggle").on("click", function(e) {
    e.preventDefault();
    $("body").toggleClass("mobile_nav-open");
  });

  // Blog index for mobile button
  $(".blog-index-button").on("click", function(e) {
    $("body").toggleClass("sidebar-open");
  });

  // Window resize
  $(window).on("resize", function() {
    // Scrolling inside the sidebar list
    // causes the resize event to fire on Chrome Android.
    // Disabled to fix this bug

    // Close nav on resize
    // $("body").removeClass("mobile_nav-open");
    // $("body").removeClass("sidebar-open");
  });

  /***

    Plugins

    ***/

  // Owl carousel
  $(".logo-list .carousel").owlCarousel({
    navigation: false,
    slideSpeed: 500,
    paginationSpeed: 500,
    transitionStyle: "fade",
    items: 8,
    itemsDesktop: [1025, 6],
    itemsDesktopSmall: [979, 4],
    itemsTablet: [768, 4],
    itemsMobile: [481, 2]
  });

  $(".js-carousel").owlCarousel({
    navigation: false,
    slideSpeed: 500,
    paginationSpeed: 500,
    items: 1,
    itemsDesktop: [1025, 1],
    itemsDesktopSmall: [979, 1],
    itemsTablet: [768, 1],
    itemsMobile: [481, 1]
  });

  // headroom
  // http://wicky.nillia.ms/headroom.js/
  $("body").headroom({
    tolerance: {
      up: 0,
      down: 10
    },
    classes: {
      initial: "site-header--animated",
      pinned: "site-header--slidedown",
      unpinned: "site-header--slideup"
    }
  });

  // Cookie message
  var messageContainer = $("[data-cookie-message]")
  var dismissButton = $("[data-cookie-dismiss]")
  if(messageContainer) {
    // If cookie doesn't exists
    if(!Cookies.get('client-cookie')) {
      messageContainer.addClass('active')
    }
  }
  // Bind cookie dismiss handler
  if(dismissButton) {
    dismissButton.click(function (event) {
      event.preventDefault(); // ensure the href is not used (scrolls user to the top)
      Cookies.set('client-cookie', 'agree to cookies', {
        expires: 365, // Cookie expires after 365 days
      });
      messageContainer.removeClass('active')
      messageContainer.addClass('inactive')
    })
  }

  var $alert_container = $("[data-alert]");
  if ($alert_container.data("alert")) {
    $.getJSON($alert_container.data("alert"), function(data) {
      if (data.text) {
        $alert_container.html('<aside class="alert">' + data.text + '</aside>');
        var $aside = $alert_container.find("aside");
        var styles = {};
        if (data.bg_colour) {
          styles['background-color'] = '#' + data.bg_colour;
        }
        if (data.text_colour) {
          styles['color'] = '#' + data.text_colour;
        }
        $aside.css(styles).toggleClass('alert--default', !(data.bg_colour || data.text_colour));
        setTimeout(() => {
          $aside.addClass('alert--active');
        }, 1);
      }
    })
  }
});
