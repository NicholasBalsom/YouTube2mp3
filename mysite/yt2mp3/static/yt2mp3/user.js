//This function is called whenever the button is clicked
function ThemeToggle() {
    //makes constant variables for all document elements selected
    const body = document.body;
    const texts = document.querySelectorAll(['h1', 'p', 'a'])
    const inputs = document.querySelectorAll(['input', 'label']);
    const buttons = document.querySelectorAll('button');

    //For loop for each element in the lit, toggles css decorator 
    texts.forEach((text) => {
        text.classList.toggle('light-mode-text');
    });
    //For loop for each element in the lit, toggles css decorator 
    inputs.forEach((input) => {
        input.classList.toggle('light-mode-special');
    });
    //For loop for each element in the lit, toggles css decorator 
    buttons.forEach((button) => {
        button.classList.toggle('light-mode-button');
    });
    //Toggles the css decorator for body elements not contained in a div
    body.classList.toggle('light-mode');
}