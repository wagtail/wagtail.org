

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
            this.close();
        });

        // Allow pressing Escape to close
        this.subnav.addEventListener('keydown', (e) => {
            if (e.key !== 'Escape') return;
            this.close();
        });
    }

    open() {
        this.subnav.classList.add('is-visible');
        this.node.setAttribute('aria-expanded', 'true');

        // Wait for elements to become visible before activating focus trap
        setTimeout(() => {
            this.focusTrap.activate();
        }, 300);
    }

    close() {
        this.subnav.classList.remove('is-visible');
        this.node.setAttribute('aria-expanded', 'false');
        this.focusTrap.deactivate();
    }
}

export default MobileSubMenu;
