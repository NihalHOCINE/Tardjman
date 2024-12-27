function switchLanguages() {
    const languages = document.querySelectorAll('.language span');
    const temp = languages[0].innerText;
    languages[0].innerText = languages[1].innerText;
    languages[1].innerText = temp;

    // Update placeholder text
    const input = document.getElementById('input-text');
    input.placeholder = `Enter text in ${languages[0].innerText}`;
}

function translateText() {
    const inputText = document.getElementById('input-text').value;
    const outputDiv = document.getElementById('output-text');

    if (inputText.trim() === '') {
        outputDiv.innerText = 'Please enter a phrase to translate.';
        return;
    }

    // Simulated translation logic
    outputDiv.innerText = `Translated: "${inputText}" (Simulated Translation)`;
}
