function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  document.cookie = encodeURIComponent(name) + '=' +
                    encodeURIComponent(value) +
                    '; expires=' + date.toGMTString();
}

function hasCookie(name, value) {
  return document.cookie.split('; ').indexOf(name + '=' + value) >= 0;
}

$(function () {
  const $kickstarter = $('.kickstarter');

  $kickstarter.toggleClass(
    'visible',
    !hasCookie('kickstarterClosed', 'true')
      && new Date() < new Date(2018, 3, 17));
  $kickstarter.find('.close').click(function (e) {
    e.preventDefault();
    setCookie('kickstarterClosed', 'true', 30);
    $kickstarter.detach();
  });
});
