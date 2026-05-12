const API = "http://127.0.0.1:8000";

// ===============================
// SIMPLE MEMORY (SESSION CONTEXT)
// ===============================
let memory = [];

const MAX_MEMORY = 8;

// ===============================
// SAVE CONTEXT
// ===============================
const saveToMemory = (role, text) => {
  memory.push({ role, text });

  if (memory.length > MAX_MEMORY) {
    memory.shift();
  }
};

// ===============================
// FORMAT CONTEXT FOR BACKEND
// ===============================
const getContext = () => {
  return memory.map(m => `${m.role}: ${m.text}`).join("\n");
};

// ===============================
// MAIN CHAT ENGINE
// ===============================
export const askAI = async (userText) => {

  saveToMemory("user", userText);

  const context = getContext();

  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: "jarvis-user",
      message: userText,
      context: context   // 🔥 IMPORTANT UPGRADE
    }),
  });

  const data = await res.json();

  saveToMemory("ai", data.response);

  return data;
};

// ===============================
// RESET MEMORY
// ===============================
export const resetChatMemory = () => {
  memory = [];
};