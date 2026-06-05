<<<<<<< HEAD
const BASE_URL = "http://127.0.0.1:8000";

export const getSchemes = async (data) => {
  const response = await fetch(`${BASE_URL}/schemes/eligible`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error("API Error");
  }

  return await response.json();
=======
const BASE_URL = "http://127.0.0.1:8000";

export const getSchemes = async (data) => {
  const response = await fetch(`${BASE_URL}/schemes/eligible`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error("API Error");
  }

  return await response.json();
>>>>>>> 6ce4515f3c6bb5527f994a20db585a667279390c
};