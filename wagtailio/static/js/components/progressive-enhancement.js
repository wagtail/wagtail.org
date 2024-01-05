class ProgressiveEnhancement {
    // This class is used to hide elements that are only used for progressive enhancement
    // and should be hidden if JS is enabled.

    static selector() {
        return '[data-progressive-enhancement]';
    }

    constructor(node) {
        this.node = node;

        if (this.node) {
            this.node.classList.add('hidden');
        }
    }
}

export default ProgressiveEnhancement;
