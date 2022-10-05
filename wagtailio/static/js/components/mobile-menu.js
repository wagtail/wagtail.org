class MobileMenu {
    static selector() {
        return '[data-mobile-menu-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.mobileMenu = document.querySelector('[data-mobile-menu]');

        this.state = {
            open: false,
        };

        this.bindEventListeners();
    }

    bindEventListeners() {
        this.node.addEventListener('click', () => {
            this.toggle();
        });
    }

    toggle() {
        if (this.state.open) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        // Fire a custom event which is useful if we need any other items such as
        // a search box to close when the mobile menu opens
        // Can be listened to with
        // document.addEventListener('onMenuOpen', () => {
        //     // do stuff here...;
        // });
        const menuOpenEvent = new Event('onMenuOpen');
        document.dispatchEvent(menuOpenEvent);
        this.node.classList.add('is-open');
        this.node.setAttribute('aria-expanded', 'true');
        this.body.classList.add('no-scroll');
        this.mobileMenu.classList.add('is-visible');

        this.state.open = true;
    }

    close() {
        this.node.classList.remove('is-open');
        this.node.setAttribute('aria-expanded', 'false');
        this.body.classList.remove('no-scroll');
        this.mobileMenu.classList.remove('is-visible');

        this.state.open = false;
    }
}

export default MobileMenu;
