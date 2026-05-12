import { useState, useEffect, useRef } from "react";
import "./App.css";

import { speakText } from "./voice/voiceAssistant";
import { startProVoiceEngine, stopProVoiceEngine } from "./voice/proVoiceEngine";

const API = "http://127.0.0.1:8000";

function App() {

  // ================= CORE STATE =================
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [voiceActive, setVoiceActive] = useState(false);
  const [status, setStatus] = useState("IDLE");
  const [logs, setLogs] = useState([]);

  // ================= SAFETY REFS =================
  const lastCommandRef = useRef("");
  const isProcessingRef = useRef(false);

  // ================= LOG ENGINE =================
  const addLog = (type, text) => {
    setLogs(prev => [
      { type, text, time: new Date().toLocaleTimeString() },
      ...prev.slice(0, 10)
    ]);
  };

  // ================= AI ENGINE =================
  const sendMessage = async (textOverride = null) => {

    const finalMessage = (textOverride || message)?.trim();
    if (!finalMessage || isProcessingRef.current) return;

    try {
      isProcessingRef.current = true;

      setLoading(true);
      setStatus("THINKING");
      setError("");

      addLog("USER", finalMessage);

      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user1",
          message: finalMessage,
        }),
      });

      const data = await res.json();
      setChatResponse(data);

      setStatus("RESPONDING");

      if (data?.response) {
        addLog("AI", data.response);
        speakText(data.response);
      }

    } catch (err) {
      console.error(err);
      setError("❌ AI Engine Failed");
      setStatus("ERROR");
    } finally {
      setLoading(false);
      setStatus("LISTENING");

      setTimeout(() => {
        isProcessingRef.current = false;
      }, 800);
    }
  };

  // ================= VOICE ENGINE =================
  useEffect(() => {

    setStatus("STARTING VOICE ENGINE");

    startProVoiceEngine(async (text) => {

      const clean = text?.toLowerCase()?.trim();
      if (!clean) return;

      // prevent duplicate execution
      if (clean === lastCommandRef.current) return;
      lastCommandRef.current = clean;

      setMessage(clean);
      await sendMessage(clean);

    });

    setVoiceActive(true);
    setStatus("LISTENING");

    return () => stopProVoiceEngine();

  }, []);

  // ================= TOGGLE VOICE =================
  const toggleVoice = () => {
    if (voiceActive) {
      stopProVoiceEngine();
      setVoiceActive(false);
      setStatus("OFFLINE");
    } else {
      startProVoiceEngine(async (text) => {
        setMessage(text);
        await sendMessage(text);
      });

      setVoiceActive(true);
      setStatus("LISTENING");
    }
  };

  // ================= UI =================
  return (
    <div style={{
      minHeight: "100vh",
      background: "#0f1117",
      color: "white",
      padding: "25px",
      fontFamily: "Arial"
    }}>

      {/* HEADER */}
      <h1 style={{ textAlign: "center", color: "#00d4ff" }}>
        🚀 BANDHU AI — FINAL JARVIS ENGINE
      </h1>

      {/* STATUS BAR */}
      <div style={{
        textAlign: "center",
        padding: "10px",
        margin: "10px",
        background: "#1a1a1a",
        borderRadius: "10px"
      }}>
        <h3>
          STATUS:{" "}
          <span style={{
            color:
              status === "LISTENING" ? "lime" :
              status === "THINKING" ? "orange" :
              status === "RESPONDING" ? "#00d4ff" :
              status === "ERROR" ? "red" : "gray"
          }}>
            {status}
          </span>
        </h3>

        <button
          onClick={toggleVoice}
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            background: voiceActive ? "red" : "green",
            color: "white",
            border: "none",
            cursor: "pointer"
          }}
        >
          {voiceActive ? "STOP VOICE" : "START VOICE"}
        </button>
      </div>

      {/* ERROR */}
      {error && (
        <p style={{ color: "red", textAlign: "center" }}>
          {error}
        </p>
      )}

      {/* INPUT */}
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Speak or type command..."
          style={{
            padding: "12px",
            width: "60%",
            borderRadius: "8px"
          }}
        />

        <button
          onClick={() => sendMessage()}
          style={{
            marginLeft: "10px",
            padding: "12px 20px",
            background: "#00d4ff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          EXECUTE
        </button>
      </div>

      {/* AI RESPONSE */}
      {chatResponse && (
        <div style={{
          marginTop: "25px",
          background: "#1e1e1e",
          padding: "15px",
          borderRadius: "10px"
        }}>
          <h3>🤖 AI RESPONSE</h3>
          <p>{chatResponse.response}</p>
        </div>
      )}

      {/* COMMAND HISTORY */}
      <div style={{
        marginTop: "30px",
        background: "#151515",
        padding: "15px",
        borderRadius: "10px"
      }}>
        <h3>📜 COMMAND HISTORY</h3>

        {logs.map((l, i) => (
          <p key={i} style={{ fontSize: "13px", opacity: 0.9 }}>
            [{l.time}] <b>{l.type}:</b> {l.text}
          </p>
        ))}
      </div>

    </div>
  );
}

export default App;