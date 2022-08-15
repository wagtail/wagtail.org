class FooterMenuColumn {
    static selector() {
        return '[data-footer-menu-column]';
    }

    constructor(node) {
        this.node = node;
        this.toggleButton = this.node.querySelector('[data-footer-menu-toggle]');
        this.openIcon = this.node.querySelector('[data-footer-open-icon]');
        this.closeIcon = this.node.querySelector('[data-footer-close-icon]');
        this.menuList = this.node.querySelector('[data-footer-menu-list]');
        this.openClass = 'is-open';

        this.bindEvents();
    }

    bindEvents() {
        this.toggleButton.addEventListener('click', () => {
            if (this.node.classList.contains(this.openClass)) {
                this.handleClose();
            } else {
                this.handleOpen();
            }
        })
    }

    handleClose() {
        this.node.classList.remove(this.openClass);
        this.toggleButton.ariaLabel = this.toggleButton.ariaLabel.replace('Close', 'Open');
        this.toggleButton.ariaExpanded = false;
    }

    handleOpen() {
        this.node.classList.add(this.openClass);
        this.toggleButton.ariaLabel = this.toggleButton.ariaLabel.replace('Open', 'Close');
        this.toggleButton.ariaExpanded = true;
    }
}

export default FooterMenuColumn;
