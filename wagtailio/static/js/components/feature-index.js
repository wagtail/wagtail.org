class FeatureIndex {
    static selector() {
        return '[data-feature-index]';
    }

    constructor(node) {
        this.node = node;
        this.allFilters = [...this.node.querySelectorAll('[data-feature-filter]')];
        // this.allFilterCheckbox = this.allFilters.find(filter => filter.id === 'all');
        this.hiddenClass = 'is-hidden';
        // this.allFeatureGroups = [...this.node.querySelectorAll('[data-feature-group]')];

        this.bindEvents();

    bindEvents() {
        this.allFilters.forEach((filter) => {
            filter.addEventListener('change', (e) => {
                if (e.target.checked) {
                    // this.allFilterCheckbox.checked = false;
                    this.handleShowGroup(e.target);
                    this.updateFilterGroups();
                } else {
                    this.handleHideGroup(e.target);
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

        checkedFilters.forEach(filterGroup => {
            this.node.querySelector(`[data-feature-group="${filterGroup.id}"]`).classList.add(this.hiddenClass);
        })
    }
}

export default FeatureIndex;
