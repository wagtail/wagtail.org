import { createFocusTrap } from 'focus-trap';

class MobileMenu {
    static selector() {
        return '[data-mobile-menu-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.mobileMenu = document.querySelector('[data-mobile-menu]');

        // Check initial state based on CSS classes
        const nodeHasOpenClass = this.node.classList.contains('is-open');
        const menuHasVisibleClass = this.mobileMenu.classList.contains('is-visible');
        const bodyHasNoScrollClass = this.body.classList.contains('no-scroll');
        
        const isInitiallyOpen = nodeHasOpenClass && menuHasVisibleClass && bodyHasNoScrollClass;
        
        this.state = {
            open: isInitiallyOpen,
        };

        // Only create focus trap if required elements exist
        if (this.mobileMenu) {
            this.focusTrap = createFocusTrap(this.mobileMenu);
        } else {
            this.focusTrap = null;
        }

        this.bindEventListeners();
    }

    bindEventListeners() {
        // Use mousedown since click events are being prevented
        this.node.addEventListener('mousedown', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        });

        // Allow pressing Escape to close
        if (this.mobileMenu) {
            this.mobileMenu.addEventListener('keydown', (e) => {
                if (e.key !== 'Escape') return;
                this.close();
            });
        }
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

        const siteWideAlert = document.querySelector('.sitewide-alert');
        const spaceBanner = document.querySelector('.space-banner');
        
        if (siteWideAlert) {
            // adjust for the site-wider alert height
            this.mobileMenu.style.marginTop = siteWideAlert.clientHeight + 'px';
        }
        
        if (spaceBanner) {
            // hide the space banner when mobile menu is open
            spaceBanner.style.display = 'none';
        }

        this.state.open = true;
        if (this.focusTrap) {
            this.focusTrap.activate();
        }
    }

    close() {
        this.node.classList.remove('is-open');
        this.node.setAttribute('aria-expanded', 'false');
        this.body.classList.remove('no-scroll');
        this.mobileMenu.classList.remove('is-visible');

        // show the space banner again when menu is closed
        const spaceBanner = document.querySelector('.space-banner');
        if (spaceBanner) {
            spaceBanner.style.display = '';
        }

        this.state.open = false;
        if (this.focusTrap) {
            this.focusTrap.deactivate();
        }
    }
}

export default MobileMenu;
