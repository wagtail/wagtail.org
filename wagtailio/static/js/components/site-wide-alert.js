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
        // Skip alert for /wagtail-space paths
        if (window.location.pathname.startsWith('/wagtail-space')) {
            return;
        }
        
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
            
            // Create a wrapper for the content
            const contentWrapper = document.createElement("div");
            contentWrapper.classList.add("sitewide-alert__wrapper");
            
            // Add the alert text
            const textContainer = document.createElement("div");
            textContainer.classList.add("sitewide-alert__text");
            textContainer.innerHTML = data.text;
            contentWrapper.appendChild(textContainer);
            
            // Add CTA button if provided
            if (data.cta_text && data.cta_url) {
                const ctaButton = document.createElement("a");
                ctaButton.href = data.cta_url;
                ctaButton.classList.add("sitewide-alert__cta");
                ctaButton.textContent = data.cta_text;
                
                // Apply inverted colors for custom themes
                if (data.bg_colour && data.text_colour) {
                    const bgColor = '#' + data.bg_colour;
                    const textColor = '#' + data.text_colour;
                    
                    ctaButton.style.backgroundColor = textColor;
                    ctaButton.style.color = bgColor;
                }
                
                contentWrapper.appendChild(ctaButton);
            }
            
            aside.appendChild(contentWrapper);
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
                aside.style.color = '#' + data.text_colour;
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