import React, { useState } from "react";
import { FiCheckCircle } from "react-icons/fi";

const InputSection = ({ onVerify, loading }) => {
  const [text, setText] = useState("");

  const handleVerify = () => {
    const claim = text.trim();
    if (!claim) return;
    onVerify(claim);
    setText("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      handleVerify();
    }
  };

  return (
    <section className="input-section" id="demo" aria-label="Verify a claim">
      <div className="input-inner container">
        <label htmlFor="claim" className="label">
          Paste a claim or news excerpt to verify
        </label>
        <textarea
          id="claim"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKey}
          rows="4"
          placeholder="Example: 'XYZ vaccine causes infertility' — paste text or a short paragraph here"
          className="textarea"
          aria-label="Claim input"
        />
        <div className="actions">
          <button
            className="btn primary"
            onClick={handleVerify}
            disabled={loading}
            aria-pressed="false"
          >
            {loading ? "Verifying…" : (<><FiCheckCircle /> Verify</>)}
          </button>
          <button
            className="btn ghost"
            onClick={() => setText("")}
            aria-label="Clear input"
          >
            Clear
          </button>
        </div>
        <small className="hint">
          Tip: Press <kbd>Ctrl/⌘ + Enter</kbd> to verify quickly.
        </small>
      </div>
    </section>
  );
};

export default InputSection;
