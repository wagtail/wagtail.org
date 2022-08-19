class FeatureIndex {
    static selector() {
        return '[data-feature-index]';
    }

    constructor(node) {
        this.node = node;
        this.allFilters = [...this.node.querySelectorAll('[data-feature-filter]')];
        this.allFilterCheckbox = this.node.querySelector('[data-feature-filter-all]')
        this.hiddenClass = 'is-hidden';
        this.allFeatureGroups = [...this.node.querySelectorAll('[data-feature-group]')];

        this.bindEvents();

    bindEvents() {
        this.allFilterCheckbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.resetUI();
            } else {
                // do nothing
            }
        })

        this.allFilters.forEach((filter) => {
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
        const checkedFilters = this.allFilters.filter(filter => filter.checked === false);
        const uncheckedFilters = this.allFilters.filter(filter => filter.checked === true);

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
        this.allFilters.forEach((filter) => {
            const filterCopy = filter;
            filterCopy.checked = false;
        })

        this.allFeatureGroups.forEach(group => group.classList.remove(this.hiddenClass));
    }
}

export default FeatureIndex;
