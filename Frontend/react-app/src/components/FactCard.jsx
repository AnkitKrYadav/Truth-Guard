import React from "react";
import { AiOutlineLink } from "react-icons/ai";

const statusColor = (status) => {
  if (!status) return "#999";
  const s = status.toLowerCase();
  if (s.includes("true") || s.includes("true")) return "#137f24"; // green
  if (s.includes("doubt") || s.includes("partially") || s.includes("mixed")) return "#b08900"; // yellow
  return "#be2b2b"; // red
};

const FactCard = ({ fact }) => {
  const color = statusColor(fact.status);

  return (
    <article className="fact-card" role="article" aria-live="polite">
      <div className="fact-head" style={{ borderLeft: `6px solid ${color}` }}>
        <div className="fact-title">{fact.title}</div>
        <div className="fact-meta">
          <span className="status" style={{ color }}>{fact.status} • {fact.confidence}%</span>
          <time className="time">{new Date(fact.timestamp).toLocaleString()}</time>
        </div>
      </div>

      <div className="fact-body">
        <p className="summary">{fact.summary}</p>
        {fact.sources && fact.sources.length > 0 && (
          <div className="sources">
            <strong>Sources:</strong>
            <ul>
              {fact.sources.map((s, i) => (
                <li key={i}><AiOutlineLink /> {s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="fact-actions">
        <button className="btn small">Agree</button>
        <button className="btn small ghost">Report</button>
      </div>
    </article>
  );
};

export default FactCard;
