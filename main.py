#!/usr/bin/env python3
"""OpenRouter Inference Revenue Statistics -- main pipeline.

Collects usage data from OpenRouter, calculates estimated revenue,
saves a timestamped snapshot, and regenerates the README.

Usage:
    python main.py                     # Normal run: current week only
    python main.py --backfill          # Backfill past 10 weeks from daily data
    python main.py --backfill --weeks 5  # Backfill past 5 weeks
"""

import argparse
import json
import os
import sys
import time
import logging
from datetime import datetime, timedelta, timezone

import requests

from src.api import fetch_model_pricing
from src.scraper import (
    scrape_rankings,
    scrape_rankings_history,
    scrape_all_model_activities,
    scrape_model_daily_data,
    sum_daily_window,
    HEADERS as SCRAPER_HEADERS,
    REQUEST_DELAY,
)
from src.calculator import calculate_revenue
from src.readme_gen import generate_readme, load_history

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
README_PATH = os.path.join(os.path.dirname(__file__), "README.md")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("main")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect OpenRouter inference revenue statistics."
    )
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Calculate historical weekly snapshots from embedded daily analytics data.",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=0,
        help="Number of past weeks to backfill (default: 0 = all available). Only used with --backfill.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if args.backfill:
        return run_backfill(args.weeks, today)
    else:
        return run_current(today)


def _find_recent_snapshot(today: str, days_back: int = 6) -> str | None:
    """Check if a snapshot already exists within the last N days.

    Returns the date string of the existing snapshot, or None.
    """
    today_dt = datetime.strptime(today, "%Y-%m-%d")
    for offset in range(0, days_back + 1):
        check_date = (today_dt - timedelta(days=offset)).strftime("%Y-%m-%d")
        check_path = os.path.join(DATA_DIR, f"{check_date}.json")
        if os.path.exists(check_path):
            return check_date
    return None


def run_current(today: str) -> int:
    """Normal mode: collect current week's data and generate README."""
    logger.info(f"=== OpenRouter Revenue Stats Collection: {today} ===")

    # Check for an existing snapshot within the current week to avoid duplicates
    existing = _find_recent_snapshot(today, days_back=6)
    if existing:
        logger.info(
            f"  Snapshot already exists for {existing} (within the last 7 days). "
            "Skipping collection to avoid duplicates."
        )
        # Still regenerate README in case code changed
        history = load_history()
        if history:
            readme_content = generate_readme(history[-1], history)
            with open(README_PATH, "w") as f:
                f.write(readme_content)
            logger.info(f"  README regenerated from existing data.")
        return 0

    # Step 1: Fetch model pricing from the API
    logger.info("Step 1: Fetching model pricing from API...")
    pricing = fetch_model_pricing()
    logger.info(f"  Loaded pricing for {len(pricing)} model entries")

    # Step 2: Scrape the rankings page
    logger.info("Step 2: Scraping rankings page...")
    rankings = scrape_rankings()
    if not rankings:
        logger.error("  No models found on rankings page! Aborting.")
        return 1
    logger.info(f"  Found {len(rankings)} ranked models")

    # Step 3: Scrape activity data for each ranked model
    logger.info("Step 3: Scraping model activity pages...")
    activities = scrape_all_model_activities(rankings)
    models_with_activity = sum(
        1 for a in activities.values()
        if a.get("prompt_tokens", 0) > 0 or a.get("completion_tokens", 0) > 0
    )
    logger.info(f"  Got activity data for {models_with_activity}/{len(rankings)} models")

    # Step 4: Calculate revenue
    logger.info("Step 4: Calculating revenue...")
    revenue_data = calculate_revenue(rankings, activities, pricing)
    logger.info(f"  Total estimated revenue: ${revenue_data['total_revenue']:,.2f}")
    logger.info(f"  Total tokens tracked: {revenue_data['total_tokens']:,}")

    # Step 5: Save snapshot
    logger.info("Step 5: Saving snapshot...")
    snapshot = {"date": today, **revenue_data}
    save_snapshot(snapshot, today)

    # Step 6: Generate README
    logger.info("Step 6: Generating README...")
    history = load_history()
    readme_content = generate_readme(snapshot, history)
    with open(README_PATH, "w") as f:
        f.write(readme_content)
    logger.info(f"  README written to {README_PATH}")

    _log_summary(revenue_data, today)
    return 0


def run_backfill(num_weeks: int, today: str) -> int:
    """Backfill mode: generate historical weekly snapshots.

    Uses the rankings page's embedded chart data to identify which models were
    in the top 10 each historical week (these change every week). Then fetches
    daily analytics from each unique model's page to compute prompt/completion
    ratios and cached token counts for accurate revenue calculation.
    """
    logger.info(f"=== Backfill Mode: generating {num_weeks} weeks of history ===")

    # Step 1: Fetch model pricing
    logger.info("Step 1: Fetching model pricing from API...")
    pricing = fetch_model_pricing()
    logger.info(f"  Loaded pricing for {len(pricing)} model entries")

    # Step 2: Scrape rankings page -- both current leaderboard and historical chart
    logger.info("Step 2: Scraping rankings page (current + historical chart)...")
    resp = requests.get("https://openrouter.ai/rankings", headers=SCRAPER_HEADERS, timeout=30)
    resp.raise_for_status()
    rankings_html = resp.text

    history_weeks = scrape_rankings_history(html=rankings_html)
    if not history_weeks:
        logger.error("  No historical chart data found! Aborting.")
        return 1

    # Select the target weeks, excluding the partial current week
    last_entry = history_weeks[-1]
    last_date = datetime.strptime(last_entry["week_start"], "%Y-%m-%d")
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    # If the last entry's week_start is within the current week, it's partial
    if (today_dt - last_date).days < 7:
        complete_weeks = history_weeks[:-1]
    else:
        complete_weeks = history_weeks

    # num_weeks=0 means all available
    if num_weeks > 0:
        target_weeks = complete_weeks[-num_weeks:]
    else:
        target_weeks = complete_weeks
    logger.info(f"  Selected {len(target_weeks)} target weeks for backfill")
    for tw in target_weeks:
        total_t = tw["total"] / 1e12
        logger.info(f"    {tw['week_start']}: {len(tw['models'])} named models, {total_t:.2f}T total")

    # Step 3: Collect all unique model slugs across target weeks
    all_slugs = set()
    for week_data in target_weeks:
        all_slugs.update(week_data["models"].keys())
    logger.info(f"\nStep 3: {len(all_slugs)} unique model slugs across all target weeks")

    # Step 4: Fetch daily analytics for each unique model (one request per model)
    logger.info("Step 4: Fetching daily analytics for all unique models...")
    all_daily_data: dict[str, dict[str, dict]] = {}
    for i, slug in enumerate(sorted(all_slugs)):
        logger.info(f"  [{i+1}/{len(all_slugs)}] {slug}")
        all_daily_data[slug] = scrape_model_daily_data(slug)
        if i < len(all_slugs) - 1:
            time.sleep(REQUEST_DELAY)

    # Build a name lookup: try pricing first, then use the slug's model part
    name_lookup = {}
    for slug in all_slugs:
        # Check pricing map for a display name
        if slug in pricing and pricing[slug].get("name"):
            name_lookup[slug] = pricing[slug]["name"]
        else:
            base = slug.split(":")[0]
            if base in pricing and pricing[base].get("name"):
                name_lookup[slug] = pricing[base]["name"]
            else:
                # Derive a name from the slug: "author/model-name" -> "Model Name"
                model_part = slug.split("/")[-1].split(":")[0]
                name_lookup[slug] = model_part.replace("-", " ").title()

    # Step 5: Generate weekly snapshots
    logger.info(f"\nStep 5: Calculating {len(target_weeks)} weekly snapshots...")

    for i, week_data in enumerate(target_weeks):
        week_start = week_data["week_start"]
        week_start_dt = datetime.strptime(week_start, "%Y-%m-%d")
        week_end_dt = week_start_dt + timedelta(days=6)
        week_end = week_end_dt.strftime("%Y-%m-%d")

        logger.info(f"\n--- Week {i+1}/{len(target_weeks)}: {week_start} to {week_end} ---")

        # Build rankings list from the chart data for this week
        week_models = week_data["models"]  # slug -> token count

        # Get previous week for WoW calculation
        prev_idx = target_weeks.index(week_data) - 1
        prev_models = {}
        if i > 0:
            prev_models = target_weeks[i - 1]["models"]
        elif len(complete_weeks) > len(target_weeks):
            # Look further back in history
            full_idx = complete_weeks.index(week_data) - 1
            if full_idx >= 0:
                prev_models = complete_weeks[full_idx]["models"]

        # Build activity dicts from daily analytics for this week's window
        activities = {}
        rankings_list = []
        rank = 0

        # Sort models by token count descending
        sorted_models = sorted(week_models.items(), key=lambda x: x[1], reverse=True)

        for slug, chart_tokens in sorted_models:
            rank += 1
            daily = all_daily_data.get(slug, {})
            activity = sum_daily_window(daily, week_end, days=7, skip_partial=False)
            activities[slug] = activity

            # WoW % change
            prev_tokens = prev_models.get(slug, 0)
            if prev_tokens > 0:
                pct_change = round((chart_tokens - prev_tokens) / prev_tokens * 100)
            else:
                pct_change = 0

            name = name_lookup.get(slug, slug.split("/")[-1])

            rankings_list.append({
                "rank": rank,
                "slug": slug,
                "name": name,
                "total_tokens": chart_tokens,
                "percent_change": pct_change,
            })

        # Calculate revenue
        revenue_data = calculate_revenue(rankings_list, activities, pricing)

        # Save snapshot (use the week-ending Sunday as the date)
        snapshot = {"date": week_end, **revenue_data}
        save_snapshot(snapshot, week_end)

        logger.info(
            f"  Revenue: ${revenue_data['total_revenue']:,.2f} | "
            f"Tokens: {revenue_data['total_tokens']:,} | "
            f"Models: {len(sorted_models)} named + Others"
        )

    # Step 6: Regenerate README with full history
    logger.info("\nStep 6: Generating README with full history...")
    history = load_history()
    if history:
        latest_snapshot = history[-1]
    else:
        latest_snapshot = {"date": today}

    readme_content = generate_readme(latest_snapshot, history)
    with open(README_PATH, "w") as f:
        f.write(readme_content)
    logger.info(f"  README written to {README_PATH}")

    logger.info(f"\n=== Backfill complete! Generated {len(target_weeks)} weekly snapshots ===")
    return 0


def save_snapshot(snapshot: dict, date: str):
    """Save a revenue snapshot to data/{date}.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{date}.json")
    with open(filepath, "w") as f:
        json.dump(snapshot, f, indent=2)
    logger.info(f"  Snapshot saved to {filepath}")


def _log_summary(revenue_data: dict, today: str):
    logger.info("=== Collection complete! ===")
    logger.info(f"  Snapshot: data/{today}.json")
    logger.info(f"  README: {README_PATH}")
    logger.info(f"  Revenue: ${revenue_data['total_revenue']:,.2f}")
    logger.info(f"  Models: {revenue_data['total_models']} "
                f"({revenue_data['paid_models']} paid, {revenue_data['free_models']} free)")


if __name__ == "__main__":
    sys.exit(main())
