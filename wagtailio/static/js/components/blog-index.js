class BlogIndex {
    static selector() {
        return '[data-blog-index]';
    }

    constructor(node) {
        this.node = node;
        // 'all' checkbox input
        this.allFilterCheckbox = this.node.querySelector('[data-blog-filter-all]');
        // other checkbox inputs not including 'all'
        this.filterCheckboxes = [...this.node.querySelectorAll('[data-blog-filter]')];
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

                    this.updateFilterGroups();
                } else {
                    this.updateFilterGroups();
                }
            })
        })
    }

    // Loop over filters and hide or show group depending on if checkbox is 'checked'
    updateFilterGroups() {
        const uncheckedFilters = this.filterCheckboxes.filter(filter => filter.checked === true);

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
    }
}

export default BlogIndex;
