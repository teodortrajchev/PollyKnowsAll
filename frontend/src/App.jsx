import { useState } from "react";
import { startGame, askQuestion } from "./api";
import "./App.css";

const CATEGORIES = ["Animals", "People", "Countries", "Abstract"];

const PROXIMITY_CONFIG = {
  BURNING: { label: "Многу топло!", percent: 100, color: "#ff2200", image: "/Polly_Win.png" },
  HOT:     { label: "Топло",        percent: 75,  color: "#ff6600", image: "/polly_hot.png" },
  WARM:    { label: "Млако",        percent: 50,  color: "#f0c000", image: "/Polly_warm.png" },
  COLD:    { label: "Ладно",        percent: 25,  color: "#00aaff", image: "/polly_cold.jpeg" },
};

function App() {
  const [category, setCategory] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("Погоди ја мојата тајна!");
  const [loading, setLoading] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [numQuestions, setNumQuestions] = useState(0);
  const [error, setError] = useState(null);
  const [proximity, setProximity] = useState(null);
  const [coins, setCoins] = useState(0);
  const [coinsEarned, setCoinsEarned] = useState(0);

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
      setProximity(null);
      setCoins(data.coins);
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
      setProximity(data.proximity);
      setCoins(data.coins);
      if (data.coins_earned) setCoinsEarned(data.coins_earned);
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
    setProximity(null);
    setCoinsEarned(0);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleAsk();
  };

  const currentImage = proximity
    ? PROXIMITY_CONFIG[proximity].image
    : "/polly_hot.png";

  // Category picker
  if (!category) {
    return (
      <div className="page">
        <nav className="navbar">
          <div className="navbar-left">
            <img src="/polly_cold.jpeg" alt="polly" className="navbar-icon" />
            <span className="navbar-title">POLLY KNOWS ALL</span>
          </div>
          <div className="navbar-right">
            <span className="navbar-coins">coins: {coins}</span>
          </div>
        </nav>

        <div className="grid-bg">
          <div className="category-screen">
            <h2 className="category-heading">Избери категорија:</h2>
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
        </div>
      </div>
    );
  }

  // Game screen
  return (
    <div className="page">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-left">
          <img src="/polly_cold.jpeg" alt="polly" className="navbar-icon" />
          <span className="navbar-title">POLLY KNOWS ALL</span>
        </div>
        <div className="navbar-right">
          <span className="navbar-category">{category}</span>
          <span className="navbar-coins">coins: {coins}</span>
          <span className="navbar-counter">прашања: {numQuestions}</span>
        </div>
      </nav>

      {/* Main grid area */}
      <div className="grid-bg">
        {gameOver ? (
          <div className="game-area">
            <div className="character-bubble-row">
              <img src="/Polly_Win.png" alt="polly win" className="character" />
              <div className="speech-bubble">
                <p>SQUAWK! Браво! Победивте!</p>
                <p className="coins-earned">+ {coinsEarned} Coins</p>
              </div>
            </div>
            <button className="button" onClick={handleRestart}>
              Играј пак
            </button>
          </div>
        ) : (
          <div className="game-area">
            {/* Parrot + speech bubble */}
            <div className="character-bubble-row">
              <img src={currentImage} alt="polly" className="character" />
              <div className="speech-bubble">
                {loading ? <LoadingDots /> : answer}
              </div>
            </div>

            {/* Proximity bar */}
            {proximity && (
              <div className="proximity-wrapper">
                <div
                  className="proximity-label"
                  style={{ color: PROXIMITY_CONFIG[proximity].color }}
                >
                  {PROXIMITY_CONFIG[proximity].label}
                </div>
                <div className="proximity-bar-track">
                  <div
                    className="proximity-bar-fill"
                    style={{
                      width: `${PROXIMITY_CONFIG[proximity].percent}%`,
                      backgroundColor: PROXIMITY_CONFIG[proximity].color,
                    }}
                  />
                </div>
              </div>
            )}

            {error && <p className="error">{error}</p>}

            {/* Input row */}
            <div className="input-row">
              <input
                className="input"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Постави прашање..."
                disabled={loading}
              />
              <button
                className="button ask-button"
                onClick={handleAsk}
                disabled={loading}
              >
                {loading ? "..." : "ASK!"}
              </button>
            </div>
          </div>
        )}
      </div>
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