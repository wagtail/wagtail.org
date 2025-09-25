
class MobileSubMenu {
    static selector() {
        return '[data-mobile-menu] [data-open-subnav]';
    }

    constructor(node) {
        this.node = node;
        this.subnav = this.node.nextElementSibling;
        
        // Only proceed if subnav exists
        if (!this.subnav) {
            return;
        }
        
        this.backLink = this.subnav.querySelector('[data-subnav-back]');
        this.bindEventListeners();
    }

    bindEventListeners() {
        // Only bind event listeners if subnav exists
        if (!this.subnav) {
            return;
        }
        
        // Open submenu
        this.node.addEventListener('click', (e) => {
            e.preventDefault();
            this.open();
        });
        
        // Click back button to close it
        if (this.backLink) {
            this.backLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.close();
            });
        }

        // Allow pressing Escape to close
        this.subnav.addEventListener('keydown', (e) => {
            if (e.key !== 'Escape') return;
            this.close();
        });
    }

    open() {
        if (!this.subnav) {
            return;
        }
        
        this.subnav.classList.add('is-visible');
        this.node.setAttribute('aria-expanded', 'true');
    }

    close() {
        if (!this.subnav) {
            return;
        }
        
        this.subnav.classList.remove('is-visible');
        this.node.setAttribute('aria-expanded', 'false');
    }
}

export default MobileSubMenu;
