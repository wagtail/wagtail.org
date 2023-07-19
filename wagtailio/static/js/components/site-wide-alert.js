class SiteWideAlert {
    static selector() {
        return '[data-site-wide-alert]';
    }

    constructor(node) {
        this.node = node;

        if (this.node.dataset.siteWideAlert) {
            this.checkAndInitializeAlert();
        }
      }

    checkAndInitializeAlert() {
        fetch(this.node.dataset.siteWideAlert)
            .then((response) => response.json())
            .then((data) => {
                if (data.text) {
                    this.populateAlert(data);
                }
            })
            .catch(() => {});
    }

    populateAlert(data) {
        if (data.text) {
            const aside = document.createElement("aside");
            aside.classList.add("sitewide-alert");
            document.querySelector('body').classList.add('banner-active');
            aside.innerHTML = data.text;
            this.node.append(aside);
            // get height to prevent whole page restructuring without animation
            document.documentElement.style.setProperty(
                '--banner-height',
                `${this.node.clientHeight}px`,
            );

            if (data.bg_colour) {
                aside.style.backgroundColor = '#' + data.bg_colour;
            }
            if (data.text_colour) {
                aside.style.color =  '#' + data.text_colour;
            }

            if (!(data.bg_colour || data.text_colour)) {
                aside.classList.add('sitewide-alert--default');
            }

            setTimeout(() => {
              aside.classList.add('sitewide-alert--active');
            }, 1);
        }
    }
}

export default SiteWideAlert;
