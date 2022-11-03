class LoopingVideo {
    static selector() {
        return '[data-looping-video]';
    }

    constructor(node) {
        this.node = node;
        this.toggle = this.toggle.bind(this);
        this.preventAutoplay();
        this.bindEventListeners();
    }

    preventAutoplay() {
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
      if (!mediaQuery.matches || !this.node.autoplay) return;
      this.node.pause();
    }

    bindEventListeners() {
        this.node.addEventListener('click', this.toggle);
        this.node.addEventListener('keydown', (e) => {
            if (e.key !== ' ' && e.key !== 'Enter') return;
            e.preventDefault();
            this.toggle();
        });
    }

    toggle() {
        if (this.node.paused || this.node.ended) {
            this.node.play();
        } else {
            this.node.pause();
        }
    }
}

export default LoopingVideo;
