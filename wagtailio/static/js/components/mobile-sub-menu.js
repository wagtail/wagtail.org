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
