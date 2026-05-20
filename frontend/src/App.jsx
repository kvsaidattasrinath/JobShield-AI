import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [jobText, setJobText] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [result, setResult] = useState(null);

  // ANALYZE FUNCTION
  const analyzeJob = async () => {

    try {

      const response = await axios.post(
        "https://jobshield-ai-backend.onrender.com/predict",
        {
          text: jobText,
          url: jobUrl,
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert("Backend connection failed");
    }
  };

  // RESET FUNCTION
  const resetFields = () => {

    setJobText("");
    setJobUrl("");
    setResult(null);
  };

  return (

    <div className="container">

      <h1 className="title">
        JobShield AI
      </h1>

      <p className="subtitle">
        AI-powered fake job and scam detection system
      </p>

      {/* URL INPUT */}
      <input
        className="textarea"
        type="text"
        placeholder="Paste Job URL here..."
        value={jobUrl}
        onChange={(e) => setJobUrl(e.target.value)}
      />

      {/* JOB DESCRIPTION */}
      <textarea
        className="textarea"
        placeholder="Paste job description here..."
        value={jobText}
        onChange={(e) => setJobText(e.target.value)}
      />

      {/* ANALYZE BUTTON */}
      <button
        className="button"
        onClick={analyzeJob}
      >
        Analyze Job
      </button>

      {/* RESET BUTTON */}
      <button
        className="button"
        onClick={resetFields}
        style={{
          marginTop: "10px",
          background: "#334155"
        }}
      >
        Reset
      </button>

      {/* RESULT */}
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

          {/* FLAGS */}
          <div className="flags">

            {result.detected_flags?.map(
              (flag, index) => (

                <div
                  key={index}
                  className="flag"
                >
                  {flag}
                </div>
              )
            )}

          </div>

          {/* AI EXPLANATION */}
          <p style={{ marginTop: "20px" }}>
            {result.ai_explanation}
          </p>

        </div>
      )}

    </div>
  );
}

export default App;