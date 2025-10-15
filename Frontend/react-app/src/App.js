import React, { useState } from "react";
import axios from "axios";
import { AnimatePresence, motion } from "framer-motion";

import Header from "./components/Header";
import InputSection from "./components/InputSection";
import FactCard from "./components/FactCard";

function App() {
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Call backend verify endpoint - replace path if needed
  const verifyClaim = async (claimText) => {
    setError(null);
    setLoading(true);
    try {
      // Example POST to /api/verify_claim
      const res = await axios.post("/api/verify_claim", { claim: claimText });
      // Expect backend to return an object: { status, confidence, summary, sources, title? }
      const payload = res.data;
      // Ensure fields exist, fallback values
      const fact = {
        status: payload.status || "Doubtful",
        confidence: payload.confidence ?? 0,
        summary: payload.summary || "No summary returned.",
        sources: payload.sources || [],
        title: payload.title || claimText,
        timestamp: new Date().toISOString(),
      };
      setFacts((prev) => [fact, ...prev]);
    } catch (err) {
      console.error(err);
      setError("Verification failed. Showing placeholder result.");
      // fallback placeholder card so demo always shows something
      setFacts((prev) => [
        {
          status: "Doubtful",
          confidence: 68,
          summary:
            "Temporary placeholder: backend not connected or returned an error.",
          sources: ["Local Demo"],
          title: claimText,
          timestamp: new Date().toISOString(),
        },
        ...prev,
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <Header />
      <main className="container">
        <InputSection onVerify={verifyClaim} loading={loading} />
        {error && <div className="error">{error}</div>}

        <section aria-label="Fact cards" className="cards-wrapper">
          <AnimatePresence>
            {facts.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="empty"
              >
                No verifications yet — paste a claim to get started.
              </motion.div>
            ) : (
              facts.map((fact, i) => (
                <motion.div
                  key={fact.timestamp + i}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                >
                  <FactCard fact={fact} />
                </motion.div>
              ))
            )}
          </AnimatePresence>
        </section>
      </main>

      <footer className="footer">
        <div>TruthGuard 🛡️ — Demo • Built for Mumbai Hacks</div>
        <div className="credits">© {new Date().getFullYear()} { /* optional team name */ }</div>
      </footer>
    </div>
  );
}

export default App;
