import { useState } from "react";
import UserForm from "./components/UserForm";
import SchemeResults from "./components/SchemeResults";
import LoadingBrain from "./components/LoadingBrain";
import { getSchemes } from "./services/api";
import "./App.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [schemes, setSchemes] = useState([]);
  const [explanation, setExplanation] = useState("");

  const handleCheck = async (formData) => {
    setLoading(true);
    setSchemes([]);

    try {
      const result = await getSchemes(formData);
      setSchemes(result.schemes);
      setExplanation(result.explanation);
    } catch (err) {
      console.log("Error:", err);
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>🧠 Scheme Brain AI</h1>

      <UserForm onSubmit={handleCheck} />

      {loading && <LoadingBrain />}

      {!loading && schemes.length > 0 && (
        <SchemeResults schemes={schemes} explanation={explanation} />
      )}
    </div>
  );
}

export default App;