class SiteSearchMobile {
    static selector() {
        return '[data-site-search-mobile]';
    }

    constructor(node) {
        this.node = node;
        this.mobileSearchForm = document.querySelector('[data-search-mobile]');

        this.hiddenClass = 'is-hidden';
        this.expandedClass = 'is-expanded';

        this.bindEvents();
    }

    bindEvents() {
        this.node.addEventListener('click', () => {
            if (this.mobileSearchForm.classList.contains(this.hiddenClass)) {
                this.open();
            } else {
                this.close();
            }
        });

        // Close the search when the menu opens
        document.addEventListener('onMenuOpen', () => this.close());
    }

    open() {
        document.dispatchEvent(new Event('onMobileSearchOpen'));
        this.mobileSearchForm.classList.remove(this.hiddenClass);
        this.node.classList.add(this.expandedClass);
        this.node.ariaExpanded = true;
        this.node.ariaLabel = this.node.ariaLabel.replace('Open', 'Close');
    }

    close() {
        if (this.mobileSearchForm.classList.contains(this.hiddenClass)) return;
        this.mobileSearchForm.classList.add(this.hiddenClass);
        this.node.classList.remove(this.expandedClass);
        this.node.ariaExpanded = false;
        this.node.ariaLabel = this.node.ariaLabel.replace('Close', 'Open');
    }
}

export default SiteSearchMobile;
