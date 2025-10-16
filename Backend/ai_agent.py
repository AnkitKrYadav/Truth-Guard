"""
ai_agent.py

Clean, minimal AI agent helpers for Truth-Guard.

Functions:
- fetch_news_sources(claim, limit=3): returns list of news source names (uses NewsAPI)
- fetch_factcheck_claims(claim, limit=3): returns short fact-check texts (uses FactCheck Tools API)
- verify_claim_with_ai(claim): calls OpenAI to produce a JSON result: {status, summary, sources}

This module is small and dependency-light. Functions degrade gracefully if keys
are missing or requests fail.
"""

import os
import json
import logging
from typing import List, Dict, Any
import requests

try:
    import openai
except ImportError:
    openai = None

# Setup logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FACTCHECK_API_KEY = os.getenv("FACTCHECK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


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


def _compute_confidence(ai_status: str, news_sources: List[str], fact_checks: List[str]) -> int:
    """
    Compute a confidence score (0-100) for the claim.
    """
    score = 50  # default mid for Unclear

    # Adjust based on AI result
    if ai_status == "True":
        score += 30
    elif ai_status == "False":
        score -= 30

    # Adjust based on number of supporting news sources
    score += min(len(news_sources), 3) * 5  # max +15

    # Adjust based on fact-check evidence
    if fact_checks:
        # If fact-checks confirm claim, boost by 20
        for fc in fact_checks:
            fc_lower = fc.lower()
            if "true" in fc_lower or "verified" in fc_lower:
                score += 20
            elif "false" in fc_lower or "misleading" in fc_lower:
                score -= 20

    # Clamp between 0 and 100
    score = max(0, min(100, score))
    return score



if __name__ == "__main__":
    # Simple local test
    test_claim = "ChatGPT can pass advanced exams"
    print(verify_claim_with_ai(test_claim))
