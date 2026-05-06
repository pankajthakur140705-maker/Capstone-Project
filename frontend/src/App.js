import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  // ---------------------------
  // SCHEME SEARCH STATE
  // ---------------------------
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [schemeResponse, setSchemeResponse] = useState(null);

  // ---------------------------
  // CHAT STATE
  // ---------------------------
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState(null);

  // ---------------------------
  // SCHEME SEARCH API
  // ---------------------------
  const searchSchemes = () => {
    if (!query.trim()) return;

    setLoading(true);
    setSchemeResponse(null);

    fetch("http://127.0.0.1:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
        filters: {},
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
  // CHAT API (UPDATED)
  // ---------------------------
  const sendMessage = () => {
    if (!message.trim()) return;

    fetch("http://127.0.0.1:8000/ai", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
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
  // UI
  // ---------------------------
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>Bandhu AI 🚀</h2>

        {/* ========================= */}
        {/* SCHEME SEARCH SECTION */}
        {/* ========================= */}
        <div style={{ marginBottom: "40px" }}>
          <h3>Scheme Search</h3>

          <input
            type="text"
            placeholder="Enter query (e.g. education scheme)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              padding: "10px",
              width: "300px",
              borderRadius: "8px",
              border: "none",
              marginBottom: "10px",
            }}
          />

          <br />

          <button onClick={searchSchemes} style={{ padding: "10px 20px" }}>
            Search Schemes
          </button>

          {loading && <p>Loading...</p>}

          {/* SCHEME RESULTS */}
          {schemeResponse && (
            <div style={{ marginTop: "20px", maxWidth: "600px", textAlign: "left" }}>
              <h3>Results</h3>

              {schemeResponse.schemes.map((s, index) => (
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
              ))}
            </div>
          )}
        </div>

        {/* ========================= */}
        {/* CHAT SECTION */}
        {/* ========================= */}
        <div style={{ marginTop: "50px" }}>
          <h3>AI Chat</h3>

          <input
            type="text"
            value={message}
            placeholder="Ask something..."
            onChange={(e) => setMessage(e.target.value)}
            style={{
              padding: "10px",
              width: "300px",
              borderRadius: "8px",
            }}
          />

          <button onClick={sendMessage} style={{ marginLeft: "10px" }}>
            Send
          </button>

          {/* CHAT RESPONSE */}
          {chatResponse && (
            <div style={{ marginTop: "20px", maxWidth: "600px" }}>
              
              {/* NORMAL CHAT */}
              {chatResponse.type === "chat" && (
                <p style={{ color: "lightblue" }}>
                  {chatResponse.reply}
                </p>
              )}

              {/* SCHEME RESPONSE */}
              {chatResponse.type === "scheme_response" && (
                <div>
                  <p style={{ color: "lightgreen" }}>
                    {chatResponse.reply}
                  </p>

                  {chatResponse.results.map((s, index) => (
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
                  ))}
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