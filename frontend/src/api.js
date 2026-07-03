const API_BASE = "http://127.0.0.1:8000";

export const startGame = async (category = null) => {
  const url = category
    ? `${API_BASE}/api/start/?category=${category}`
    : `${API_BASE}/api/start/`;

  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to start game");
  return response.json();
};

export const askQuestion = async (sessionId, question) => {
  console.log("Asking:", sessionId, question);  //debug

  const response = await fetch(`${API_BASE}/api/ask/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, question }),
  });

  console.log("Response status:", response.status);  //debug

  if (!response.ok) {
    const errorData = await response.json();
    console.log("Error response:", errorData);  //debug
    throw new Error("Server error");
  }

  return response.json();
};