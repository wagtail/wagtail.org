// See https://github.com/pa11y/pa11y-ci#configuration
module.exports = {
    defaults: {
        standard: 'WCAG2AA',
        runners: ['axe'],
        // Axe can't always work out colours, for example behind pseudo-elements.
        // Those results need a manual check, so report them as warnings.
        levelCapWhenNeedsReview: 'warning',
    },
};
