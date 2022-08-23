import MicroModal from 'micromodal';

class SiteSearchDesktop {
    static selector() {
        return '[data-site-search-desktop]';
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

export default SiteSearchDesktop;
