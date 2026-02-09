"""Fetch model pricing data from the OpenRouter public API."""

import requests

MODELS_API_URL = "https://openrouter.ai/api/v1/models"

# Headers to mimic a normal browser request
HEADERS = {
    "User-Agent": "OpenRouter-Inference-Stats/1.0 (https://github.com)",
    "Accept": "application/json",
}


def fetch_model_pricing() -> dict:
    """Fetch all models and return a dict mapping canonical_slug -> pricing info.

    Returns:
        dict: {
            "anthropic/claude-4.5-sonnet-20250929": {
                "id": "anthropic/claude-sonnet-4.5",
                "name": "Anthropic: Claude Sonnet 4.5",
                "prompt_price": 0.000003,
                "completion_price": 0.000015,
                "reasoning_price": 0.000015,  # falls back to completion if not set
                "image_price": 0.0,
                "web_search_price": 0.0,
            },
            ...
        }
    """
    resp = requests.get(MODELS_API_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    pricing_map = {}
    for model in data.get("data", []):
        model_id = model.get("id", "")
        canonical_slug = model.get("canonical_slug", "")
        name = model.get("name", "")
        pricing = model.get("pricing", {})

        prompt_price = _parse_price(pricing.get("prompt", "0"))
        completion_price = _parse_price(pricing.get("completion", "0"))
        reasoning_price = _parse_price(pricing.get("internal_reasoning", ""))
        image_price = _parse_price(pricing.get("image", "0"))
        web_search_price = _parse_price(pricing.get("web_search", "0"))
        cache_read_price = _parse_price(pricing.get("input_cache_read", "0"))
        cache_write_price = _parse_price(pricing.get("input_cache_write", "0"))

        # Fall back to completion price for reasoning if not explicitly set
        if reasoning_price == 0.0:
            reasoning_price = completion_price

        entry = {
            "id": model_id,
            "name": name,
            "prompt_price": prompt_price,
            "completion_price": completion_price,
            "reasoning_price": reasoning_price,
            "image_price": image_price,
            "web_search_price": web_search_price,
            "cache_read_price": cache_read_price,
            "cache_write_price": cache_write_price,
        }

        # Index by both canonical_slug and model_id for flexible lookups
        if canonical_slug:
            pricing_map[canonical_slug] = entry
        if model_id:
            pricing_map[model_id] = entry

    return pricing_map


def _parse_price(value: str) -> float:
    """Parse a price string to float, returning 0.0 for empty/invalid values."""
    if not value:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
