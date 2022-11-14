class FeatureIndex {
    static selector() {
        return '[data-feature-index]';
    }

    constructor(node) {
        this.node = node;
        // 'all' checkbox input
        this.allFilterCheckbox = this.node.querySelector('[data-feature-filter-all]');
        // other checkbox inputs not including 'all'
        this.filterCheckboxes = [...this.node.querySelectorAll('[data-feature-filter]')];
        this.allFeatureGroups = [...this.node.querySelectorAll('[data-feature-group]')];
        this.hiddenClass = 'is-hidden';

        this.bindEvents();
    }

    bindEvents() {
        // 'all' filter checkbox
        this.allFilterCheckbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.resetUI();
            } else {
                // Don't uncheck if it's the only one checked
                this.allFilterCheckbox.checked = true;
            }
        })

        // Other filter checkboxes not including 'all'
        this.filterCheckboxes.forEach((filter) => {
            filter.addEventListener('change', (e) => {
                if (e.target.checked) {
                    // Uncheck 'all' checkbox
                    this.allFilterCheckbox.checked = false;

                    this.handleShowGroup(e.target);
                    this.updateFilterGroups();
                } else {
                    this.handleHideGroup(e.target);
                    this.updateFilterGroups();
                }
            })
        })
    }

    // Show an individual group
    handleShowGroup(item) {
        this.node.querySelector(`[data-feature-group="${item.id}"]`).classList.remove(this.hiddenClass);
    }

    // Hide an individual group
    handleHideGroup(item) {
        this.node.querySelector(`[data-feature-group="${item.id}"]`).classList.add(this.hiddenClass);
    }

    // Loop over filters and hide or show group depending on if checkbox is 'checked'
    updateFilterGroups() {
        const checkedFilters = this.filterCheckboxes.filter(filter => filter.checked === false);
        const uncheckedFilters = this.filterCheckboxes.filter(filter => filter.checked === true);

        checkedFilters.forEach(filterGroup => {
            this.node.querySelector(`[data-feature-group="${filterGroup.id}"]`).classList.add(this.hiddenClass);
        })

        if (uncheckedFilters.length === 0) {
            this.allFilterCheckbox.checked = true;
            this.resetUI();
        }
    }

    // Untick all filters - show all groups
    resetUI() {
        this.filterCheckboxes.forEach((filter) => {
            const filterCopy = filter;
            filterCopy.checked = false;
        })

        this.allFeatureGroups.forEach(group => group.classList.remove(this.hiddenClass));
    }
}

export default FeatureIndex;
