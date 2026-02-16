# OpenRouter Inference Revenue Statistics

> Estimated inference revenue across models on [OpenRouter](https://openrouter.ai/rankings), calculated from public usage data and pricing.

**Last updated:** 2026-02-16

## Summary

| Metric | Value |
|--------|-------|
| Estimated Weekly Revenue | **$7.18M** |
| Total Tokens Tracked | **7.50T** |
| Models Tracked | **10** (9 paid, 1 free) |

## Revenue Over Time

```mermaid
xychart-beta
    title "Estimated Weekly Revenue (USD)"
    x-axis ["11/16", "11/23", "11/30", "12/07", "12/14", "12/21", "12/28", "1/04", "1/11", "1/18", "1/25", "2/01", "2/08", "2/16"]
    y-axis "Revenue ($)" 0 --> 8000000
    bar [2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3084659.53, 2918272.88, 2862056.98, 4558077.75, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 7177565.34]
    line [2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3084659.53, 2918272.88, 2862056.98, 4558077.75, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 7177565.34]
```

## Revenue by Model (Top 9)

```mermaid
xychart-beta
    title "Estimated Weekly Revenue by Model"
    x-axis ["Opus 4.6", "Sonnet 4.5", "Gem 3 Fl Prev", "Minimax M2.5", "Kimi K2.5 0127", "Deepseek V3.2", "Gem 2.5 Fl", "GLM 5", "Grok 4.1 Fast"]
    y-axis "Revenue ($)" 0 --> 3000000
    bar [2937276.14, 2139329.21, 486514.54, 475217.5, 343406.68, 224148.12, 214829.69, 213693.92, 143149.55]
```

## Revenue Share

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'pie1': '#FF6384', 'pie2': '#36A2EB', 'pie3': '#FFCE56', 'pie4': '#4BC0C0', 'pie5': '#9966FF', 'pie6': '#FF9F40', 'pie7': '#2ECC71', 'pie8': '#FF66B2', 'pie9': '#00CCFF', 'pie10': '#E74C3C', 'pie11': '#F39C12', 'pie12': '#1ABC9C'}}}%%
pie
    title Revenue Share by Model
    "Claude Opus 4.6 $2.94M" : 2937276.14
    "Claude Sonnet 4.5 $2.14M" : 2139329.21
    "Gemini 3 Flash Preview $486.5K" : 486514.54
    "Minimax M2.5 $475.2K" : 475217.5
    "Kimi K2.5 0127 $343.4K" : 343406.68
    "Deepseek V3.2 $224.1K" : 224148.12
    "Gemini 2.5 Flash $214.8K" : 214829.69
    "GLM 5 $213.7K" : 213693.92
    "Grok 4.1 Fast $143.1K" : 143149.55
```

## Token Type Distribution

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'pie1': '#FF6384', 'pie2': '#36A2EB', 'pie3': '#FFCE56', 'pie4': '#4BC0C0', 'pie5': '#9966FF', 'pie6': '#FF9F40', 'pie7': '#2ECC71', 'pie8': '#FF66B2', 'pie9': '#00CCFF', 'pie10': '#E74C3C', 'pie11': '#F39C12', 'pie12': '#1ABC9C'}}}%%
pie
    title Token Distribution Across All Tracked Models
    "Prompt Tokens - 7.26T" : 7259547764772
    "Cached Input Tokens - 4.48T" : 4476085532789
    "Response Tokens - 149.4B" : 149443376474
    "Reasoning Tokens - 85.4B" : 85448155768
```

## Model Breakdown

| Rank | Model | Total Tokens | Cached | Prompt % | Compl. % | Input Price | Output Price | Est. Revenue | WoW |
|------|-------|-------------|--------|----------|----------|-------------|-------------|-------------|-----|
| 8 | [Claude Opus 4.6](https://openrouter.ai/anthropic/claude-4.6-opus-20260205) | 524.0B | 347.8B | 98.6% | 1.4% | $5.00/M | $25.00/M | $2.94M | +284% |
| 6 | [Claude Sonnet 4.5](https://openrouter.ai/anthropic/claude-4.5-sonnet-20250929) | 627.0B | 393.9B | 98.1% | 1.9% | $3.00/M | $15.00/M | $2.14M | -11% |
| 3 | [Gemini 3 Flash Preview](https://openrouter.ai/google/gemini-3-flash-preview-20251217) | 776.0B | 370.4B | 95.9% | 4.1% | $0.5000/M | $3.00/M | $486.5K | +2% |
| 1 | [Minimax M2.5](https://openrouter.ai/minimax/minimax-m2.5-20260211) | 1.44T | 1.25T | 99.4% | 0.6% | $0.3000/M | $1.20/M | $475.2K | 0% |
| 2 | [Kimi K2.5 0127](https://openrouter.ai/moonshotai/kimi-k2.5-0127) | 1.30T | 1.07T | 98.7% | 1.3% | $0.2300/M | $3.00/M | $343.4K | +12% |
| 4 | [Deepseek V3.2](https://openrouter.ai/deepseek/deepseek-v3.2-20251201) | 757.0B | 246.9B | 95.8% | 4.2% | $0.2500/M | $0.3800/M | $224.1K | +14% |
| 9 | [Gemini 2.5 Flash](https://openrouter.ai/google/gemini-2.5-flash) | 451.0B | 124.1B | 92.3% | 7.7% | $0.3000/M | $2.50/M | $214.8K | +5% |
| 5 | [GLM 5](https://openrouter.ai/z-ai/glm-5-20260211) | 629.0B | 480.0B | 98.2% | 1.8% | $0.3000/M | $2.55/M | $213.7K | 0% |
| 7 | [Grok 4.1 Fast](https://openrouter.ai/x-ai/grok-4.1-fast) | 557.0B | 195.7B | 86.9% | 13.2% | $0.2000/M | $0.5000/M | $143.1K | +62% |
| 10 | [Trinity Large Preview (free)](https://openrouter.ai/arcee-ai/trinity-large-preview:free) | 440.0B | 0 | 98.1% | 1.9% | Free | Free | $0.00 | +28% |

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
