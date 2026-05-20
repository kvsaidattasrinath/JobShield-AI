import { useState } from "react";
import axios from "axios";

function App() {

  const [jobText, setJobText] = useState("");

  const [jobUrl, setJobUrl] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  // -----------------------------
  // ANALYZE JOB
  // -----------------------------
  const analyzeJob = async () => {

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        {
          text: jobText,
          url: jobUrl
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert("Backend connection failed");

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen bg-black text-white flex justify-center items-center p-6">

      <div className="w-full max-w-3xl bg-gray-900 p-8 rounded-2xl border border-gray-800 shadow-2xl">

        {/* HEADER */}
        <div className="mb-8">

          <h1 className="text-4xl font-bold text-red-500">
            JobShield AI
          </h1>

          <p className="text-gray-400 mt-2">
            AI-powered fake job and scam detection system
          </p>

        </div>

        {/* URL INPUT */}
        <input
          type="text"
          placeholder="Paste Job URL here..."
          value={jobUrl}
          onChange={(e) => setJobUrl(e.target.value)}
          className="w-full mb-4 bg-gray-800 border border-gray-700 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
        />

        {/* TEXTAREA */}
        <textarea
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
          placeholder="Or paste job description here..."
          className="w-full h-48 bg-gray-800 border border-gray-700 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
        />

        {/* BUTTON */}
        <button
          onClick={analyzeJob}
          disabled={loading}
          className="w-full mt-6 bg-red-500 hover:bg-red-600 transition-all py-3 rounded-xl font-semibold"
        >

          {loading ? "Analyzing..." : "Analyze Job"}

        </button>

        {/* RESULTS */}
        {result && (

          <div className="mt-8 space-y-6">

            {/* PREDICTION */}
            <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">

              <h2 className="text-2xl font-bold">

                Prediction:

                <span
                  className={`ml-3 ${
                    result.prediction === "Fake Job"
                      ? "text-red-500"
                      : "text-green-400"
                  }`}
                >
                  {result.prediction}
                </span>

              </h2>

            </div>

            {/* CONFIDENCE */}
            <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">

              <h2 className="text-xl font-semibold text-blue-400 mb-3">
                Confidence Scores
              </h2>

              <p>
                ML Confidence:
                <span className="ml-2 font-bold">
                  {result.ml_confidence}%
                </span>
              </p>

              <p className="mt-2">
                Rule Score:
                <span className="ml-2 font-bold">
                  {result.rule_score}
                </span>
              </p>

              <p className="mt-2">
                Final Confidence:
                <span className="ml-2 font-bold">
                  {result.final_confidence}%
                </span>
              </p>

            </div>

            {/* FLAGS */}
            <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">

              <h2 className="text-xl font-semibold text-yellow-400 mb-3">
                Detected Scam Flags
              </h2>

              <div className="flex flex-wrap gap-2">

                {result.detected_flags.length > 0 ? (

                  result.detected_flags.map((flag, index) => (

                    <span
                      key={index}
                      className="bg-red-500/20 text-red-400 border border-red-500 px-3 py-1 rounded-full"
                    >
                      {flag}
                    </span>

                  ))

                ) : (

                  <span className="text-green-400">
                    No scam flags detected
                  </span>

                )}

              </div>

            </div>

            {/* AI EXPLANATION */}
            <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">

              <h2 className="text-xl font-semibold text-purple-400 mb-3">
                AI Explanation
              </h2>

              <p className="text-gray-300 whitespace-pre-line leading-relaxed">

                {result.ai_explanation}

              </p>

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default App;