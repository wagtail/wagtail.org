import '../sass/main.scss';

import GetStartedMenu from './components/get-started-menu';
import SiteSearchDesktop from './components/site-search-desktop';
import SiteSearchMobile from './components/site-search-mobile';
import FooterMenuColumn from './components/footer-menu-column';
import FeatureIndex from './components/feature-index';
import Feature from './components/feature';

function initComponent(ComponentClass) {
    const items = document.querySelectorAll(ComponentClass.selector());
    items.forEach((item) => new ComponentClass(item));
}

document.addEventListener('DOMContentLoaded', () => {
    // Remove no-js class if JS is enabled
    document.documentElement.classList.remove('no-js');

    initComponent(GetStartedMenu);
    initComponent(SiteSearchDesktop);
    initComponent(SiteSearchMobile);
    initComponent(FooterMenuColumn);
    initComponent(FeatureIndex);
    initComponent(Feature);
});
