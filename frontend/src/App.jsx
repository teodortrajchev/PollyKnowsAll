import { useState } from "react";
import { startGame, askQuestion } from "./api";
import "./App.css";

const CATEGORIES = ["Animals", "People", "Countries", "Abstract"];

function App() {
  const [category, setCategory] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("Погоди ја мојата тајна!");
  const [loading, setLoading] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [numQuestions, setNumQuestions] = useState(0);
  const [error, setError] = useState(null);

  const handleCategorySelect = async (cat) => {
    setError(null);
    setLoading(true);
    try {
      const data = await startGame(cat);
      setSessionId(data.session_id);
      setCategory(cat);
      setAnswer("Погоди ја мојата тајна!");
      setGameOver(false);
      setNumQuestions(0);
    } catch (err) {
      setError("⚠️ Не може да се поврзе со серверот");
    }
    setLoading(false);
  };

  const handleAsk = async () => {
    if (!question.trim() || !sessionId || loading) return;

    setLoading(true);
    setAnswer("...");
    setError(null);

    try {
      const data = await askQuestion(sessionId, question);
      setAnswer(data.answer);
      setNumQuestions(data.num_questions);
      setGameOver(data.game_over);
    } catch (err) {
      setError("⚠️ Грешка при поврзување со серверот");
    }

    setLoading(false);
    setQuestion("");
  };

  const handleRestart = () => {
    setCategory(null);
    setSessionId(null);
    setAnswer("Погоди ја мојата тајна!");
    setNumQuestions(0);
    setQuestion("");
    setGameOver(false);
    setError(null);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleAsk();
  };

  // Category picker screen
  if (!category) {
    return (
      <div className="container">
        <h1 className="title">🤔 Погоди го зборот!</h1>
        <h2>Избери категорија:</h2>
        {error && <p className="error">{error}</p>}
        <div className="categories">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              className="button"
              onClick={() => handleCategorySelect(cat)}
              disabled={loading}
            >
              {loading ? "..." : cat}
            </button>
          ))}
        </div>
      </div>
    );
  }

  // Game screen
  return (
    <div className="container">
      <h1 className="title">🤔 Погоди го зборот!</h1>
      <p className="counter">Категорија: {category} | Прашања: {numQuestions}</p>

      <div className="bubble">
        {loading ? <LoadingDots /> : answer}
      </div>

      <img
        src="https://cdn-icons-png.flaticon.com/512/616/616430.png"
        alt="character"
        className="character"
      />

      {error && <p className="error">{error}</p>}

      {!gameOver && (
        <>
          <input
            className="input"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Постави прашање..."
            disabled={loading}
          />
          <button
            className="button"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "Размислувам..." : "Прашај"}
          </button>
        </>
      )}

      {gameOver && (
        <div className="game-over">
          <h2>🎉 Браво! Победивте за {numQuestions} прашања!</h2>
          <button className="button" onClick={handleRestart}>
            Играј пак
          </button>
        </div>
      )}
    </div>
  );
}

function LoadingDots() {
  return (
    <span className="dots">
      <span>.</span>
      <span>.</span>
      <span>.</span>
    </span>
  );
}

export default App;