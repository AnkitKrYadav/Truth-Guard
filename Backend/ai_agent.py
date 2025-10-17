"""
ai_agent.py
Clean AI helpers for Truth-Guard with full debug logging.
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

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FACTCHECK_API_KEY = os.getenv("FACTCHECK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
AI_MOCK = os.getenv("AI_MOCK", "False").lower() in ("1", "true", "yes")

if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def fetch_news_sources(claim: str, limit: int = 3) -> List[str]:
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
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
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
    score = 50
    if ai_status == "True":
        score += 30
    elif ai_status == "False":
        score -= 30

    score += min(len(news_sources), 3) * 5
    for fc in fact_checks:
        fc_lower = (fc or "").lower()
        if "true" in fc_lower or "verified" in fc_lower:
            score += 20
        elif "false" in fc_lower or "misleading" in fc_lower:
            score -= 20
    return max(0, min(100, score))


def verify_claim_with_ai(claim: str) -> Dict[str, Any]:
    _logger.info("Verifying claim: %s", claim)
    news = fetch_news_sources(claim, limit=3)
    facts = fetch_factcheck_claims(claim, limit=3)
    collected = list(dict.fromkeys([s for s in (news + facts) if s]))

    if AI_MOCK:
        _logger.info("AI_MOCK enabled — returning mock result")
        return {
            "claim": claim,
            "status": "Unclear",
            "summary": "Mock mode: no live AI call.",
            "sources": collected,
            "confidence": _compute_confidence("Unclear", news, facts),
        }

    if not openai or not OPENAI_API_KEY:
        _logger.warning("OpenAI not configured; returning collected evidence only")
        return {
            "claim": claim,
            "status": "Unclear",
            "summary": "AI not configured. Returning collected sources.",
            "sources": collected,
            "confidence": _compute_confidence("Unclear", news, facts),
        }

    prompt = (
        "You are TruthGuard, an assistant that verifies short claims.\n"
        "Provide output as strict JSON with keys: status (True|False|Unclear), summary (1-2 sentences), sources (array).\n"
        f"CLAIM: {claim}\n"
    )

    text = ""
    try:
        # Modern OpenAI API
        if hasattr(openai, "chat") and hasattr(openai.chat, "completions"):
            resp = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.2,
            )
            choices = getattr(resp, "choices", [])
            first = choices[0] if choices else {}
            message = getattr(first, "message", {})
            text = getattr(message, "content", "") or ""
        else:
            # Legacy fallback
            resp = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.2,
            )
            choices = getattr(resp, "choices", [])
            if choices:
                first = choices[0]
                message = getattr(first, "message", {})
                text = getattr(message, "content", "") or ""
    except Exception as e:
        _logger.exception("OpenAI request failed: %s", e)
        return {
            "claim": claim,
            "status": "Unclear",
            "summary": f"AI request failed: {str(e)}",
            "sources": collected,
            "confidence": _compute_confidence("Unclear", news, facts),
        }

    parsed = _safe_json_parse(text)
    if isinstance(parsed, dict):
        status = parsed.get("status", "Unclear")
        summary = parsed.get("summary", text.strip())
        sources_out = parsed.get("sources", []) or []
        merged = list(dict.fromkeys(collected + list(sources_out)))
        confidence = _compute_confidence(status, news, facts)
        return {"claim": claim, "status": status, "summary": summary, "sources": merged, "confidence": confidence}

    return {
        "claim": claim,
        "status": "Unclear",
        "summary": text.strip(),
        "sources": collected,
        "confidence": _compute_confidence("Unclear", news, facts),
    }
