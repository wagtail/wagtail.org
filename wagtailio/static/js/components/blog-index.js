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
        this.showFilterButton = document.querySelector('[data-blog-index-show-filters]');
        this.showFilterButtonText = this.showFilterButton.querySelector("p");
        this.hiddenClass = 'is-hidden';

        // Progressive enhancement, display "show filters" button and hide filters
        this.node.classList.add(this.hiddenClass);
        this.showFilterButton.classList.remove(this.hiddenClass);

        // Handle when a non-all filter has been selected
        if (!this.allFilterCheckbox.checked) {
            this.showFilterButtonText.innerText = "Hide filters"
            this.node.classList.remove(this.hiddenClass);
        }  
        this.bindEvents();
    }

    bindEvents() {
        // Toggle visibility of filters
        this.showFilterButton.addEventListener('click', () => {
            if (this.node.classList.contains(this.hiddenClass)){
                this.node.classList.remove(this.hiddenClass);
                this.showFilterButtonText.innerText = "Hide filters"
            }
            else {
                this.node.classList.add(this.hiddenClass);
                this.showFilterButtonText.innerText = "Show filters"
            }
        })
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
