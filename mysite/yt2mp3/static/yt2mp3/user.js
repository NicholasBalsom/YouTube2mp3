function ThemeToggle() {
    const body = document.body;
    const links = document.querySelectorAll('a');
    const inputs = document.querySelectorAll('input');

    links.forEach((link) => {
        link.classList.toggle('light-mode');
    });
    
    inputs.forEach((input) => {
        input.classList.toggle('light-mode-special');
    });

    body.classList.toggle('light-mode');
}

function BurgerNav() {
    const spans = document.querySelectorAll('span');
    spans.forEach((span) => {
        span.classList.toggle('is-active');
    });
}