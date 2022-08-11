import '../sass/main.scss';

import GetStartedMenu from './components/get-started-menu';
import SiteSearch from './components/site-search';

function initComponent(ComponentClass) {
    const items = document.querySelectorAll(ComponentClass.selector());
    items.forEach((item) => new ComponentClass(item));
}

document.addEventListener('DOMContentLoaded', () => {
    initComponent(GetStartedMenu);
    initComponent(SiteSearch);
});
