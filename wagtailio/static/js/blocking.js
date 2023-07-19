/**
 * IMPORTANT: This script will block the DOM from loading, only add critical path JS here.
 */

/**
 * Set and store dark/light (theme) mode.
 *
 * Mode will be set to be one of "light" or "dark", by default the resolved
 * theme mode will be flipped (e.g. light to dark).
 *
 * @param {Event} event - is for usage with event listeners, and indicates the user has manually clicked a button
 * @param {object?} options - additional options param when called explicitly
 * @param {boolean?} options.isInitial - if true the current value will be resolved & set NOT toggled
 */
function updateThemeMode(event, { isInitial = false } = {}) {
    const DARK = 'dark';
    const LIGHT = 'light';
    const STORAGE_KEY = 'wagtail-theme';

    let currentMode;
    let applyMode;
    let savedThemeMode;

    // safely request local storage - if cookies/storage is disabled it should not error
    try {
        savedThemeMode = localStorage.getItem(STORAGE_KEY);
    } catch (error) {
        // eslint-disable-next-line no-console
        console.warn('Unable to read theme from localStorage', error);
    }

    // find the current mode from existing storage or browser preference
    if (savedThemeMode) {
        // note - do not assume correct format of local storage
        currentMode = savedThemeMode === LIGHT ? LIGHT : DARK;
    } else {
        // fall back on browser media for first toggle
        const prefersDarkMode = window.matchMedia(
            '(prefers-color-scheme:dark)',
        ).matches;

        currentMode = prefersDarkMode ? DARK : LIGHT;
    }

    // if running initially - do not 'flip' - instead apply current mode
    if (isInitial) {
        applyMode = currentMode === DARK ? DARK : LIGHT;
    } else {
        applyMode = currentMode === DARK ? LIGHT : DARK;
    }

    // set applied mode to the DOM
    document.body.classList.toggle('theme-dark', applyMode === DARK);

    // only store value if already stored OR was triggered by an actual click
    if (savedThemeMode || event) {
        try {
            localStorage.setItem(STORAGE_KEY, applyMode);
        } catch (error) {
            // eslint-disable-next-line no-console
            console.warn('Unable to store theme in localStorage', error);
        }
    }
}

/**
 * Apply user's saved light/dark preference, or fall back to browser setting.
 * Load light/dark preference before DOMContentLoaded so the user does not see a
 * flash during theme initialisation.
 */
updateThemeMode(null, { isInitial: true });

/**
 * Set up event listener for other manual toggling.
 */
document.addEventListener('theme:toggle-theme-mode', updateThemeMode, {
    passive: true,
});
