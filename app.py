"""
Growth Experiment Intelligence Engine
======================================
AI-powered A/B test analyser for Growth teams.
Turns messy, incomplete experiment data into management-ready decisions in seconds.
"""

import streamlit as st
import pandas as pd
import json
import io
import csv
from datetime import datetime

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Growth AI Ops Engine",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None, "About": None},
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0b0d12 !important;
    color: #dde1e7 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f1117 !important;
    border-right: 1px solid #1c1f2a !important;
    padding-top: 1.5rem !important;
}
section[data-testid="stSidebar"] * { color: #8892a4 !important; }
section[data-testid="stSidebar"] h3 {
    color: #dde1e7 !important; font-size: 13px !important;
    font-weight: 600 !important; letter-spacing: .04em !important;
}
section[data-testid="stSidebar"] input {
    background: #0b0d12 !important; border: 1px solid #262a38 !important;
    color: #6ee7b7 !important; font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Hero metric cards (Tier 1) ── */
.hero-card {
    background: #13161f; border: 1px solid #1e2230;
    border-radius: 14px; padding: 22px 20px 18px;
    position: relative; overflow: hidden;
}
.hero-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    border-radius:14px 14px 0 0;
}
.hero-card.green::before { background: linear-gradient(90deg,#10b981,#34d399); }
.hero-card.amber::before { background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.hero-card.red::before  { background: linear-gradient(90deg,#ef4444,#f87171); }
.hero-card.blue::before  { background: linear-gradient(90deg,#3b82f6,#60a5fa); }
.hero-card.slate::before { background: linear-gradient(90deg,#475569,#64748b); }
.hero-label {
    font-size: 10px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
    color: #4b5568; font-family: 'JetBrains Mono', monospace; margin-bottom: 12px;
}
.hero-value {
    font-size: 30px; font-weight: 600; line-height: 1;
    margin-bottom: 8px; font-family: 'JetBrains Mono', monospace;
}
.hero-value.green { color: #10b981; }
.hero-value.amber { color: #f59e0b; }
.hero-value.red  { color: #ef4444; }
.hero-value.blue  { color: #60a5fa; }
.hero-value.white { color: #f1f5f9; }
.hero-sub { font-size: 11px; color: #3d4657; line-height: 1.5; }

/* ── Verdict banner ── */
.verdict-banner {
    border-radius: 14px; padding: 22px 26px;
    display: flex; align-items: center; gap: 20px; margin-bottom: 4px;
}
.verdict-banner.scale   { background: #041f13; border: 1px solid #10b981; }
.verdict-banner.iterate { background: #1a1100; border: 1px solid #f59e0b; }
.verdict-banner.kill    { background: #180404; border: 1px solid #ef4444; }
.verdict-icon  { font-size: 36px; flex-shrink: 0; line-height: 1; }
.verdict-title {
    font-size: 19px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
    letter-spacing: .04em; margin-bottom: 5px;
}
.verdict-title.scale   { color: #10b981; }
.verdict-title.iterate { color: #f59e0b; }
.verdict-title.kill    { color: #ef4444; }
.verdict-body  { font-size: 13px; color: #8892a4; line-height: 1.65; }
.verdict-body b { color: #dde1e7; font-weight: 500; }

/* ── Insight card ── */
.insight-card {
    background: #13161f; border: 1px solid #1e2230;
    border-radius: 12px; padding: 18px 20px; margin-bottom: 10px;
    font-size: 13px; color: #8892a4; line-height: 1.75;
}
.insight-card b { color: #dde1e7; font-weight: 500; }

/* ── Action steps ── */
.action-step {
    display: flex; gap: 14px; padding: 12px 0;
    border-bottom: 1px solid #181b25; align-items: flex-start;
}
.action-step:last-child { border-bottom: none; }
.action-num {
    width: 26px; height: 26px; border-radius: 50%;
    background: #10b981; color: #022c22; font-size: 11px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px; font-family: 'JetBrains Mono', monospace;
}
.action-title { font-size: 13px; font-weight: 500; color: #dde1e7; margin-bottom: 2px; }
.action-desc  { font-size: 12px; color: #4b5568; line-height: 1.55; }

/* ── Variant rows ── */
.variant-row {
    background: #13161f; border: 1px solid #1e2230; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 8px; display: flex; align-items: center;
}
.variant-row.winner { border-color: #10b981; }
.stat-label {
    font-size: 10px; color: #3d4657; text-transform: uppercase;
    letter-spacing: .06em; margin-bottom: 3px;
    font-family: 'JetBrains Mono', monospace;
}
.stat-value { font-size: 13px; font-weight: 500; color: #dde1e7; font-family: 'JetBrains Mono', monospace; }
.stat-value.miss { color: #ef4444; }
.rpi-bar { background: #1e2230; border-radius: 2px; height: 3px; width: 100%; margin-top: 5px; overflow: hidden; }

/* ── Pills ── */
.pill {
    display: inline-flex; align-items: center; font-size: 10px; font-weight: 600;
    padding: 3px 8px; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: .05em;
}
.pill.green { background: #041f13; color: #10b981; border: 1px solid #10b98140; }
.pill.amber { background: #1a1100; color: #f59e0b; border: 1px solid #f59e0b40; }
.pill.red   { background: #180404; color: #ef4444; border: 1px solid #ef444440; }
.pill.slate { background: #1e2230; color: #64748b; border: 1px solid #2a2d3840; }
.pill.blue  { background: #091930; color: #60a5fa; border: 1px solid #3b82f640; }

/* ── Issue cards ── */
.issue-card {
    border-radius: 10px; padding: 12px 15px; margin-bottom: 8px;
    font-size: 12px; border-left: 3px solid; line-height: 1.55;
}
.issue-card.high { background: #180404; border-color: #ef4444; }
.issue-card.low  { background: #1a1100; border-color: #f59e0b; }
.issue-card.ok   { background: #041f13; border-color: #10b981; }
.issue-title { font-weight: 500; color: #dde1e7; margin-bottom: 3px; }
.issue-fix   { color: #4b5568; margin-top: 4px; }

/* ── Download buttons ── */
.stDownloadButton > button {
    background: #10b981 !important; color: #022c22 !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: 14px !important;
    height: 48px !important; width: 100% !important;
}
.stDownloadButton > button:hover { background: #059669 !important; }

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: #13161f !important; border: 1px solid #1e2230 !important;
    border-radius: 10px !important; font-size: 13px !important;
    color: #64748b !important; font-weight: 500 !important; padding: 12px 16px !important;
}
.streamlit-expanderContent {
    background: #0b0d12 !important; border: 1px solid #1e2230 !important;
    border-top: none !important; border-radius: 0 0 10px 10px !important;
    padding: 16px !important;
}

/* ── Section headers ── */
.section-head {
    font-size: 10px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
    color: #2d3343; font-family: 'JetBrains Mono', monospace;
    margin: 22px 0 10px; padding-top: 22px; border-top: 1px solid #181b25;
}

/* ── Assumptions ── */
.assumption {
    background: #13161f; border-left: 3px solid #f59e0b;
    padding: 9px 13px; margin-bottom: 7px; border-radius: 0 6px 6px 0;
    font-size: 12px; color: #8892a4; line-height: 1.55;
}

/* ── Prompt box ── */
.prompt-box {
    background: #080a0e; border: 1px solid #1e2230; border-radius: 8px;
    padding: 16px 18px; font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px; color: #8892a4; white-space: pre-wrap; line-height: 1.7;
}

/* ── App title ── */
.app-title {
    font-size: 22px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
    color: #f1f5f9; letter-spacing: -.02em; margin-bottom: 2px;
}
.app-meta {
    font-size: 11px; color: #2d3343; font-family: 'JetBrains Mono', monospace;
    margin-bottom: 28px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def compute_metrics(variants: list) -> list:
    """
    Enrich each variant with:
      rpi      — Revenue Per Impression (primary normalisation metric)
      ctr_ok   — tracking health flag
      brand    — low | medium | high (inferred from free-text notes)
      rpi_pct  — relative RPI for progress bars
      is_winner— highest revenue variant
    """
    results = []
    for v in variants:
        rpi = v["revenue"] / v["impressions"]
        ctr_ok = v.get("ctr") is not None
        notes = (v.get("notes") or "").lower()
        if any(w in notes for w in ["scary", "aggressive", "negative", "fear", "alarming", "bad"]):
            brand = "medium"
        elif any(w in notes for w in ["complaint", "churn", "unsubscribe", "angry", "toxic"]):
            brand = "high"
        else:
            brand = "low"
        results.append({**v, "rpi": rpi, "ctr_ok": ctr_ok, "brand": brand})

    max_rev = max(r["revenue"] for r in results)
    max_rpi = max(r["rpi"] for r in results)
    for r in results:
        r["is_winner"] = r["revenue"] == max_rev
        r["rpi_pct"] = r["rpi"] / max_rpi
    return results


def detect_issues(results: list) -> list:
    """Structured data-quality audit with severity, field, message and fix."""
    issues = []
    for r in results:
        if not r["ctr_ok"]:
            issues.append({
                "sev": "high", "variant": r["name"], "field": "CTR",
                "msg": f"Variant {r['name']} CTR is missing — top-of-funnel visibility is blind.",
                "fix": "Check pixel / event firing on the desktop upsell modal for this variant."
            })
        if r["impressions"] < 100_000:
            issues.append({
                "sev": "low", "variant": r["name"], "field": "Sample size",
                "msg": f"Variant {r['name']} has only {r['impressions']:,} impressions — statistical power may be insufficient.",
                "fix": "Ensure equal traffic split or account for imbalance before declaring significance."
            })
    return issues


def project_monthly(results: list, duration_days: int) -> dict:
    """Project monthly revenue per variant if rolled out to 100% of total traffic."""
    total_imp = sum(r["impressions"] for r in results)
    return {r["name"]: r["rpi"] * (total_imp / duration_days) * 30 for r in results}


def score_variant(r: dict) -> float:
    """
    Composite score 0–100.
    Formula: RPI_relative × (1 − brand_risk_penalty)
    Penalties: low=0%, medium=15%, high=40%
    """
    penalty = {"low": 0.0, "medium": 0.15, "high": 0.40}[r["brand"]]
    return round(r["rpi_pct"] * (1 - penalty) * 100, 1)


def decide_verdict(winner: dict) -> tuple:
    """Return (css_class, icon, label, body) for the verdict banner."""
    if winner["brand"] == "high":
        return ("kill", "KILL", "KILL — Do not scale",
                f"Variant <b>{winner['name']}</b> has the highest revenue but critical brand risk. "
                "Scaling now risks long-term trust erosion. Revert to baseline and redesign the copy.")
    if winner["brand"] == "medium":
        return ("iterate", "ITERATE", "ITERATE — Improve before scaling",
                f"Variant <b>{winner['name']}</b> wins financially but carries a medium brand risk. "
                f"Launch a softened copy test (<b>Variant {winner['name']}.2</b>) before committing to full rollout.")
    return ("scale", "SCALE", "SCALE — Ready to roll out",
            f"Variant <b>{winner['name']}</b> wins on every metric with no brand-risk signals. "
            "Proceed with a phased rollout: 20% → 50% → 100% over 9 days.")


def build_txt(winner, results, meta, issues, projs, lift, gap_annual, ts) -> str:
    lines = [
        "GROWTH EXPERIMENT INTELLIGENCE ENGINE — MANAGEMENT REPORT",
        "=" * 58,
        f"Generated : {ts}",
        f"Experiment: {meta.get('experiment','—')}",
        f"Market    : {meta.get('market','—')}",
        f"Duration  : {meta.get('duration_days','?')} days",
        "",
        "EXECUTIVE SUMMARY",
        "-" * 30,
        f"Winner        : Variant {winner['name']}",
        f"Copy          : \"{winner['copy']}\"",
        f"RPI           : ${winner['rpi']:.4f}",
        f"Conversion    : {winner['conversion']}%",
        f"Revenue       : ${winner['revenue']:,}",
        f"Revenue lift  : +{lift:.1f}% vs Variant A",
        f"Brand risk    : {winner['brand'].capitalize()}",
        f"Annual $ gap  : ${gap_annual:,.0f} (best vs worst variant)",
        "",
        "VARIANT BREAKDOWN", "-" * 30,
    ]
    for r in results:
        lines.append(
            f"Variant {r['name']}: impressions={r['impressions']:,} | "
            f"CTR={'MISSING' if not r['ctr_ok'] else str(r['ctr'])+'%'} | "
            f"conv={r['conversion']}% | rev=${r['revenue']:,} | "
            f"RPI=${r['rpi']:.4f} | brand={r['brand']} | score={score_variant(r)}"
        )
    lines += ["", "DATA QUALITY ISSUES", "-" * 30]
    for i in issues:
        lines += [f"[{i['sev'].upper()}] Variant {i['variant']} — {i['field']}: {i['msg']}",
                  f"  Fix: {i['fix']}"]
    if not issues:
        lines.append("No issues detected.")
    lines += ["", "MONTHLY REVENUE PROJECTIONS (full traffic)", "-" * 30]
    for name, rev in projs.items():
        lines.append(f"Variant {name}: ${rev:,.0f}/month")
    lines += [
        "", "ACTION PLAN", "-" * 30,
        "01. Fix CTR tracking — repair instrumentation before next iteration.",
        f"02. Launch Variant {winner['name']}.2 — softer urgency copy to reduce brand risk.",
        f"03. Geo validation — test winner in a Tier-2 market outside {meta.get('market','USA')}.",
    ]
    return "\n".join(lines)


def build_csv(results) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Variant", "Copy", "Impressions", "CTR", "Conversion %",
                "Revenue $", "RPI", "Brand Risk", "Composite Score"])
    for r in results:
        w.writerow([r["name"], r["copy"], r["impressions"],
                    r["ctr"] if r["ctr_ok"] else "MISSING",
                    r["conversion"], r["revenue"],
                    f"{r['rpi']:.4f}", r["brand"].capitalize(), score_variant(r)])
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — USER FRIENDLY INPUT
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### Experiment Configuration")
    
    exp_name = st.text_input("Experiment Name", "Upsell message test — desktop")
    col_m, col_d = st.columns(2)
    with col_m:
        market = st.text_input("Market", "USA")
    with col_d:
        duration_days = st.number_input("Duration (days)", min_value=1, value=10)

    st.markdown("---")
    st.markdown("### Variant Data")
    st.markdown(
        "<div style='font-size:11px;color:#8892a4;line-height:1.5;margin-bottom:12px;'>"
        "Edit this table directly. Leave CTR as 0.0 if tracking failed. You can add or remove rows at the bottom."
        "</div>",
        unsafe_allow_html=True
    )

    default_variants = pd.DataFrame([
        {"name": "A", "copy": "Upgrade now for full protection", "impressions": 120000, "ctr": 2.3, "conversion": 0.9, "revenue": 4200, "notes": ""},
        {"name": "B", "copy": "Stay safe online – unlock premium features", "impressions": 98000, "ctr": 3.1, "conversion": 0.7, "revenue": 3800, "notes": ""},
        {"name": "C", "copy": "Your device may be at risk – fix it now", "impressions": 110000, "ctr": 0.0, "conversion": 1.2, "revenue": 5100, "notes": "negative feedback: too scary"}
    ])

    edited_df = st.data_editor(
        default_variants,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PARSE & COMPUTE
# ══════════════════════════════════════════════════════════════════════════════

variants_list = edited_df.to_dict('records')

for v in variants_list:
    if v["ctr"] == 0 or pd.isna(v["ctr"]):
        v["ctr"] = None

raw_data = {
    "experiment": exp_name,
    "market": market,
    "duration_days": duration_days,
    "variants": variants_list
}

computed    = compute_metrics(raw_data["variants"])
all_issues  = detect_issues(computed)
winner_v    = next(r for r in computed if r["is_winner"])
baseline    = computed[0]
lift        = (winner_v["revenue"] - baseline["revenue"]) / baseline["revenue"] * 100
projs       = project_monthly(computed, int(raw_data.get("duration_days", 10)))
gap_annual  = (max(projs.values()) - min(projs.values())) * 12
vclass, vicon, vlabel, vbody = decide_verdict(winner_v)
ts          = datetime.now().strftime("%Y-%m-%d %H:%M")


# ══════════════════════════════════════════════════════════════════════════════
# TIER 1 — 5 HERO METRICS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(
    f'<div class="app-title">Growth Experiment Intelligence Engine</div>'
    f'<div class="app-meta">'
    f'experiment: {raw_data.get("experiment","—")} &nbsp;·&nbsp; '
    f'market: {raw_data.get("market","—")} &nbsp;·&nbsp; '
    f'{raw_data.get("duration_days","?")} days &nbsp;·&nbsp; {ts}'
    f'</div>',
    unsafe_allow_html=True,
)

health_css = "red" if any(i["sev"] == "high" for i in all_issues) else "green"
health_val = "WARNING" if health_css == "red" else "CLEAN"
risk_css   = {"low": "green", "medium": "amber", "high": "red"}[winner_v["brand"]]

c1, c2, c3, c4, c5 = st.columns(5)
_cards = [
    (c1, "Financial winner",        f"Variant {winner_v['name']}",   f"{winner_v['conversion']}% conv · ${winner_v['revenue']:,}", "green"),
    (c2, "Revenue per impression",  f"${winner_v['rpi']:.4f}",       "primary normalised metric",  "green"),
    (c3, "Revenue lift vs A",       f"+{lift:.1f}%",                  "winner over baseline",        "blue"),
    (c4, "Data health",             health_val,                       "tracking status",             health_css),
    (c5, "Brand risk",              winner_v["brand"].capitalize(),   "qualitative signal",          risk_css),
]
for col, label, value, sub, css in _cards:
    col.markdown(
        f'<div class="hero-card {css}">'
        f'<div class="hero-label">{label}</div>'
        f'<div class="hero-value {css}">{value}</div>'
        f'<div class="hero-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TIER 2A — VERDICT
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-head'>AI Verdict — what should we do?</div>", unsafe_allow_html=True)
st.markdown(
    f'<div class="verdict-banner {vclass}">'
    f'<div class="verdict-icon">{vicon}</div>'
    f'<div><div class="verdict-title {vclass}">{vlabel}</div>'
    f'<div class="verdict-body">{vbody}</div></div>'
    f'</div>',
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# TIER 2B — AI INSIGHT
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-head'>AI Insight — what the data is really saying</div>", unsafe_allow_html=True)

risk_note = {
    "medium": f'<b style="color:#f59e0b">Brand alert:</b> Qualitative feedback signals the copy may feel too alarming. Recommend softening the tone before global rollout.',
    "high":   f'<b style="color:#ef4444">Critical brand risk:</b> Team notes indicate high-toxicity signals. Stop scaling immediately.',
    "low":    "No negative signals detected in team feedback. The winning copy is safe to scale with standard monitoring.",
}[winner_v["brand"]]

st.markdown(
    f'<div class="insight-card">'
    f'<b>Variant {winner_v["name"]}</b> generates <b>${winner_v["revenue"]:,}</b> at an RPI of '
    f'<b>${winner_v["rpi"]:.4f}</b> — a <b>+{lift:.1f}%</b> revenue lift over the baseline. '
    f'Projected to 12 months, the gap between best and worst variant equals '
    f'<b style="color:#10b981">${gap_annual:,.0f} in incremental annual revenue</b> — '
    f'with zero additional acquisition spend.<br><br>{risk_note}'
    f'</div>',
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# TIER 2C — ACTION PLAN
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-head'>Action plan — next 3 steps</div>", unsafe_allow_html=True)

steps = []
if any(i["sev"] == "high" for i in all_issues):
    steps.append((
        "Fix CTR tracking immediately",
        "Repair the desktop tracking event before the next iteration. Without CTR data there is no top-of-funnel visibility.",
    ))
if winner_v["brand"] == "medium":
    steps.append((
        f"Launch Variant {winner_v['name']}.2 — soften the copy",
        f"Maintain the urgency angle but reduce the alarmist language. "
        f"E.g. \"Give your device the protection it deserves.\"",
    ))
elif winner_v["brand"] == "low":
    steps.append((
        f"Phased rollout of Variant {winner_v['name']}",
        "20% → 50% → 100% traffic in 3-day windows. Monitor CTR, conversion, and support ticket volume.",
    ))
else:
    steps.append((
        "Pause the winner and redesign copy",
        "Brand risk outweighs the revenue gain. Revert to baseline while the team develops a new angle.",
    ))
steps.append((
    "Geo validation",
    f"Run the test in a Tier-2 market outside {raw_data.get('market','USA')}. "
    "Urgency-based messaging performs differently across cultures — validate before global rollout.",
))

html = '<div class="insight-card" style="padding:16px 20px">'
for i, (title, desc) in enumerate(steps, 1):
    html += (
        f'<div class="action-step">'
        f'<div class="action-num">{i:02d}</div>'
        f'<div><div class="action-title">{title}</div>'
        f'<div class="action-desc">{desc}</div></div>'
        f'</div>'
    )
html += "</div>"
st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TIER 2D — EXPORT BUTTONS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-head'>Export for management</div>", unsafe_allow_html=True)
dl1, dl2, _ = st.columns([2, 2, 3])
with dl1:
    st.download_button(
        "Download Management Report (.txt)",
        build_txt(winner_v, computed, raw_data, all_issues, projs, lift, gap_annual, ts),
        file_name=f"experiment_report_{ts[:10]}.txt",
        mime="text/plain",
        use_container_width=True,
    )
with dl2:
    st.download_button(
        "Download Raw Data (.csv)",
        build_csv(computed),
        file_name=f"experiment_data_{ts[:10]}.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TIER 3 — PROGRESSIVE DISCLOSURE
# ══════════════════════════════════════════════════════════════════════════════

with st.expander("Full variant breakdown — raw data table"):
    for d in computed:
        wcls  = "winner" if d["is_winner"] else ""
        rp    = {"low": "slate", "medium": "amber", "high": "red"}[d["brand"]]
        rl    = {"low": "Low risk", "medium": "Medium risk", "high": "High risk"}[d["brand"]]
        bar_c = "#10b981" if d["is_winner"] else "#1e2230"
        wpill = ' <span class="pill green" style="margin-left:6px">WINNER</span>' if d["is_winner"] else ""
        ctr_html = (
            f'<div class="stat-value">{d["ctr"]}%</div>' if d["ctr_ok"]
            else '<div class="stat-value miss">MISSING</div>'
        )
        st.markdown(f"""
        <div class="variant-row {wcls}">
          <div style="min-width:150px">
            <div style="font-size:14px;font-weight:500;color:#dde1e7">Variant {d['name']}{wpill}</div>
            <div style="font-size:11px;color:#2d3343;font-style:italic;margin-top:3px">
              "{d['copy'][:52]}{'…' if len(d['copy'])>52 else ''}"
            </div>
          </div>
          <div style="flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:8px;padding:0 20px">
            <div><div class="stat-label">Impressions</div><div class="stat-value">{d['impressions']:,}</div></div>
            <div><div class="stat-label">CTR</div>{ctr_html}</div>
            <div><div class="stat-label">Conversion</div><div class="stat-value">{d['conversion']}%</div></div>
            <div><div class="stat-label">Revenue</div><div class="stat-value">${d['revenue']:,}</div></div>
            <div>
              <div class="stat-label">RPI</div>
              <div class="stat-value">${d['rpi']:.4f}</div>
              <div class="rpi-bar">
                <div style="height:3px;width:{int(d['rpi_pct']*100)}%;background:{bar_c}"></div>
              </div>
            </div>
          </div>
          <div style="min-width:110px;text-align:right;padding-right:4px">
            <span class="pill {rp}">{rl}</span>
            <div style="font-size:11px;color:#2d3343;margin-top:6px">Score: {score_variant(d)}</div>
          </div>
        </div>""", unsafe_allow_html=True)


with st.expander("Data quality audit"):
    if not all_issues:
        st.markdown(
            '<div class="issue-card ok">'
            '<div class="issue-title" style="color:#10b981">All clear</div>'
            '<div class="issue-fix">No tracking failures or data inconsistencies detected.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    for iss in all_issues:
        rc = "red" if iss["sev"] == "high" else "amber"
        st.markdown(f"""
        <div class="issue-card {iss['sev']}">
          <div style="display:flex;gap:8px;align-items:center;margin-bottom:5px">
            <span class="pill {rc}">{iss['sev'].upper()}</span>
            <span class="issue-title">Variant {iss['variant']} — {iss['field']}</span>
          </div>
          <div style="font-size:12px;color:#8892a4">{iss['msg']}</div>
          <div class="issue-fix">Suggested fix: {iss['fix']}</div>
        </div>""", unsafe_allow_html=True)


with st.expander("Monthly revenue projection — full traffic rollout"):
    pc = st.columns(len(computed))
    for col, d in zip(pc, computed):
        css = "green" if d["is_winner"] else "slate"
        col.markdown(
            f'<div class="hero-card {css}" style="text-align:center">'
            f'<div class="hero-label">Variant {d["name"]}</div>'
            f'<div class="hero-value {css}" style="font-size:24px">${projs[d["name"]]:,.0f}</div>'
            f'<div class="hero-sub">projected / month</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f'<div class="insight-card" style="margin-top:12px">'
        f'Rolling out Variant <b>{winner_v["name"]}</b> to 100% of traffic is worth '
        f'<b style="color:#10b981">${gap_annual:,.0f} in incremental annual revenue</b> '
        f'vs the worst-performing variant — zero increase in acquisition budget.</div>',
        unsafe_allow_html=True,
    )


with st.expander("Key assumptions & limitations"):
    for a in [
        "RPI is used as the primary normalisation metric because impression volumes are unequal across variants.",
        "Missing CTR for Variant C is treated as a technical tracking failure, not a data anomaly masking a real engagement drop.",
        "The experiment ran ~10 days in USA on desktop only. Seasonal, geographic, and device-type effects limit generalisability.",
        "Qualitative feedback ('too scary') is a medium brand-risk signal — sample volume is too small for statistical significance.",
        "Monthly projections assume constant RPI at scale. In practice, RPI may degrade due to audience saturation.",
    ]:
        st.markdown(f'<div class="assumption">{a}</div>', unsafe_allow_html=True)


with st.expander("Reusable AI prompt — paste into Claude, GPT-4, or Gemini"):
    st.markdown(
        "<div style='font-size:11px;color:#3d4657;line-height:1.6;margin-bottom:10px;'>"
        "Copy this prompt and paste your experiment data at the bottom. "
        "Works with any LLM. Produces the same structured output every time.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
<div class="prompt-box">
# SYSTEM PROMPT — Growth Experiment Analyser

You are a Senior AI Operations Analyst for a Growth team.
Analyse the experiment data below and return a management-ready report.

## ANALYSIS RULES
1. Calculate RPI = Revenue / Impressions for each variant.
2. If CTR is missing, flag as DATA WARNING. Do NOT discard the variant.
3. Score qualitative notes as brand risk: LOW / MEDIUM / HIGH.
4. Compute a composite score: RPI efficiency (70%) minus brand risk penalty (30%).
5. Issue a verdict: SCALE / ITERATE / KILL.
6. Project monthly revenue at full traffic rollout.

## OUTPUT FORMAT
- Winner           : [variant name + copy]
- Top RPI          : [value]
- Revenue lift     : [% vs Variant A]
- Composite score  : [0–100]
- Monthly revenue  : [winner projected $/month]
- Data health      : [OK | WARNING + reason]
- Brand risk       : [Low | Medium | High + reason]
- Verdict          : [SCALE | ITERATE | KILL]
- Action 1         : [highest priority]
- Action 2         : [second priority]
- Action 3         : [third priority]

## EXPERIMENT DATA
[Paste your variant table here]
</div>
""", unsafe_allow_html=True)