# OpenRouter Inference Revenue Statistics

> Estimated inference revenue across models on [OpenRouter](https://openrouter.ai/rankings), calculated from public usage data and pricing.

**Last updated:** 2026-02-09

## Summary

| Metric | Value |
|--------|-------|
| Estimated Weekly Revenue | **$6.25M** |
| Total Tokens Tracked | **5.57T** |
| Models Tracked | **10** (9 paid, 1 free) |

## Revenue Over Time

```mermaid
xychart-beta
    title "Estimated Weekly Revenue (USD)"
    x-axis ["2025-02-16", "2025-02-23", "2025-03-02", "2025-03-09", "2025-03-16", "2025-03-23", "2025-03-30", "2025-04-06", "2025-04-13", "2025-04-20", "2025-04-27", "2025-05-04", "2025-05-11", "2025-05-18", "2025-05-25", "2025-06-01", "2025-06-08", "2025-06-15", "2025-06-22", "2025-06-29", "2025-07-06", "2025-07-13", "2025-07-20", "2025-07-27", "2025-08-03", "2025-08-10", "2025-08-17", "2025-08-24", "2025-08-31", "2025-09-07", "2025-09-14", "2025-09-21", "2025-09-28", "2025-10-05", "2025-10-12", "2025-10-19", "2025-10-26", "2025-11-02", "2025-11-09", "2025-11-16", "2025-11-23", "2025-11-30", "2025-12-07", "2025-12-14", "2025-12-21", "2025-12-28", "2026-01-04", "2026-01-11", "2026-01-18", "2026-01-25", "2026-02-01", "2026-02-08", "2026-02-09"]
    y-axis "Revenue (USD)" 0 --> 8000000
    bar [3636551.37, 3187190.68, 2898697.3, 2605824.47, 3173095.31, 3351464.84, 2856644.26, 2374925.71, 2606266.76, 2864094.45, 2493470.82, 2625648.87, 2431249.99, 2596439.07, 3068070.35, 3377334.62, 2934973.17, 2864505.98, 3207616.69, 2851460.78, 2986409.46, 2980604.88, 3699767.67, 4604563.18, 4944814.68, 4358341.87, 4407794.13, 4302491.62, 4195641.45, 4448167.36, 4505578.6, 4197140.38, 5061241.31, 4451596.96, 5279274.27, 4966022.01, 5100915.23, 6002432.08, 6057878.44, 2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3106880.8, 2967779.11, 2907694.56, 4609777.81, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 6247827.58]
    line [3636551.37, 3187190.68, 2898697.3, 2605824.47, 3173095.31, 3351464.84, 2856644.26, 2374925.71, 2606266.76, 2864094.45, 2493470.82, 2625648.87, 2431249.99, 2596439.07, 3068070.35, 3377334.62, 2934973.17, 2864505.98, 3207616.69, 2851460.78, 2986409.46, 2980604.88, 3699767.67, 4604563.18, 4944814.68, 4358341.87, 4407794.13, 4302491.62, 4195641.45, 4448167.36, 4505578.6, 4197140.38, 5061241.31, 4451596.96, 5279274.27, 4966022.01, 5100915.23, 6002432.08, 6057878.44, 2740620.94, 2816925.48, 2523142.13, 3991396.39, 3551394.6, 3106880.8, 2967779.11, 2907694.56, 4609777.81, 7057753.91, 5373700.56, 5970586.37, 6247827.58, 6247827.58]
```

## Revenue by Model (Top 9)

```mermaid
xychart-beta
    title "Estimated Weekly Revenue by Model (USD)"
    x-axis ["Claude Sonnet ..", "Claude Opus 4.5", "Kimi K2.5 0127", "Gemini 3 Flash..", "Gemini 2.5 Flash", "Deepseek V3.2", "Minimax M2.1", "Grok 4.1 Fast", "Gemini 2.5 Fla.."]
    y-axis "Revenue (USD)" 0 --> 3000000
    bar [2397302.04, 2081607.17, 613222.07, 474733.24, 211530.76, 202961.01, 133543.61, 87587.52, 45340.16]
```

## Revenue Share

```mermaid
pie showData
    title Revenue Share by Model
    "Claude Sonnet 4.5" : 2397302.04
    "Claude Opus 4.5" : 2081607.17
    "Kimi K2.5 0127" : 613222.07
    "Gemini 3 Flash Preview" : 474733.24
    "Gemini 2.5 Flash" : 211530.76
    "Deepseek V3.2" : 202961.01
    "Minimax M2.1" : 133543.61
    "Grok 4.1 Fast" : 87587.52
    "Gemini 2.5 Flash Lite" : 45340.16
```

## Token Type Distribution

```mermaid
pie showData
    title Token Distribution Across All Tracked Models
    "Prompt Tokens" : 5349040692037
    "Cached Input Tokens" : 2928357241567
    "Response Tokens" : 159844805519
    "Reasoning Tokens" : 57505324896
```

## Model Breakdown

| Rank | Model | Total Tokens | Cached | Prompt % | Compl. % | Input Price | Output Price | Est. Revenue | WoW |
|------|-------|-------------|--------|----------|----------|-------------|-------------|-------------|-----|
| 3 | [Claude Sonnet 4.5](https://openrouter.ai/anthropic/claude-4.5-sonnet-20250929) | 706.0B | 448.4B | 98.3% | 1.7% | $3.00/M | $15.00/M | $2.40M | -9% |
| 7 | [Claude Opus 4.5](https://openrouter.ai/anthropic/claude-4.5-opus-20251124) | 370.0B | 248.9B | 98.5% | 1.5% | $5.00/M | $25.00/M | $2.08M | -2% |
| 1 | [Kimi K2.5 0127](https://openrouter.ai/moonshotai/kimi-k2.5-0127) | 1.16T | 950.2B | 98.8% | 1.2% | $0.4500/M | $2.25/M | $613.2K | +222% |
| 2 | [Gemini 3 Flash Preview](https://openrouter.ai/google/gemini-3-flash-preview-20251217) | 764.0B | 387.5B | 96.2% | 3.8% | $0.5000/M | $3.00/M | $474.7K | +11% |
| 6 | [Gemini 2.5 Flash](https://openrouter.ai/google/gemini-2.5-flash) | 430.0B | 118.4B | 91.6% | 8.4% | $0.3000/M | $2.50/M | $211.5K | +6% |
| 4 | [Deepseek V3.2](https://openrouter.ai/deepseek/deepseek-v3.2-20251201) | 665.0B | 265.1B | 95.8% | 4.2% | $0.2500/M | $0.3800/M | $203.0K | +31% |
| 5 | [Minimax M2.1](https://openrouter.ai/minimax/minimax-m2.1) | 442.0B | 349.1B | 98.7% | 1.3% | $0.2700/M | $0.9500/M | $133.5K | +88% |
| 8 | [Grok 4.1 Fast](https://openrouter.ai/x-ai/grok-4.1-fast) | 345.0B | 94.8B | 86.6% | 13.4% | $0.2000/M | $0.5000/M | $87.6K | +9% |
| 9 | [Gemini 2.5 Flash Lite](https://openrouter.ai/google/gemini-2.5-flash-lite) | 344.0B | 66.0B | 90.0% | 10.0% | $0.1000/M | $0.4000/M | $45.3K | +16% |
| 10 | [Trinity Large Preview (free)](https://openrouter.ai/arcee-ai/trinity-large-preview:free) | 343.0B | 0 | 98.1% | 1.9% | Free | Free | $0.00 | +226% |

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

*Data collected by [openrouter-inference-stats](https://github.com) and updated weekly via GitHub Actions.*
