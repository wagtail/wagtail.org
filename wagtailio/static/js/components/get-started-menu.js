import MicroModal from 'micromodal';

class GetStarted {
    static selector() {
        return '[data-get-started]';
    }

    constructor(node) {
        this.node = node;
        this.modalId = 'get-started-menu';
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

export default GetStarted;
