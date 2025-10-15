import React from "react";
import Header from "./components/Header";
import InputSection from "./components/InputSection";
import FactCard from "./components/FactCard";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 text-gray-900">
      <Header />
      <main className="max-w-4xl mx-auto p-6">
        <InputSection />
        <section className="mt-10 space-y-6">
          <FactCard
            title="Breaking News: AI Detects Fake Article"
            source="BBC News"
            confidence="92%"
            verdict="Likely True"
            description="An AI model has flagged misinformation in trending news articles and verified facts using cross-source analysis."
          />
          <FactCard
            title="Viral Tweet Misleading About Climate Data"
            source="Twitter / X"
            confidence="64%"
            verdict="Partially False"
            description="Data was selectively used, omitting key scientific studies that contradict the claim."
          />
        </section>
      </main>
      <footer className="mt-10 py-6 text-center text-gray-500 border-t">
        © 2025 TruthGuard — Built with 💡 by Uday
      </footer>
    </div>
  );
}

export default App;
