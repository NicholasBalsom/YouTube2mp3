function ThemeToggle() {
    const body = document.body;
    const links = document.querySelectorAll('a');
    const inputs = document.querySelectorAll('input');
    const buttons = document.querySelectorAll('button');

    links.forEach((link) => {
        link.classList.toggle('light-mode');
    });
    
    inputs.forEach((input) => {
        input.classList.toggle('light-mode-special');
    });

    buttons.forEach((button) => {
        button.classList.toggle('light-mode-button');
    });

    body.classList.toggle('light-mode');


}

