const BASE_URL = "http://127.0.0.1:8000/api";

export async function startGame(sessionId) {
  await fetch(`${BASE_URL}/start/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ session_id: sessionId })
  });
}

export async function askQuestion(sessionId, question) {
  const res = await fetch(`${BASE_URL}/ask/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      session_id: sessionId,
      question: question
    })
  });

  if (!res.ok) {
    throw new Error("Server error");
  }

  return await res.json();
}