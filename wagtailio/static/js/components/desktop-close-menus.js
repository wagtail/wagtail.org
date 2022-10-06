// Adds "close" functionality for all DesktopSubMenus at once.
// It's a separate class because it captures events outside those components.

import DesktopSubMenu from './desktop-sub-menu';

class DesktopCloseMenus {
    constructor() {
        this.desktopSubMenus = document.querySelectorAll(
            DesktopSubMenu.selector(),
        );
        this.allPrimaryNavs = document.querySelectorAll(
            '[data-desktop-menu] [data-primary-nav]',
        );
        this.bindEvents();
    }

    // Close desktop menus when clicking on document
    closeMenus(e) {
        let close = true;

        this.allPrimaryNavs.forEach((item) => {
            if (item.contains(e.target)) {
                // don't close the menus if we are clicking anywhere on the primary navigation
                close = false;
            }
        });

        if (close) {
            this.desktopSubMenus.forEach((item) => {
                item.closest('[data-has-subnav]').classList.remove('active');
                item.setAttribute('aria-expanded', 'false');
            });
        }
    }

    bindEvents() {
        if (this.desktopSubMenus && this.desktopSubMenus.length !== 0) {
            document.addEventListener('touchstart', (e) => {
                this.closeMenus(e);
            });

            document.addEventListener('click', (e) => {
                this.closeMenus(e);
            });
        }
    }
}

export default DesktopCloseMenus;
