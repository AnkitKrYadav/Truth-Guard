import React, { useState } from "react";
import axios from "axios";

function Verify() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!claim.trim()) return;

    setLoading(true);
    setResult(null);
    try {
      const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";
      console.log("Using API base:", API_BASE_URL);
      const res = await axios.post(`${API_BASE_URL}/api/verify`, { claim });
      // const res = await axios.post("https://truth-guard-89p9.onrender.com/api/verify", { claim });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Error verifying claim." });
    } finally {
      setLoading(false);
    }
  };

  const getBadgeColor = (status) => {
    if (status === "True") return "bg-green-200 text-green-800";
    if (status === "False") return "bg-red-200 text-red-800";
    return "bg-yellow-200 text-yellow-800";
  };

  // 🔥 NEW: Get color for confidence bar
  const getConfidenceColor = (confidence) => {
    if (confidence >= 70) return "bg-green-500";
    if (confidence >= 40) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="p-6 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen">
      <h2 className="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
        Verify News
      </h2>

      {/* Input Section */}
      <form
        onSubmit={handleSubmit}
        className="flex flex-col sm:flex-row gap-3 mb-6"
      >
        <input
          type="text"
          value={claim}
          onChange={(e) => setClaim(e.target.value)}
          placeholder="Enter news or claim to verify..."
          className="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition"
        >
          {loading ? "Verifying..." : "Verify"}
        </button>
      </form>

      {/* Result Card */}
      {result && (
        <div className="p-5 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 max-w-2xl">
          {result.error ? (
            <p className="text-red-500">{result.error}</p>
          ) : (
            <>
              <p className="mb-2 font-medium text-lg">
                Claim: <span className="font-semibold">{result.claim}</span>
              </p>

              <span
                className={`inline-block px-3 py-1 text-sm font-semibold rounded-full ${getBadgeColor(
                  result.status
                )}`}
              >
                {result.status}
              </span>

              <p className="mt-3 text-gray-700 dark:text-gray-300">
                {result.summary}
              </p>

              {/* 🔥 NEW: Confidence Score Section */}
              {result.confidence !== undefined && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Confidence Score:{" "}
                    <span className="font-semibold">{result.confidence}%</span>
                  </p>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${getConfidenceColor(
                        result.confidence
                      )}`}
                      style={{ width: `${result.confidence}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Sources */}
              {result.sources && result.sources.length > 0 && (
                <p className="mt-4 text-sm text-gray-600 dark:text-gray-300">
                  <span className="font-medium">Sources:</span>{" "}
                  {result.sources.join(", ")}
                </p>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default Verify;
