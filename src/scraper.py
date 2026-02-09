"""Scrape OpenRouter rankings and model activity pages."""

import re
import time
import logging
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://openrouter.ai"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Navigation prefixes that are NOT model slugs
NAV_PREFIXES = ("docs/", "chat/", "settings/", "compare/", "apps", "models",
                "rankings", "enterprise", "pricing")

# Delay between model page requests (seconds)
REQUEST_DELAY = 1.5


def parse_token_count(text: str) -> int:
    """Parse human-readable token counts like '1.16T', '706B', '445M', '13.4K'.

    Returns the integer token count, or 0 if unparsable.
    """
    text = text.strip().replace(",", "")
    multipliers = {
        "T": 1_000_000_000_000,
        "B": 1_000_000_000,
        "M": 1_000_000,
        "K": 1_000,
    }
    match = re.match(r"^([0-9.]+)\s*([TGBMK])?$", text, re.IGNORECASE)
    if not match:
        return 0
    number = float(match.group(1))
    suffix = (match.group(2) or "").upper()
    multiplier = multipliers.get(suffix, 1)
    return int(number * multiplier)


def scrape_rankings_history(html: str | None = None) -> list[dict]:
    """Extract per-model weekly token data from the rankings page chart.

    The rankings page embeds a stacked bar chart with ~53 weeks of data.
    Each weekly entry contains the top 9 named models and their token counts,
    plus an "Others" category.

    Args:
        html: Pre-fetched HTML string. If None, fetches the rankings page.

    Returns:
        List of weekly entries sorted by date ascending:
        [
            {
                "week_start": "2025-12-01",   # Monday start of the week
                "models": {
                    "x-ai/grok-code-fast-1": 878900000000,
                    "anthropic/claude-4.5-sonnet-20250929": 429300000000,
                    ...
                },
                "others": 3025200000000,
                "total": 6190000000000,
            },
            ...
        ]
    """
    if html is None:
        url = f"{BASE_URL}/rankings"
        logger.info(f"Fetching rankings page for historical chart data from {url}")
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        html = resp.text

    # The rankings page contains multiple chart datasets in separate <script> tags.
    # We need the MAIN model-level weekly chart (the one with the most entries
    # that contain model slugs with "/" in them).
    # Strategy: parse each script tag independently, find the one with the most
    # model-level entries, and use only that one.

    script_tags = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)

    best_entries: list[dict] = []

    for script in script_tags:
        if len(script) < 1000:
            continue

        unescaped = script.replace('\\"', '"').replace('\\\\', '\\')

        entries = []
        for m in re.finditer(r'"x":"(\d{4}-\d{2}-\d{2})(?:[^"]*)?","ys":\{', unescaped):
            date_str = m.group(1)
            brace_start = m.end() - 1

            depth = 0
            brace_end = brace_start
            for j in range(brace_start, min(brace_start + 10000, len(unescaped))):
                if unescaped[j] == '{':
                    depth += 1
                elif unescaped[j] == '}':
                    depth -= 1
                    if depth == 0:
                        brace_end = j
                        break

            ys_str = unescaped[brace_start:brace_end + 1]
            pairs = re.findall(r'"([^"]+)":(\d+(?:\.\d+)?)', ys_str)

            if not pairs:
                continue

            # Only consider entries where keys contain "/" (model slugs)
            has_model_slugs = any("/" in p[0] for p in pairs)
            if not has_model_slugs:
                continue

            models = {}
            others = 0
            total = 0
            for slug, tokens_str in pairs:
                tokens = int(float(tokens_str))
                total += tokens
                if slug == "Others":
                    others = tokens
                else:
                    models[slug] = tokens

            entries.append({
                "week_start": date_str,
                "models": models,
                "others": others,
                "total": total,
            })

        # The main model rankings chart is the script with the most entries
        if len(entries) > len(best_entries):
            best_entries = entries

    final = sorted(best_entries, key=lambda x: x["week_start"])
    logger.info(f"Extracted {len(final)} weeks of historical chart data")
    if final:
        logger.info(f"  Range: {final[0]['week_start']} to {final[-1]['week_start']}")

    return final


def scrape_rankings() -> list[dict]:
    """Scrape the OpenRouter rankings page for the top models.

    Returns a list of dicts:
        [
            {
                "rank": 1,
                "slug": "moonshotai/kimi-k2.5-0127",
                "name": "Kimi K2.5 0127",
                "total_tokens": 1160000000000,
                "percent_change": 222,
            },
            ...
        ]
    """
    url = f"{BASE_URL}/rankings"
    logger.info(f"Fetching rankings from {url}")
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    rank = 0

    # Each ranked model is inside a grid row: <div class="grid grid-cols-12 ...">
    grid_rows = soup.find_all("div", class_=re.compile(r"grid grid-cols-12"))

    for row in grid_rows:
        # Model link: <a class="...text-foreground..." href="/author/model-slug">Name</a>
        model_link = row.find("a", class_=re.compile(r"text-foreground"))
        if not model_link:
            continue

        href = model_link.get("href", "")
        slug = href.lstrip("/")

        # Skip navigation links
        if not slug or slug.startswith(NAV_PREFIXES) or "/" not in slug:
            continue

        name = model_link.get_text(strip=True)
        rank += 1

        # Token count: inside <div class="col-span-4 ...">
        token_col = row.find("div", class_=re.compile(r"col-span-4"))
        total_tokens = 0
        percent_change = 0

        if token_col:
            col_text = token_col.get_text(strip=True)

            # Parse token count: extract "1.16T" from "1.16Ttokens222%"
            token_match = re.match(r"([0-9.]+)([TGBMK])tokens", col_text, re.IGNORECASE)
            if token_match:
                token_str = token_match.group(1) + token_match.group(2)
                total_tokens = parse_token_count(token_str)

            # Parse percentage: extract "222" from the end
            pct_match = re.search(r"(\d+)%", col_text)
            if pct_match:
                percent_change = int(pct_match.group(1))

            # Determine direction from SVG color class
            svg = token_col.find("svg")
            if svg:
                svg_classes = " ".join(svg.get("class", []))
                if "text-red" in svg_classes:
                    percent_change = -percent_change

        results.append({
            "rank": rank,
            "slug": slug,
            "name": name,
            "total_tokens": total_tokens,
            "percent_change": percent_change,
        })

    logger.info(f"Parsed {len(results)} models from rankings")
    return results


# --- Daily analytics extraction (used by both normal and backfill modes) ---

def _extract_daily_data(html: str) -> dict[str, dict]:
    """Extract all daily analytics entries from a model page's HTML.

    Parses the embedded Next.js script data for daily token counts.

    Returns:
        Dict mapping date string (YYYY-MM-DD) to:
        {
            "prompt": int,
            "completion": int,
            "reasoning": int,
            "cached": int,
            "count": int,
        }
        Returns empty dict if no data found.
    """
    Q = r'(?:\\"|")'  # matches either \" or "

    daily_pattern = re.compile(
        Q + r'date' + Q + r':' + Q + r'(\d{4}-\d{2}-\d{2})[^"\\]*' + Q + r','
        + Q + r'model_permaslug' + Q + r':' + Q + r'[^"\\]*' + Q + r','
        + Q + r'variant' + Q + r':' + Q + r'([^"\\]*)' + Q + r','
        + Q + r'total_completion_tokens' + Q + r':(\d+),'
        + Q + r'total_prompt_tokens' + Q + r':(\d+),'
        + Q + r'total_native_tokens_reasoning' + Q + r':(\d+),'
        + Q + r'count' + Q + r':(\d+)'
    )
    daily_entries = daily_pattern.findall(html)

    if not daily_entries:
        return {}

    # Extract cached tokens
    cached_pattern = re.compile(
        Q + r'date' + Q + r':' + Q + r'(\d{4}-\d{2}-\d{2})[^"\\]*' + Q + r','
        + Q + r'model_permaslug' + Q + r'.*?'
        + Q + r'total_native_tokens_cached' + Q + r':(\d+)'
    )
    cached_entries = cached_pattern.findall(html)
    cached_by_date: dict[str, int] = {}
    for date_str, cached in cached_entries:
        cached_by_date[date_str] = cached_by_date.get(date_str, 0) + int(cached)

    # Group by date, summing across all variants
    daily_totals: dict[str, dict] = {}
    for date_str, variant, comp, prompt, reasoning, count in daily_entries:
        if date_str not in daily_totals:
            daily_totals[date_str] = {
                "prompt": 0, "completion": 0, "reasoning": 0, "cached": 0, "count": 0
            }
        daily_totals[date_str]["prompt"] += int(prompt)
        daily_totals[date_str]["completion"] += int(comp)
        daily_totals[date_str]["reasoning"] += int(reasoning)
        daily_totals[date_str]["count"] += int(count)

    # Merge cached tokens
    for date_str, cached_val in cached_by_date.items():
        if date_str in daily_totals:
            daily_totals[date_str]["cached"] = cached_val

    return daily_totals


def sum_daily_window(
    daily_data: dict[str, dict],
    end_date: str,
    days: int = 7,
    skip_partial: bool = True,
) -> dict:
    """Sum daily analytics over a specific window.

    Args:
        daily_data: Dict of date -> daily totals from _extract_daily_data()
        end_date: The last date of the window (YYYY-MM-DD)
        days: Number of days to sum (default 7 for weekly)
        skip_partial: If True and end_date is today, skip it (partial day)

    Returns:
        Activity dict with prompt_tokens, completion_tokens, reasoning_tokens,
        cached_tokens, request_count.
    """
    result = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "reasoning_tokens": 0,
        "cached_tokens": 0,
        "request_count": 0,
    }

    end = datetime.strptime(end_date, "%Y-%m-%d")
    today = datetime.utcnow().strftime("%Y-%m-%d")

    dates_to_sum = []
    for i in range(days):
        d = (end - timedelta(days=i)).strftime("%Y-%m-%d")
        # Skip today if partial
        if skip_partial and d == today:
            continue
        dates_to_sum.append(d)

    # If we skipped today, add one more day at the start to keep 7 days
    if skip_partial and end_date == today and len(dates_to_sum) < days:
        extra = (end - timedelta(days=days)).strftime("%Y-%m-%d")
        dates_to_sum.append(extra)

    for d in dates_to_sum:
        if d in daily_data:
            day = daily_data[d]
            result["prompt_tokens"] += day["prompt"]
            result["completion_tokens"] += day["completion"]
            result["reasoning_tokens"] += day["reasoning"]
            result["cached_tokens"] += day.get("cached", 0)
            result["request_count"] += day["count"]

    return result


# --- Public scraping functions ---

def scrape_model_daily_data(slug: str) -> dict[str, dict]:
    """Fetch a model page and return all daily analytics data.

    This is used by backfill mode to get the full history (typically ~90 days)
    in a single request per model.

    Args:
        slug: The model's canonical slug

    Returns:
        Dict mapping date string (YYYY-MM-DD) -> daily totals dict.
        Empty dict if data cannot be found.
    """
    url = f"{BASE_URL}/{slug}"
    logger.info(f"Fetching model daily data from {url}")

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return {}

    daily_data = _extract_daily_data(resp.text)
    if daily_data:
        sorted_dates = sorted(daily_data.keys())
        logger.info(
            f"  {slug}: {len(daily_data)} days of data "
            f"({sorted_dates[0]} to {sorted_dates[-1]})"
        )
    else:
        logger.warning(f"  {slug}: no embedded analytics found")

    return daily_data


def scrape_model_activity(slug: str) -> dict:
    """Scrape a model's page for the current week's token breakdown.

    Convenience wrapper: fetches daily data and sums the most recent 7 full days.
    """
    url = f"{BASE_URL}/{slug}"
    logger.info(f"Fetching model activity from {url}")

    default_result = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "reasoning_tokens": 0,
        "cached_tokens": 0,
        "request_count": 0,
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return default_result

    daily_data = _extract_daily_data(resp.text)
    if not daily_data:
        logger.warning(f"No embedded analytics found for {slug}, falling back to HTML parsing")
        return _scrape_model_activity_html(resp.text)

    # Sum the most recent 7 full days (skip partial today)
    sorted_dates = sorted(daily_data.keys(), reverse=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    end = sorted_dates[0]
    result = sum_daily_window(daily_data, end, days=7, skip_partial=True)

    logger.info(
        f"  {slug}: prompt={result['prompt_tokens']/1e9:.1f}B, "
        f"comp={result['completion_tokens']/1e9:.2f}B, "
        f"reasoning={result['reasoning_tokens']/1e6:.1f}M, "
        f"cached={result['cached_tokens']/1e9:.1f}B, "
        f"requests={result['request_count']:,}"
    )

    return result


def _scrape_model_activity_html(html: str) -> dict:
    """Fallback: scrape token breakdown from the HTML activity legend."""
    result = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "reasoning_tokens": 0,
        "cached_tokens": 0,
        "request_count": 0,
    }

    token_type_map = {
        "Prompt": "prompt_tokens",
        "Completion": "completion_tokens",
        "Reasoning": "reasoning_tokens",
    }

    for label, key in token_type_map.items():
        pattern = re.compile(
            rf'aria-label="{label}".*?'
            rf'<div class="font-medium[^"]*"[^>]*>{label}</div>'
            rf'.*?<div>([0-9.]+[TGBMK]?)</div>',
            re.DOTALL,
        )
        match = pattern.search(html)
        if match:
            result[key] = parse_token_count(match.group(1))

    return result


def scrape_all_model_activities(rankings: list[dict], delay: float = REQUEST_DELAY) -> dict:
    """Scrape activity data for all ranked models (current week only).

    Args:
        rankings: List of ranked model dicts from scrape_rankings()
        delay: Seconds to wait between requests

    Returns:
        Dict mapping slug -> activity dict
    """
    activities = {}
    for i, model in enumerate(rankings):
        slug = model["slug"]
        logger.info(f"[{i+1}/{len(rankings)}] Scraping activity for {slug}")
        activities[slug] = scrape_model_activity(slug)

        # Be polite: delay between requests (skip after last)
        if i < len(rankings) - 1:
            time.sleep(delay)

    return activities


def scrape_all_model_daily_data(
    rankings: list[dict],
    delay: float = REQUEST_DELAY,
) -> dict[str, dict[str, dict]]:
    """Scrape full daily history for all ranked models.

    Makes one request per model and returns the complete daily data set,
    which can then be sliced into arbitrary weekly windows for backfill.

    Args:
        rankings: List of ranked model dicts from scrape_rankings()
        delay: Seconds to wait between requests

    Returns:
        Dict mapping slug -> {date -> daily_totals}
    """
    all_daily = {}
    for i, model in enumerate(rankings):
        slug = model["slug"]
        logger.info(f"[{i+1}/{len(rankings)}] Scraping daily data for {slug}")
        all_daily[slug] = scrape_model_daily_data(slug)

        if i < len(rankings) - 1:
            time.sleep(delay)

    return all_daily
