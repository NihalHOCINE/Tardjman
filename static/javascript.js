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

function speakText(elementId) {
    const textElement = document.getElementById(elementId);
    const text = textElement.value || textElement.innerText;

    if (!text.trim()) {
        alert('No text available to speak!');
        return;
    }

    // Initialize SpeechSynthesis API
    const speech = new SpeechSynthesisUtterance();
    speech.text = text;

    // Detect language of the input text
    const isArabic = /[\u0600-\u06FF]/.test(text); // Check if text contains Arabic characters  
    const isFrench = /[a-zA-ZéèêçàâîôûùÉÈÊÇÀÂÎÔÛÙ]/.test(text); //Check if text contains Latin-based characters

    if (isArabic) {
        speech.lang = 'ar-SA'; // Arabic language
    } else if (isFrench) {
        speech.lang = 'fr-FR'; // French language
    } else {
        speech.lang = 'en-US'; // Fallback to English if no Arabic or French is detected
    }

    // Retrieve available voices
    const voices = window.speechSynthesis.getVoices();

    // Find a matching voice for the detected language
    const matchedVoice = voices.find(voice =>
voice.lang.startsWith(speech.lang.split('-')[0]));
    if (matchedVoice) {
        speech.voice = matchedVoice;
    } else {
        alert(`No voice available for the detected language: ${speech.lang}.`);
    }

    // Speak the text
    window.speechSynthesis.speak(speech);

    // Debugging: Log voice settings and text
    console.log(`Speaking text: "${text}"`);
    console.log(`Using voice: ${matchedVoice ? matchedVoice.name :
"Default"} (lang: ${speech.lang})`);
}

// Ensure voices are loaded
window.speechSynthesis.onvoiceschanged = () => {
    const voices = window.speechSynthesis.getVoices();
    console.log('Available voices:', voices);
};