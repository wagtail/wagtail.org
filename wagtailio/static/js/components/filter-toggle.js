class FilterToggle {
    static selector() {
        return '[data-filter-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.toggleButton = this.node.querySelector('[data-filter-button]');
        this.openClass = 'is-open';

        this.bindEvents();
    }

    bindEvents() {
      this.toggleButton.addEventListener('click', (e) => {
            e.preventDefault();
            if (this.node.classList.contains(this.openClass)) {
                this.handleClose();
            } else {
                this.handleOpen();
            }
        })
    }

    handleClose() {

        this.node.classList.remove(this.openClass);
        this.toggleButton.ariaExpanded = false;
    }

    handleOpen() {
        this.node.classList.add(this.openClass);
        this.toggleButton.ariaExpanded = true;
    }
}

export default FilterToggle;
