class CookieMessage {
    static selector() {
        return '[data-cookie-message]';
    }

    // eslint-disable-next-line class-methods-use-this
    getCookie(name) {
        const value = `; ${document.cookie}`;
	    const parts = value.split(`; ${name}=`);
	    if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return false;
    }

    constructor(node) {
        this.node = node;

        if (this.node) {
            this.dismissButton = this.node.querySelector('[data-cookie-dismiss]');

            // If cookie doesn't exists
            if (!this.getCookie('client-cookie')) {
                this.node.classList.add('active');
            }
            this.bindEvents();
        }
    }

    bindEvents() {
        this.dismissButton.addEventListener('click' , (event) => {
            event.preventDefault(); // ensure the href is not used (scrolls user to the top)
            document.cookie = 'client-cookie=agree to cookies;max-age=' + 60*60*24*365;
            this.node.classList.remove('active');
            this.node.classList.add('inactive');
        })
    }
}

export default CookieMessage;
