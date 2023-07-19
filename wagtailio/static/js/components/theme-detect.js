// Wire up light/dark mode button.
document.getElementById('wagtail-theme').addEventListener('click', (event) => {
    document.dispatchEvent(new CustomEvent('theme:toggle-theme-mode', event));
});
