// ===============================
// VOICE ASSISTANT (FINAL VERSION)
// ===============================

let recognition = null;

// ===============================
// START VOICE RECOGNITION
// ===============================
export const startVoiceRecognition = (onResult) => {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Speech Recognition not supported in this browser");
    return;
  }

  recognition = new SpeechRecognition();

  recognition.continuous = false; // stable single command mode
  recognition.interimResults = false;
  recognition.lang = "en-IN";

  recognition.onstart = () => {
    console.log("🎤 Listening...");
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    console.log("User said:", text);

    if (onResult) onResult(text);
  };

  recognition.onerror = (err) => {
    console.error("Voice error:", err);
  };

  recognition.onend = () => {
    console.log("🛑 Voice recognition ended");
  };

  recognition.start();
};

// ===============================
// STOP VOICE RECOGNITION
// ===============================
export const stopVoiceRecognition = () => {
  if (recognition) {
    recognition.stop();
    recognition = null;
  }
};

// ===============================
// TEXT TO SPEECH (AI VOICE OUTPUT)
// ===============================
export const speakText = (text, onDone) => {
  if (!text) return;

  const synth = window.speechSynthesis;

  // stop previous speech (important for AI chat)
  synth.cancel();

  const utterance = new SpeechSynthesisUtterance(text);

  utterance.lang = "en-IN";
  utterance.rate = 1;
  utterance.pitch = 1;
  utterance.volume = 1;

  utterance.onend = () => {
    console.log("🔊 AI finished speaking");
    if (onDone) onDone();
  };

  synth.speak(utterance);
};