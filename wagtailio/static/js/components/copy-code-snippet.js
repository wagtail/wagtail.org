class CopyCodeSnippet {
    static selector() {
        return '[data-code-snippet]';
    }

    constructor(node) {
        this.node = node;
        this.codeBlock = this.node.querySelector('[data-code-to-copy]');
        this.copyButton = this.node.querySelector('[data-copy-code-button]');
        this.snippet = this.codeBlock ? this.codeBlock.innerText : null;
        this.copiedClass = 'has-copied';
        this.bindEvents();
    }

    bindEvents() {
        this.copyButton.addEventListener('click' , () => {
            navigator.clipboard.writeText(this.snippet).then(
                () => {
                    this.node.classList.add(this.copiedClass);

                    setTimeout(() => {
                        this.node.classList.remove(this.copiedClass);
                    }, 1250);
                }
            )
        })
    }
}

export default CopyCodeSnippet;
