import React, { useState } from "react";
import { Search } from "lucide-react";

function InputSection() {
  const [query, setQuery] = useState("");

  const handleVerify = () => {
    if (!query.trim()) return;
    alert(`Verifying: ${query}`);
    // TODO: connect backend (fetch('/api/verify_news', { method: 'POST', ... }))
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md flex items-center gap-3">
      <Search className="w-6 h-6 text-gray-500" />
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Paste a news headline, link, or claim..."
        className="flex-grow focus:outline-none bg-transparent text-gray-800 placeholder-gray-500"
      />
      <button
        onClick={handleVerify}
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg transition"
      >
        Verify
      </button>
    </div>
  );
}

export default InputSection;
