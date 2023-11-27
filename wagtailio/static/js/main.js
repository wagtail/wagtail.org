import '../sass/main.scss';

import './components/theme-detect';
import GetStartedMenu from './components/get-started-menu';
import SiteSearchDesktop from './components/site-search-desktop';
import SiteSearchMobile from './components/site-search-mobile';
import FooterMenuColumn from './components/footer-menu-column';
import FeatureIndex from './components/feature-index';
import CopyCodeSnippet from './components/copy-code-snippet';
import MobileMenu from './components/mobile-menu';
import MobileSubMenu from './components/mobile-sub-menu';
import DesktopSubMenu from './components/desktop-sub-menu';
import DesktopCloseMenus from './components/desktop-close-menus';
import CookieMessage from "./components/cookie-message";
import SiteWideAlert from "./components/site-wide-alert";

function initComponent(ComponentClass) {
    const items = document.querySelectorAll(ComponentClass.selector());
    items.forEach((item) => new ComponentClass(item));
}

document.addEventListener('DOMContentLoaded', () => {
    // Remove no-js class if JS is enabled
    document.documentElement.classList.remove('no-js');

    initComponent(CookieMessage);
    initComponent(SiteWideAlert);
    initComponent(GetStartedMenu);
    initComponent(SiteSearchDesktop);
    initComponent(SiteSearchMobile);
    initComponent(FooterMenuColumn);
    initComponent(FeatureIndex);
    initComponent(CopyCodeSnippet);
    initComponent(MobileMenu);
    initComponent(MobileSubMenu);
    initComponent(DesktopSubMenu);
    /* eslint-disable no-new */
    new DesktopCloseMenus();
});
