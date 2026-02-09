"""Calculate estimated revenue from token usage and pricing data."""

import logging

logger = logging.getLogger(__name__)


def calculate_revenue(
    rankings: list[dict],
    activities: dict[str, dict],
    pricing: dict[str, dict],
) -> dict:
    """Calculate estimated revenue for each model and total.

    Uses exact token counts from the embedded daily analytics data.
    The analytics data provides prompt_tokens, completion_tokens (includes reasoning),
    reasoning_tokens, and cached_tokens for each model. These are summed over
    the last 7 full days to match the weekly totals on the rankings page.

    Revenue includes:
    - prompt_tokens * prompt_price
    - completion_tokens * completion_price  (completion already includes reasoning)
    - cached_tokens * cache_read_price

    Note: completion_tokens INCLUDES reasoning_tokens (OpenAI convention).
    Reasoning is NOT double-charged; it's a subset of completion.

    Args:
        rankings: List of model dicts from scrape_rankings()
        activities: Dict of slug -> activity dict from scrape_all_model_activities()
        pricing: Dict of slug -> pricing dict from fetch_model_pricing()

    Returns:
        dict with model-level and aggregate revenue data
    """
    models_result = []
    total_revenue = 0.0
    total_tokens = 0
    paid_count = 0
    free_count = 0
    agg_prompt = 0
    agg_completion = 0
    agg_reasoning = 0
    agg_cached = 0

    for model in rankings:
        slug = model["slug"]
        name = model["name"]
        rank = model["rank"]
        ranking_total = model["total_tokens"]
        percent_change = model.get("percent_change", 0)

        # Get exact token counts from embedded analytics
        activity = activities.get(slug, {})
        prompt_tokens = activity.get("prompt_tokens", 0)
        completion_tokens = activity.get("completion_tokens", 0)
        reasoning_tokens = activity.get("reasoning_tokens", 0)
        cached_tokens = activity.get("cached_tokens", 0)
        request_count = activity.get("request_count", 0)

        analytics_total = prompt_tokens + completion_tokens

        # If we have no analytics data, this model contributes $0 revenue.
        # We do NOT fall back to an assumed split — that produces inaccurate data.
        if analytics_total == 0:
            logger.warning(f"No analytics data for {slug}, skipping revenue (tokens stay as ranking total)")

        # Calculate ratios from the actual data
        if analytics_total > 0:
            prompt_ratio = prompt_tokens / analytics_total
            completion_ratio = completion_tokens / analytics_total
            reasoning_ratio = reasoning_tokens / analytics_total
        else:
            prompt_ratio = 0.0
            completion_ratio = 0.0
            reasoning_ratio = 0.0

        # Look up pricing
        price_info = _find_pricing(slug, pricing)

        prompt_price = price_info.get("prompt_price", 0.0) if price_info else 0.0
        completion_price = price_info.get("completion_price", 0.0) if price_info else 0.0
        reasoning_price = price_info.get("reasoning_price", 0.0) if price_info else 0.0
        cache_read_price = 0.0
        if price_info:
            # Cache read price from API: input_cache_read field
            cache_read_price = price_info.get("cache_read_price", 0.0)

        is_free = (prompt_price == 0.0 and completion_price == 0.0)

        # Revenue calculation:
        # - Prompt tokens charged at prompt_price
        # - Completion tokens (already includes reasoning) charged at completion_price
        # - Cached tokens charged at cache_read_price (discounted input)
        # NOTE: We do NOT separately charge reasoning -- it's already in completion_tokens
        revenue = (
            prompt_tokens * prompt_price
            + completion_tokens * completion_price
            + cached_tokens * cache_read_price
        )

        if is_free:
            free_count += 1
        else:
            paid_count += 1

        total_revenue += revenue
        total_tokens += ranking_total
        agg_prompt += prompt_tokens
        agg_completion += completion_tokens
        agg_reasoning += reasoning_tokens
        agg_cached += cached_tokens

        models_result.append({
            "rank": rank,
            "slug": slug,
            "name": name,
            "total_tokens": ranking_total,
            "percent_change": percent_change,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "reasoning_tokens": reasoning_tokens,
            "cached_tokens": cached_tokens,
            "request_count": request_count,
            "prompt_ratio": round(prompt_ratio, 4),
            "completion_ratio": round(completion_ratio, 4),
            "reasoning_ratio": round(reasoning_ratio, 4),
            "prompt_price": prompt_price,
            "completion_price": completion_price,
            "reasoning_price": reasoning_price,
            "cache_read_price": cache_read_price,
            "estimated_revenue": round(revenue, 2),
            "is_free": is_free,
        })

        logger.info(
            f"  #{rank} {name}: {_format_tokens(ranking_total)} tokens, "
            f"prompt={prompt_ratio*100:.1f}%, comp={completion_ratio*100:.1f}%, "
            f"cached={_format_tokens(cached_tokens)}, "
            f"${revenue:,.2f} revenue"
            f"{' (FREE)' if is_free else ''}"
        )

    # Sort by revenue descending
    models_result.sort(key=lambda x: x["estimated_revenue"], reverse=True)

    return {
        "models": models_result,
        "total_revenue": round(total_revenue, 2),
        "total_tokens": total_tokens,
        "total_models": len(models_result),
        "paid_models": paid_count,
        "free_models": free_count,
        "token_breakdown": {
            "prompt_tokens": agg_prompt,
            "completion_tokens": agg_completion,
            "reasoning_tokens": agg_reasoning,
            "cached_tokens": agg_cached,
        },
    }


def _find_pricing(slug: str, pricing: dict) -> dict | None:
    """Find pricing info for a model slug, trying various key formats."""
    # Direct match
    if slug in pricing:
        return pricing[slug]

    # Try without :free suffix
    base_slug = slug.split(":")[0]
    if base_slug in pricing:
        return pricing[base_slug]

    # Try partial match on the slug
    for key, value in pricing.items():
        if key.startswith(slug.split("/")[0] + "/") and _slug_similarity(slug, key) > 0.7:
            return value

    logger.warning(f"No pricing found for slug: {slug}")
    return None


def _slug_similarity(a: str, b: str) -> float:
    """Simple similarity score between two slugs."""
    a_parts = set(a.lower().replace("-", " ").replace(".", " ").split())
    b_parts = set(b.lower().replace("-", " ").replace(".", " ").split())
    if not a_parts or not b_parts:
        return 0.0
    intersection = a_parts & b_parts
    union = a_parts | b_parts
    return len(intersection) / len(union)


def _format_tokens(count: int) -> str:
    """Format token count in human-readable form."""
    if count >= 1_000_000_000_000:
        return f"{count / 1_000_000_000_000:.2f}T"
    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}B"
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)
