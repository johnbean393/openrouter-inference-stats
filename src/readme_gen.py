"""Generate README.md with Mermaid charts and statistics tables."""

import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def format_tokens(count: int) -> str:
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


def format_dollars(amount: float) -> str:
    """Format dollar amounts with appropriate precision."""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    return f"${amount:,.2f}"


def _sanitize_mermaid_label(text: str) -> str:
    """Sanitize text for use in Mermaid labels (remove special chars)."""
    # Remove characters that break Mermaid syntax
    text = text.replace('"', "'")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace("#", "")
    text = text.replace(":", " -")
    text = text.replace(";", "")
    return text.strip()


def _truncate_label(text: str, max_len: int = 20) -> str:
    """Truncate label for chart readability.

    If the text is in "Provider - Model Name" format, extracts just the model
    name to avoid multiple labels showing "Anthropic - Cl.." ambiguously.
    """
    text = _sanitize_mermaid_label(text)
    # Extract model name from "Provider - Model Name" format
    if " - " in text:
        text = text.split(" - ", 1)[1]
    if len(text) > max_len:
        return text[:max_len - 2] + ".."
    return text


def load_history() -> list[dict]:
    """Load all historical snapshots from the data directory.

    Returns a list of snapshots sorted by date ascending.
    """
    snapshots = []
    if not os.path.isdir(DATA_DIR):
        return snapshots

    for filename in sorted(os.listdir(DATA_DIR)):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                snapshots.append(data)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load {filepath}: {e}")

    return snapshots


def generate_readme(snapshot: dict, history: list[dict] | None = None) -> str:
    """Generate the full README.md content.

    Args:
        snapshot: Current revenue data from calculate_revenue()
        history: List of all historical snapshots (including current)

    Returns:
        README markdown string
    """
    if history is None:
        history = load_history()

    date = snapshot.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
    models = snapshot.get("models", [])
    total_revenue = snapshot.get("total_revenue", 0)
    total_tokens = snapshot.get("total_tokens", 0)
    total_models = snapshot.get("total_models", 0)
    paid_models = snapshot.get("paid_models", 0)
    free_models = snapshot.get("free_models", 0)
    token_breakdown = snapshot.get("token_breakdown", {})

    sections = []

    # --- Header ---
    sections.append(_generate_header(date))

    # --- Summary Stats ---
    sections.append(_generate_summary(
        total_revenue, total_tokens, total_models, paid_models, free_models
    ))

    # --- Revenue Over Time (line chart) ---
    if len(history) > 0:
        sections.append(_generate_revenue_over_time_chart(history))

    # --- Revenue by Model (bar chart) ---
    paid_models_list = [m for m in models if not m.get("is_free", False)]
    if paid_models_list:
        sections.append(_generate_revenue_bar_chart(paid_models_list[:10]))

    # --- Revenue Share (pie chart) ---
    if paid_models_list:
        sections.append(_generate_revenue_pie_chart(paid_models_list[:10], total_revenue))

    # --- Token Distribution (pie chart) ---
    if token_breakdown:
        sections.append(_generate_token_distribution_chart(token_breakdown))

    # --- Detailed Table ---
    if models:
        sections.append(_generate_model_table(models))

    # --- Methodology ---
    sections.append(_generate_methodology())

    return "\n\n".join(sections) + "\n"


def _generate_header(date: str) -> str:
    return f"""# OpenRouter Inference Revenue Statistics

> Estimated inference revenue across models on [OpenRouter](https://openrouter.ai/rankings), calculated from public usage data and pricing.

**Last updated:** {date}"""


def _generate_summary(
    total_revenue: float,
    total_tokens: int,
    total_models: int,
    paid_models: int,
    free_models: int,
) -> str:
    return f"""## Summary

| Metric | Value |
|--------|-------|
| Estimated Weekly Revenue | **{format_dollars(total_revenue)}** |
| Total Tokens Tracked | **{format_tokens(total_tokens)}** |
| Models Tracked | **{total_models}** ({paid_models} paid, {free_models} free) |"""


def _generate_revenue_over_time_chart(history: list[dict]) -> str:
    """Generate a Mermaid xychart for revenue over time."""
    if len(history) < 1:
        return ""

    dates = []
    revenues = []

    # Show every Nth label to avoid x-axis crowding (~13 visible labels)
    label_interval = max(1, len(history) // 13)

    for i, snap in enumerate(history):
        d = snap.get("date", "?")
        r = snap.get("total_revenue", 0)
        revenues.append(round(r, 2))

        # Only show a label at regular intervals and the last entry
        if i % label_interval == 0 or i == len(history) - 1:
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                dates.append(f'"{dt.strftime("%b %d, %y")}"')
            except ValueError:
                dates.append(f'"{d}"')
        else:
            dates.append('" "')

    x_axis = ", ".join(dates)
    y_values = ", ".join(str(r) for r in revenues)

    max_rev = max(revenues) if revenues else 1000
    y_max = _nice_axis_max(max_rev)

    return f"""## Revenue Over Time

```mermaid
xychart-beta
    title "Estimated Weekly Revenue"
    x-axis [{x_axis}]
    y-axis "Revenue ($)" 0 --> {y_max}
    bar [{y_values}]
    line [{y_values}]
```"""


def _generate_revenue_bar_chart(models: list[dict]) -> str:
    """Generate a Mermaid xychart bar chart for top model revenue."""
    labels = []
    values = []
    for m in models:
        label = _truncate_label(m["name"], 20)
        labels.append(f'"{label}"')
        values.append(round(m["estimated_revenue"], 2))

    x_axis = ", ".join(labels)
    y_values = ", ".join(str(v) for v in values)

    max_val = max(values) if values else 1000
    y_max = _nice_axis_max(max_val)

    return f"""## Revenue by Model (Top {len(models)})

```mermaid
xychart-beta
    title "Estimated Weekly Revenue by Model"
    x-axis [{x_axis}]
    y-axis "Revenue ($)" 0 --> {y_max}
    bar [{y_values}]
```"""


def _generate_revenue_pie_chart(models: list[dict], total_revenue: float) -> str:
    """Generate a Mermaid pie chart for revenue share."""
    lines = []
    shown_revenue = 0
    for m in models:
        label = _sanitize_mermaid_label(m["name"])
        rev = m["estimated_revenue"]
        shown_revenue += rev
        formatted_rev = format_dollars(rev)
        lines.append(f'    "{label} {formatted_rev}" : {round(rev, 2)}')

    # Add "Other" for remaining revenue
    other = total_revenue - shown_revenue
    if other > 0:
        formatted_other = format_dollars(other)
        lines.append(f'    "Other {formatted_other}" : {round(other, 2)}')

    pie_data = "\n".join(lines)

    return f"""## Revenue Share

```mermaid
pie
    title Revenue Share by Model
{pie_data}
```"""


def _generate_token_distribution_chart(token_breakdown: dict) -> str:
    """Generate a Mermaid pie chart for token type distribution."""
    prompt = token_breakdown.get("prompt_tokens", 0)
    completion = token_breakdown.get("completion_tokens", 0)
    reasoning = token_breakdown.get("reasoning_tokens", 0)
    cached = token_breakdown.get("cached_tokens", 0)

    # Note: completion includes reasoning (OpenAI convention).
    # For the chart, show completion-minus-reasoning as "Response Tokens"
    # and reasoning separately.
    response_only = max(0, completion - reasoning)

    lines = []
    if prompt > 0:
        lines.append(f'    "Prompt Tokens - {format_tokens(prompt)}" : {prompt}')
    if cached > 0:
        lines.append(f'    "Cached Input Tokens - {format_tokens(cached)}" : {cached}')
    if response_only > 0:
        lines.append(f'    "Response Tokens - {format_tokens(response_only)}" : {response_only}')
    if reasoning > 0:
        lines.append(f'    "Reasoning Tokens - {format_tokens(reasoning)}" : {reasoning}')

    if not lines:
        return ""

    pie_data = "\n".join(lines)

    return f"""## Token Type Distribution

```mermaid
pie
    title Token Distribution Across All Tracked Models
{pie_data}
```"""


def _generate_model_table(models: list[dict]) -> str:
    """Generate a detailed markdown table of all models."""
    header = (
        "## Model Breakdown\n\n"
        "| Rank | Model | Total Tokens | Cached | Prompt % | Compl. % "
        "| Input Price | Output Price | Est. Revenue | WoW |\n"
        "|------|-------|-------------|--------|----------|----------"
        "|-------------|-------------|-------------|-----|\n"
    )

    rows = []
    for m in models:
        rank = m["rank"]
        name = m["name"]
        slug = m["slug"]
        tokens = format_tokens(m["total_tokens"])
        cached = format_tokens(m.get("cached_tokens", 0))
        p_ratio = f"{m['prompt_ratio'] * 100:.1f}%"
        c_ratio = f"{m['completion_ratio'] * 100:.1f}%"
        p_price = _format_price_per_m(m["prompt_price"])
        c_price = _format_price_per_m(m["completion_price"])
        revenue = format_dollars(m["estimated_revenue"])
        wow = _format_wow(m.get("percent_change", 0))

        link = f"[{name}](https://openrouter.ai/{slug})"
        rows.append(
            f"| {rank} | {link} | {tokens} | {cached} | {p_ratio} | {c_ratio} "
            f"| {p_price} | {c_price} | {revenue} | {wow} |"
        )

    return header + "\n".join(rows)


def _generate_methodology() -> str:
    return """## Methodology

This data is collected automatically from public sources:

1. **Model Pricing**: Fetched from the [OpenRouter API](https://openrouter.ai/api/v1/models) — per-token prices for prompt, completion, reasoning, and cache reads
2. **Usage Rankings**: Scraped from the [OpenRouter Rankings](https://openrouter.ai/rankings) page — top models by weekly token volume
3. **Token Breakdown**: Extracted from each model page's embedded daily analytics data — exact daily counts of prompt, completion, reasoning, and cached input tokens, summed over the most recent 7 full days

**Revenue Calculation**:
- `revenue = prompt_tokens × prompt_price + completion_tokens × output_price + cached_tokens × cache_read_price`
- Completion tokens include reasoning tokens (standard OpenAI convention); reasoning is **not** double-counted
- Cached input tokens are charged at the discounted `input_cache_read` rate

**Caveats**:
- Revenue estimates use list prices; actual revenue may differ due to volume discounts or BYOK usage
- Only the top models from the rankings page are tracked; the long tail of smaller models is not included
- Free models (price = $0) contribute $0 to revenue regardless of usage volume

---

*Data collected by [openrouter-inference-stats](https://github.com/johnbean393/openrouter-inference-stats) and updated weekly via GitHub Actions.*"""


def _format_price_per_m(price_per_token: float) -> str:
    """Format price as $/M tokens."""
    if price_per_token == 0:
        return "Free"
    per_million = price_per_token * 1_000_000
    if per_million >= 1:
        return f"${per_million:.2f}/M"
    return f"${per_million:.4f}/M"


def _format_wow(pct: int) -> str:
    """Format week-over-week percentage change."""
    if pct > 0:
        return f"+{pct}%"
    if pct < 0:
        return f"{pct}%"
    return "0%"


def _nice_axis_max(value: float) -> int:
    """Calculate a nice round max value for chart axes."""
    if value <= 0:
        return 1000
    # Round up to a nice number
    import math
    magnitude = 10 ** math.floor(math.log10(value))
    normalized = value / magnitude
    if normalized <= 1.5:
        nice = 2
    elif normalized <= 3:
        nice = 3
    elif normalized <= 5:
        nice = 5
    elif normalized <= 7.5:
        nice = 8
    else:
        nice = 10
    return int(nice * magnitude)
