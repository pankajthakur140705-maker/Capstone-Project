import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

// 🔥 BASE URL (CHANGE ONCE ONLY)
const API = "https://bandhu-ai-backend.onrender.com";

function App() {
  // ---------------------------
  // STATE
  // ---------------------------
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [schemeResponse, setSchemeResponse] = useState(null);

  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState(null);

  // ---------------------------
  // SCHEME SEARCH
  // ---------------------------
  const searchSchemes = () => {
    if (!query.trim()) return;

    setLoading(true);
    setSchemeResponse(null);

    fetch(`${API}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        filters: {}
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setSchemeResponse(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  // ---------------------------
  // CHAT API
  // ---------------------------
  const sendMessage = () => {
    if (!message.trim()) return;

    fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "user1",
        message: message,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setChatResponse(data);
      })
      .catch((err) => console.error(err));
  };

  // ---------------------------
  // UI CARD
  // ---------------------------
  const renderScheme = (s, index) => (
    <div
      key={index}
      style={{
        background: "#222",
        padding: "10px",
        marginTop: "10px",
        borderRadius: "10px",
      }}
    >
      <h4>{s.name}</h4>
      <p>{s.description}</p>
      <small>{s.category}</small>
    </div>
  );

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>Bandhu AI 🚀</h2>

        {/* ---------------- SCHEME SEARCH ---------------- */}
        <div style={{ marginBottom: "40px" }}>
          <h3>Scheme Search</h3>

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter query..."
            style={{
              padding: "10px",
              width: "300px",
              borderRadius: "8px",
            }}
          />

          <br />

          <button onClick={searchSchemes} style={{ padding: "10px 20px" }}>
            Search
          </button>

          {loading && <p>Loading...</p>}

          {schemeResponse?.results && (
            <div style={{ marginTop: "20px", textAlign: "left" }}>
              <h3>Results</h3>
              {schemeResponse.results.map(renderScheme)}
            </div>
          )}
        </div>

        {/* ---------------- CHAT ---------------- */}
        <div style={{ marginTop: "50px" }}>
          <h3>AI Chat</h3>

          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask something..."
            style={{ padding: "10px", width: "300px" }}
          />

          <button onClick={sendMessage} style={{ marginLeft: "10px" }}>
            Send
          </button>

          {chatResponse && (
            <div style={{ marginTop: "20px", maxWidth: "600px" }}>
              {/* CHAT */}
              {chatResponse.type === "chat" && (
                <p style={{ color: "lightblue" }}>
                  {chatResponse.response}
                </p>
              )}

              {/* SCHEMES */}
              {chatResponse.type === "scheme_recommendation" && (
                <div>
                  <p style={{ color: "lightgreen" }}>
                    {chatResponse.response}
                  </p>

                  {chatResponse.data?.map(renderScheme)}
                </div>
              )}
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;