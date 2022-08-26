class Feature {
    static selector() {
        return '[data-feature]';
    }

    constructor(node) {
        this.node = node;
        this.toggleButton = this.node.querySelector('[data-feature-toggle]');
        this.featureContent = this.node.querySelector('[data-feature-content]');

        this.collapsedClass = 'is-collapsed';

        this.bindEvents();
    }

    bindEvents() {
        this.toggleButton.addEventListener('click', () => {
            if (this.node.classList.contains(this.collapsedClass)) {
                this.handleOpen();
            } else {
                this.handleClose();
            }
        })
    }

    handleOpen() {
        this.node.classList.remove(this.collapsedClass);
        this.toggleButton.ariaLabel = this.toggleButton.ariaLabel.replace('Open', 'Collapse');
    }

    handleClose() {
        this.node.classList.add(this.collapsedClass);
        this.toggleButton.ariaLabel = this.toggleButton.ariaLabel.replace('Collapse', 'Open');
    }
}

export default Feature;
