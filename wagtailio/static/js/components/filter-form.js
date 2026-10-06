class FilterForm {
    static selector() {
        return '[data-filter-form]';
    }

    constructor(node) {
        this.node = node;
        this.allFilter = this.node.querySelector('[data-filter-all]');
        this.filterElements = this.node.querySelectorAll(
            'select, input[type="checkbox"]',
        );

        this.bindEvents();
    }

    bindEvents() {
        this.filterElements.forEach((element) => {
            element.addEventListener('change', () => {
                if (element === this.allFilter) {
                    // 'All' has no value to submit, so go to the unfiltered page
                    window.location.assign(this.node.action);
                } else {
                    // Submit the form when a value is selected
                    this.node.submit();
                }
            });
        });
    }
}

export default FilterForm;
