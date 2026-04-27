# OpenRouter Inference Revenue Statistics

> Estimated inference revenue across models on [OpenRouter](https://openrouter.ai/rankings), calculated from public usage data and pricing.

**Last updated:** 2026-04-27

## Summary

| Metric | Value |
|--------|-------|
| Estimated Weekly Revenue | **$17.89M** |
| Total Tokens Tracked | **10.00T** |
| Models Tracked | **10** (10 paid, 0 free) |

## Revenue Over Time

```mermaid
xychart-beta
    title "Estimated Weekly Revenue (USD)"
    x-axis ["11/16", "11/23", "11/30", "12/07", "12/14", "12/21", "12/28", "1/04", "1/11", "1/18", "1/25", "2/01", "2/08", "2/16", "2/23", "3/02", "3/09", "3/16", "3/23", "3/30", "4/06", "4/13", "4/20", "4/27"]
    y-axis "Revenue ($)" 0 --> 30000000
    bar [2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3084659.53, 2918272.88, 2862056.98, 4558077.75, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 7177565.34, 9116055.43, 10024024.86, 8991833.66, 9781034.43, 13516359.09, 17042158.26, 14398956.04, 13440739.33, 14964047.88, 17890596.37]
    line [2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3084659.53, 2918272.88, 2862056.98, 4558077.75, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 7177565.34, 9116055.43, 10024024.86, 8991833.66, 9781034.43, 13516359.09, 17042158.26, 14398956.04, 13440739.33, 14964047.88, 17890596.37]
```

## Revenue by Model (Top 10)

```mermaid
xychart-beta
    title "Estimated Weekly Revenue by Model"
    x-axis ["Opus 4.7", "Sonnet 4.6", "Opus 4.6", "Kimi K2.6", "Gem 3 Fl Prev", "Deepseek V3.2", "Minimax M2.7", "Grok 4.1 Fast", "Gem 2.5 Fl L..", "Step 3.5 Fl"]
    y-axis "Revenue ($)" 0 --> 8000000
    bar [6391288.14, 4590909.47, 3822175.74, 1453994.43, 667755.29, 339165.13, 283277.94, 180219.96, 87132.63, 74677.64]
```

## Revenue Share

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'pie1': '#FF6384', 'pie2': '#36A2EB', 'pie3': '#FFCE56', 'pie4': '#4BC0C0', 'pie5': '#9966FF', 'pie6': '#FF9F40', 'pie7': '#2ECC71', 'pie8': '#FF66B2', 'pie9': '#00CCFF', 'pie10': '#E74C3C', 'pie11': '#F39C12', 'pie12': '#1ABC9C'}}}%%
pie
    title Revenue Share by Model
    "Claude Opus 4.7 $6.39M" : 6391288.14
    "Claude Sonnet 4.6 $4.59M" : 4590909.47
    "Claude Opus 4.6 $3.82M" : 3822175.74
    "Kimi K2.6 $1.45M" : 1453994.43
    "Gemini 3 Flash Preview $667.8K" : 667755.29
    "Deepseek V3.2 $339.2K" : 339165.13
    "Minimax M2.7 $283.3K" : 283277.94
    "Grok 4.1 Fast $180.2K" : 180219.96
    "Gemini 2.5 Flash Lite $87.1K" : 87132.63
    "Step 3.5 Flash $74.7K" : 74677.64
```

## Token Type Distribution

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'pie1': '#FF6384', 'pie2': '#36A2EB', 'pie3': '#FFCE56', 'pie4': '#4BC0C0', 'pie5': '#9966FF', 'pie6': '#FF9F40', 'pie7': '#2ECC71', 'pie8': '#FF66B2', 'pie9': '#00CCFF', 'pie10': '#E74C3C', 'pie11': '#F39C12', 'pie12': '#1ABC9C'}}}%%
pie
    title Token Distribution Across All Tracked Models
    "Prompt Tokens - 9.68T" : 9682470087353
    "Cached Input Tokens - 5.99T" : 5990230217122
    "Response Tokens - 234.0B" : 234011705130
    "Reasoning Tokens - 82.9B" : 82887769404
```

## Model Breakdown

| Rank | Model | Total Tokens | Cached | Prompt % | Compl. % | Input Price | Output Price | Est. Revenue | WoW |
|------|-------|-------------|--------|----------|----------|-------------|-------------|-------------|-----|
| 4 | [Claude Opus 4.7](https://openrouter.ai/anthropic/claude-4.7-opus-20260416) | 1.15T | 905.6B | 99.2% | 0.8% | $5.00/M | $25.00/M | $6.39M | +279% |
| 2 | [Claude Sonnet 4.6](https://openrouter.ai/anthropic/claude-4.6-sonnet-20260217) | 1.36T | 941.1B | 98.5% | 1.5% | $3.00/M | $15.00/M | $4.59M | -2% |
| 9 | [Claude Opus 4.6](https://openrouter.ai/anthropic/claude-4.6-opus-20260205) | 685.0B | 458.0B | 98.8% | 1.2% | $5.00/M | $25.00/M | $3.82M | -44% |
| 1 | [Kimi K2.6](https://openrouter.ai/moonshotai/kimi-k2.6-20260420) | 1.58T | 1.37T | 98.8% | 1.2% | $0.7448/M | $4.66/M | $1.45M | 0% |
| 5 | [Gemini 3 Flash Preview](https://openrouter.ai/google/gemini-3-flash-preview-20251217) | 1.04T | 364.9B | 95.0% | 5.0% | $0.5000/M | $3.00/M | $667.8K | -9% |
| 3 | [Deepseek V3.2](https://openrouter.ai/deepseek/deepseek-v3.2-20251201) | 1.28T | 460.7B | 96.4% | 3.6% | $0.2520/M | $0.3780/M | $339.2K | 0% |
| 6 | [Minimax M2.7](https://openrouter.ai/minimax/minimax-m2.7-20260318) | 790.0B | 539.5B | 98.0% | 2.0% | $0.3000/M | $1.20/M | $283.3K | -18% |
| 7 | [Grok 4.1 Fast](https://openrouter.ai/x-ai/grok-4.1-fast) | 747.0B | 240.4B | 91.6% | 8.4% | $0.2000/M | $0.5000/M | $180.2K | +30% |
| 10 | [Gemini 2.5 Flash Lite](https://openrouter.ai/google/gemini-2.5-flash-lite) | 651.0B | 105.0B | 89.2% | 10.8% | $0.1000/M | $0.4000/M | $87.1K | +9% |
| 8 | [Step 3.5 Flash](https://openrouter.ai/stepfun/step-3.5-flash) | 721.0B | 602.4B | 98.2% | 1.8% | $0.1000/M | $0.3000/M | $74.7K | +98% |

## Methodology

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

*Data collected by [openrouter-inference-stats](https://github.com/johnbean393/openrouter-inference-stats) and updated weekly via GitHub Actions.*
