# OpenRouter Inference Revenue Statistics

> Estimated inference revenue across models on [OpenRouter](https://openrouter.ai/rankings), calculated from public usage data and pricing.

**Last updated:** 2026-02-23

## Summary

| Metric | Value |
|--------|-------|
| Estimated Weekly Revenue | **$9.12M** |
| Total Tokens Tracked | **8.74T** |
| Models Tracked | **10** (9 paid, 1 free) |

## Revenue Over Time

```mermaid
xychart-beta
    title "Estimated Weekly Revenue (USD)"
    x-axis ["11/16", "11/23", "11/30", "12/07", "12/14", "12/21", "12/28", "1/04", "1/11", "1/18", "1/25", "2/01", "2/08", "2/16", "2/23"]
    y-axis "Revenue ($)" 0 --> 10000000
    bar [2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3084659.53, 2918272.88, 2862056.98, 4558077.75, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 7177565.34, 9116055.43]
    line [2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3084659.53, 2918272.88, 2862056.98, 4558077.75, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 7177565.34, 9116055.43]
```

## Revenue by Model (Top 9)

```mermaid
xychart-beta
    title "Estimated Weekly Revenue by Model"
    x-axis ["Opus 4.6", "Sonnet 4.5", "Minimax M2.5", "GLM 5", "Kimi K2.5 0127", "Gem 3 Fl Prev", "Deepseek V3.2", "Gem 2.5 Fl", "Grok 4.1 Fast"]
    y-axis "Revenue ($)" 0 --> 5000000
    bar [3589968.98, 1834921.17, 1101083.88, 784262.88, 670464.58, 538467.05, 226573.58, 199328.9, 170984.42]
```

## Revenue Share

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'pie1': '#FF6384', 'pie2': '#36A2EB', 'pie3': '#FFCE56', 'pie4': '#4BC0C0', 'pie5': '#9966FF', 'pie6': '#FF9F40', 'pie7': '#2ECC71', 'pie8': '#FF66B2', 'pie9': '#00CCFF', 'pie10': '#E74C3C', 'pie11': '#F39C12', 'pie12': '#1ABC9C'}}}%%
pie
    title Revenue Share by Model
    "Claude Opus 4.6 $3.59M" : 3589968.98
    "Claude Sonnet 4.5 $1.83M" : 1834921.17
    "Minimax M2.5 $1.10M" : 1101083.88
    "GLM 5 $784.3K" : 784262.88
    "Kimi K2.5 0127 $670.5K" : 670464.58
    "Gemini 3 Flash Preview $538.5K" : 538467.05
    "Deepseek V3.2 $226.6K" : 226573.58
    "Gemini 2.5 Flash $199.3K" : 199328.9
    "Grok 4.1 Fast $171.0K" : 170984.42
```

## Token Type Distribution

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'pie1': '#FF6384', 'pie2': '#36A2EB', 'pie3': '#FFCE56', 'pie4': '#4BC0C0', 'pie5': '#9966FF', 'pie6': '#FF9F40', 'pie7': '#2ECC71', 'pie8': '#FF66B2', 'pie9': '#00CCFF', 'pie10': '#E74C3C', 'pie11': '#F39C12', 'pie12': '#1ABC9C'}}}%%
pie
    title Token Distribution Across All Tracked Models
    "Prompt Tokens - 8.47T" : 8472214189635
    "Cached Input Tokens - 5.03T" : 5033002752958
    "Response Tokens - 166.3B" : 166269912014
    "Reasoning Tokens - 103.6B" : 103589768344
```

## Model Breakdown

| Rank | Model | Total Tokens | Cached | Prompt % | Compl. % | Input Price | Output Price | Est. Revenue | WoW |
|------|-------|-------------|--------|----------|----------|-------------|-------------|-------------|-----|
| 7 | [Claude Opus 4.6](https://openrouter.ai/anthropic/claude-4.6-opus-20260205) | 643.0B | 436.5B | 98.8% | 1.2% | $5.00/M | $25.00/M | $3.59M | +23% |
| 8 | [Claude Sonnet 4.5](https://openrouter.ai/anthropic/claude-4.5-sonnet-20250929) | 534.0B | 355.2B | 98.0% | 2.0% | $3.00/M | $15.00/M | $1.83M | -15% |
| 1 | [Minimax M2.5](https://openrouter.ai/minimax/minimax-m2.5-20260211) | 2.57T | 2.08T | 99.1% | 0.9% | $0.3000/M | $1.10/M | $1.10M | +79% |
| 4 | [GLM 5](https://openrouter.ai/z-ai/glm-5-20260211) | 803.0B | 462.8B | 98.4% | 1.6% | $0.9500/M | $2.55/M | $784.3K | +28% |
| 2 | [Kimi K2.5 0127](https://openrouter.ai/moonshotai/kimi-k2.5-0127) | 1.04T | 796.0B | 98.6% | 1.4% | $0.4500/M | $2.20/M | $670.5K | -20% |
| 3 | [Gemini 3 Flash Preview](https://openrouter.ai/google/gemini-3-flash-preview-20251217) | 859.0B | 398.2B | 95.9% | 4.2% | $0.5000/M | $3.00/M | $538.5K | +11% |
| 5 | [Deepseek V3.2](https://openrouter.ai/deepseek/deepseek-v3.2-20251201) | 745.0B | 225.1B | 96.0% | 4.0% | $0.2600/M | $0.3800/M | $226.6K | -2% |
| 10 | [Gemini 2.5 Flash](https://openrouter.ai/google/gemini-2.5-flash) | 431.0B | 123.4B | 93.0% | 7.0% | $0.3000/M | $2.50/M | $199.3K | -4% |
| 6 | [Grok 4.1 Fast](https://openrouter.ai/x-ai/grok-4.1-fast) | 669.0B | 157.7B | 85.4% | 14.6% | $0.2000/M | $0.5000/M | $171.0K | +20% |
| 9 | [Trinity Large Preview (free)](https://openrouter.ai/arcee-ai/trinity-large-preview:free) | 449.0B | 0 | 98.1% | 1.9% | Free | Free | $0.00 | +2% |

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
