"""
ai_agent.py

Clean AI agent helpers for Truth-Guard.

Functions:
- fetch_news_sources(claim, limit=3): returns list of news source names (uses NewsAPI)
- fetch_factcheck_claims(claim, limit=3): returns short fact-check texts (uses FactCheck Tools API)
- verify_claim_with_ai(claim): calls Gemini to produce a JSON result: {status, summary, sources, confidence}
"""

import os
import json
import logging
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - dependency optional at runtime
    genai = None

# Setup logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FACTCHECK_API_KEY = os.getenv("FACTCHECK_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if genai and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def fetch_news_sources(claim: str, limit: int = 3) -> List[str]:
    """Fetch top news source names related to the claim using NewsAPI."""
    if not NEWS_API_KEY:
        _logger.debug("No NEWS_API_KEY configured; skipping news fetch")
        return []

    try:
        url = "https://newsapi.org/v2/everything"
        params = {"q": claim, "apiKey": NEWS_API_KEY, "pageSize": limit}
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [a.get("source", {}).get("name") for a in articles if a.get("source")][:limit]
    except Exception as e:
        _logger.warning("fetch_news_sources error: %s", e)
        return []


def fetch_factcheck_claims(claim: str, limit: int = 3) -> List[str]:
    """Fetch short fact-check claim texts using Google Fact Check Tools API."""
    if not FACTCHECK_API_KEY:
        _logger.debug("No FACTCHECK_API_KEY configured; skipping factcheck fetch")
        return []

    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {"query": claim, "key": FACTCHECK_API_KEY, "pageSize": limit}
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        items = resp.json().get("claims", [])
        return [item.get("text", "") for item in items[:limit]]
    except Exception as e:
        _logger.warning("fetch_factcheck_claims error: %s", e)
        return []


def _safe_json_parse(text: str) -> Any:
    """Attempt to parse JSON from text, even if embedded in extra text."""
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = text[start:end + 1]
        try:
            return json.loads(snippet)
        except Exception:
            pass
    return None


def _compute_confidence(ai_status: str, news_sources: list, fact_checks: list) -> int:
    """Compute confidence score from 0 to 100."""
    score = 50  # default neutral

    # AI signal
    if ai_status == "True":
        score += 30
    elif ai_status == "False":
        score -= 30

    # News sources signal
    score += min(len(news_sources), 3) * 5  # up to +15

    # Fact-check signal
    for fc in fact_checks:
        fc_lower = fc.lower()
        if "true" in fc_lower or "verified" in fc_lower:
            score += 10
        elif "false" in fc_lower or "misleading" in fc_lower:
            score -= 10

    return max(0, min(100, score))


def verify_claim_with_ai(claim: str) -> Dict[str, Any]:
    """Call Gemini to analyze a claim and return verification details."""
    if not genai or not GEMINI_API_KEY:
        return {
            "status": "Needs Verification",
            "summary": "No Gemini API key configured.",
            "sources": [],
            "confidence": 50,
            "claim": claim,
        }

    prompt = f"""
    You are a fact-checking assistant. Analyze the following claim and determine if it is True, False, or Needs Verification.
    Provide a short summary and list 1-3 credible sources if available. Respond only in JSON format:

    {{
        "status": "True / False / Needs Verification",
        "summary": "...",
        "sources": ["source1", "source2"]
    }}

    Claim: {claim}
    """

    ai_result: Dict[str, Any] | None
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        response_text = getattr(response, "text", None) or ""
        if not response_text and getattr(response, "candidates", None):
            parts = []
            for candidate in response.candidates:
                contents = getattr(candidate, "content", None)
                if not contents:
                    continue
                for part in getattr(contents, "parts", []) or []:
                    part_text = getattr(part, "text", None)
                    if part_text:
                        parts.append(part_text)
            response_text = "\n".join(parts)

        ai_result = _safe_json_parse(response_text) if response_text else None
    except Exception as e:
        _logger.warning("AI verification failed: %s", e)
        ai_result = None

    if not isinstance(ai_result, dict):
        ai_result = {
            "status": "Needs Verification",
            "summary": "AI could not parse the response.",
            "sources": [],
        }

    ai_status = ai_result.get("status", "Needs Verification")
    news_sources = fetch_news_sources(claim)
    fact_checks = fetch_factcheck_claims(claim)
    confidence = _compute_confidence(ai_status, news_sources, fact_checks)

    combined_sources = [s for s in ai_result.get("sources", []) if s]
    combined_sources.extend(source for source in news_sources if source)
    combined_sources.extend(fc for fc in fact_checks if fc)
    ai_result["sources"] = list(dict.fromkeys(combined_sources))
    ai_result["confidence"] = confidence
    ai_result["claim"] = claim
    return ai_result


if __name__ == "__main__":
    # Quick local test
    test_claim = "ChatGPT can pass advanced exams"
    result = verify_claim_with_ai(test_claim)
    print(json.dumps(result, indent=2))
