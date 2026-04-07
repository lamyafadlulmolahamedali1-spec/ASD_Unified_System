window.PepperVoice = {
    speak: function(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1.1;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }
    }
};
