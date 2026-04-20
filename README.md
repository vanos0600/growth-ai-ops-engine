# Growth Experiment Intelligence Engine

**AI-powered experiment analysis tool for Growth teams.**  
Transforms messy, incomplete A/B test data into management-ready reports in seconds.

---

## Quickstart

```bash
pip install streamlit pandas
streamlit run app.py
```

---

## Features

| Feature | What it does |
|---|---|
| **RPI Normalization** | Computes Revenue Per Impression to compare variants with unequal traffic |
| **Data Quality Audit** | Auto-detects missing fields (CTR, conversions) and suggests fixes |
| **Composite Scoring** | Scores variants 0–100 balancing financial performance vs brand risk |
| **Revenue Projections** | Projects monthly revenue if the winning variant is rolled out to 100% traffic |
| **AI Wow Moment** | Calculates the annual $ at stake between best and worst variant |
| **Reusable Prompt Template** | Copy-paste prompt for Claude / GPT-4 to run this analysis on any future experiment |
| **CSV + TXT Export** | One-click export for management reporting |

---

## Input format

Paste a JSON object in the sidebar:

```json
{
  "experiment": "Upsell message test on desktop",
  "market": "USA",
  "duration_days": 10,
  "variants": [
    {
      "name": "A",
      "copy": "Upgrade now for full protection",
      "impressions": 120000,
      "ctr": 2.3,
      "conversion": 0.9,
      "revenue": 4200,
      "notes": ""
    },
    {
      "name": "C",
      "copy": "Your device may be at risk – fix it now",
      "impressions": 110000,
      "ctr": null,
      "conversion": 1.2,
      "revenue": 5100,
      "notes": "negative feedback: too scary"
    }
  ]
}
```

Set `"ctr": null` for missing data — the engine handles it gracefully.

---

## How the analysis works

```
Raw data (messy JSON)
        ↓
compute_metrics()     → RPI, brand risk, winner flag
detect_data_issues()  → structured QA warnings + fix suggestions  
score_variant()       → composite score (RPI × risk penalty)
estimate_monthly_revenue() → 30-day projection at full rollout
generate_report()     → unified management report dict
        ↓
Streamlit dashboard + TXT/CSV export
```

---

## Reusable AI prompt

See the "Reusable prompt template" section in the app, or use this directly:

> *"You are a Senior AI Operations Analyst. Calculate RPI = Revenue/Impressions for each variant. Flag missing data. Score variants 0–100 adjusting for brand risk. Output: Winner, RPI, Revenue lift, Composite score, Monthly projection, Data Health, Brand Risk, Action plan."*

Paste any experiment table after the prompt and any LLM returns a consistent, structured report.

---

Built for the AI Operations Intern case study. ~1 hour to build.
# growth-ai-ops-engine
