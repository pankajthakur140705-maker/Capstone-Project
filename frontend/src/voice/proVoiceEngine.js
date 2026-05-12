let recognition = null;
let isRunning = false;

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

export const startProVoiceEngine = (onCommand) => {
  if (!SpeechRecognition) {
    alert("Speech Recognition not supported in this browser");
    return;
  }

  if (isRunning) return; // prevent multiple instances

  recognition = new SpeechRecognition();

  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.lang = "en-IN";

  const WAKE_WORD = "hey bandhu";

  recognition.onresult = (event) => {
    const text =
      event.results[event.results.length - 1][0].transcript
        .toLowerCase()
        .trim();

    console.log("🎤 Heard:", text);

    // Wake word logic (JARVIS mode)
    if (!isRunning) return;

    if (text.includes(WAKE_WORD)) {
      console.log("🟢 Wake word detected");
      return;
    }

    // Ignore empty noise
    if (!text) return;

    onCommand(text);
  };

  recognition.onerror = (err) => {
    console.error("Voice error:", err);
  };

  recognition.onend = () => {
    // Auto-restart for always-on assistant
    if (isRunning) {
      recognition.start();
    }
  };

  isRunning = true;
  recognition.start();
};

export const stopProVoiceEngine = () => {
  isRunning = false;

  if (recognition) {
    recognition.onend = null;
    recognition.stop();
    recognition = null;
  }
};