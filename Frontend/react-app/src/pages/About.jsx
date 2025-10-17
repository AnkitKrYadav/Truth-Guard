import React from "react";

function About() {
  return (
    <div className="p-6 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen">
      <h2 className="text-2xl font-semibold mb-4">About TruthGuard</h2>
      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
        TruthGuard is an AI-powered fact-verification platform designed to combat misinformation.  
        It integrates language models, trusted APIs, and community feedback to verify digital claims in real time.
      </p>
    </div>
  );
}

export default About;
