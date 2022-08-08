import MicroModal from 'micromodal';

class SiteSearch {
    static selector() {
        return '[data-site-search]';
    }

    constructor(node) {
        this.node = node;
        this.modalId = 'site-search-modal';
        this.bindEvents();
    }

    bindEvents() {
        this.node.addEventListener('click', () => {
            this.openMenu();
        })
    }

    openMenu() {
        MicroModal.show(this.modalId, {
            awaitCloseAnimation: true,
        });
    }
}

export default SiteSearch;
