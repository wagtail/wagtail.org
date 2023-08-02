// Wire up light/dark mode button.
document.getElementById('wagtail-theme').addEventListener('click', (event) => {
    document.dispatchEvent(new CustomEvent('theme:toggle-theme-mode', event));
    const theme = localStorage.getItem('wagtail-theme');

    if (theme === 'light') {
        event.target.setAttribute('aria-label', 'Change to Dark Theme');
    } else {
        event.target.setAttribute('aria-label', 'Change to Light Theme');
    }
});
