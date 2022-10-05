// Expected markup - see primarynav.html
/* <ul class="primary-nav" data-primary-nav="">
    <li class="primary-nav__item primary-nav__item--is-parent" data-has-subnav="">
        <a class="primary-nav__link" data-open-subnav="" href="/" aria-haspopup="true" aria-expanded="false">
            Home
            <span class="primary-nav__icon">›</span>
        </a>
        <ul class="sub-nav" data-subnav="">
            <li class="sub-nav__item sub-nav__item--back"><a data-subnav-back="" href="#">‹ Back</a></li>
            <li class="sub-nav__item">
                <a class="sub-nav__link" href="/">About us overview</a>
            </li>
            <li class="sub-nav__item sub-nav__item--secondary">
                <a class="sub-nav__link" href="/page-1/">page 1</a>
            </li>
        </ul>
    </li>
</ul> */

class MobileSubMenu {
    static selector() {
        return '[data-mobile-menu] [data-open-subnav]';
    }

    constructor(node) {
        this.node = node;
        this.subnav = this.node.nextElementSibling;
        this.backLink = this.subnav.querySelector('[data-subnav-back]');
        this.bindEventListeners();
    }

    bindEventListeners() {
        // Open submenu
        this.node.addEventListener('click', (e) => {
            e.preventDefault();
            this.open();
        });
        // Click back button to close it
        this.backLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.subnav.classList.remove('is-visible');
            this.node.setAttribute('aria-expanded', 'false');
        });
    }

    open() {
        this.subnav.classList.add('is-visible');
        this.node.setAttribute('aria-expanded', 'true');
    }
}

export default MobileSubMenu;
