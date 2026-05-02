import { useState, useEffect } from "react";
import { startGame, askQuestion } from "./api";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("Guess my secret!");
  const [loading, setLoading] = useState(false);
  const [gameOver, setGameOver] = useState(false);

  const sessionId = "user1";

  // start game on load
  useEffect(() => {
    startGame(sessionId);
  }, []);

  const handleAsk = async () => {
    if (!question) return;

    setLoading(true);
    setAnswer("..."); // placeholder

    try {
      const data = await askQuestion(sessionId, question);

      setAnswer(data.answer);
      setGameOver(data.game_over);
    } catch (err) {
      setAnswer("⚠️ Error connecting to server");
    }

    setLoading(false);
    setQuestion("");
  };

  return (
    <div className="container">
      <div className="bubble">
        {loading ? <LoadingDots /> : answer}
      </div>

      <img
        src="https://cdn-icons-png.flaticon.com/512/616/616430.png"
        alt="character"
        className="character"
      />

      {!gameOver && (
        <>
          <input
            className="input"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question..."
            disabled={loading}
          />

          <button
            className="button"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </>
      )}

      {gameOver && <h2>🎉 Game Over!</h2>}
    </div>
  );
}

function LoadingDots() {
  return (
    <span className="dots">
      <span>Loading.</span>
      <span>.</span>
      <span>.</span>
    </span>
  );
}

export default App;