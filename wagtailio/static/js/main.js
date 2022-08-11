import '../sass/main.scss';

import GetStartedMenu from './components/get-started-menu';
import SiteSearch from './components/site-search';
import FooterMenuColumn from './components/footer-menu-column';

function initComponent(ComponentClass) {
    const items = document.querySelectorAll(ComponentClass.selector());
    items.forEach((item) => new ComponentClass(item));
}

document.addEventListener('DOMContentLoaded', () => {
    // Remove no-js class if JS is enabled
    document.documentElement.classList.remove('no-js');

    initComponent(GetStartedMenu);
    initComponent(SiteSearch);
    initComponent(FooterMenuColumn);
});
