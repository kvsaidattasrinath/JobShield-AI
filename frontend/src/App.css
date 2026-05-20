import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);

  const analyzeJob = async () => {
    try {
      const response = await axios.post(
        "https://jobshield-ai-backend.onrender.com/predict",
        {
          text: jobText,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    }
  };

  return (
    <div className="container">
      <h1 className="title">JobShield AI</h1>

      <p className="subtitle">
        AI-powered fake job and scam detection system
      </p>

      <textarea
        className="textarea"
        placeholder="Paste job description here..."
        value={jobText}
        onChange={(e) => setJobText(e.target.value)}
      />

      <button className="button" onClick={analyzeJob}>
        Analyze Job
      </button>

      {result && (
        <div className="result-card">
          <h2>
            Prediction:
            <span
              className={
                result.prediction === "Fake Job"
                  ? "fake"
                  : "real"
              }
            >
              {" "}
              {result.prediction}
            </span>
          </h2>

          <p>
            <strong>Confidence:</strong>{" "}
            {result.final_confidence}%
          </p>

          <div className="flags">
            {result.flags?.map((flag, index) => (
              <div key={index} className="flag">
                {flag}
              </div>
            ))}
          </div>

          <p style={{ marginTop: "20px" }}>
            {result.ai_explanation}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;