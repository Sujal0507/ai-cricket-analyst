import os
import pandas as pd
import gradio as gr
import plotly.express as px
from groq import Groq

# =====================================================
# LOAD DATA
# =====================================================
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

deliveries = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id",
    how="left"
)

players = sorted(deliveries["batter"].dropna().unique())

# =====================================================
# GROQ CLIENT (SECURE – ENV / HF SECRETS)
# =====================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Add it to environment variables or HF Secrets.")

client = Groq(api_key=GROQ_API_KEY)

# =====================================================
# ANALYTICS
# =====================================================
def top_run_scorers():
    return (
        deliveries.groupby("batter")["batsman_runs"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

def top_wicket_takers():
    return (
        deliveries[deliveries["is_wicket"] == 1]
        .groupby("bowler")
        .size()
        .nlargest(10)
        .reset_index(name="wickets")
    )

def player_stats(player):
    df = deliveries[deliveries["batter"] == player]
    runs = int(df["batsman_runs"].sum())
    balls = df.shape[0]
    sr = round((runs / balls) * 100, 2) if balls else 0
    matches_played = df["match_id"].nunique()
    best_season = df.groupby("season")["batsman_runs"].sum().idxmax()
    return runs, sr, matches_played, best_season

def player_trend(player):
    return (
        deliveries[deliveries["batter"] == player]
        .groupby("season")["batsman_runs"]
        .sum()
        .reset_index()
    )

# =====================================================
# LLM (IPL-ONLY, DATA-GROUNDED)
# =====================================================
def llm_answer(facts, question):
    prompt = f"""
You are an IPL (Indian Premier League) cricket analyst.

RULES:
- Talk ONLY about IPL.
- Use ONLY the facts provided.
- Do NOT mention datasets, calculations, or models.
- 2–3 crisp professional sentences.
- Sound like Cricinfo / IPL broadcast analysis.

FACTS:
{facts}

QUESTION:
{question}

FINAL IPL ANALYSIS:
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=180,
    )
    return response.choices[0].message.content.strip()

# =====================================================
# ASK AI
# =====================================================
def ask_ai(question):
    q = question.lower()

    if any(k in q for k in ["run", "runs", "run scorer"]):
        df = top_run_scorers()
        leader = df.iloc[0]
        facts = f"In the IPL, {leader['batter']} is the highest run scorer with {int(leader['batsman_runs'])} runs."
        ans = llm_answer(facts, question)

        fig = px.bar(
            df, x="batter", y="batsman_runs",
            height=650,
            color_discrete_sequence=["#4988C4"]
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        return ans, fig, ""

    if any(k in q for k in ["wicket", "wickets", "wicket taker"]):
        df = top_wicket_takers()
        leader = df.iloc[0]
        facts = f"In the IPL, {leader['bowler']} is the leading wicket taker with {int(leader['wickets'])} wickets."
        ans = llm_answer(facts, question)

        fig = px.bar(
            df, x="bowler", y="wickets",
            height=650,
            color_discrete_sequence=["#1C4D8D"]
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        return ans, fig, ""

    return llm_answer(
        "This question relates to IPL cricket but no numerical fact was matched.",
        question
    ), None, ""

# =====================================================
# COMPARE PLAYERS
# =====================================================
def compare_players(p1, p2):
    r1, sr1, m1, _ = player_stats(p1)
    r2, sr2, m2, _ = player_stats(p2)

    facts = f"""
In the IPL:
{p1}: {r1} runs, strike rate {sr1}, {m1} matches
{p2}: {r2} runs, strike rate {sr2}, {m2} matches
"""
    ans = llm_answer(facts, f"Compare {p1} vs {p2}")

    fig = px.bar(
        pd.DataFrame({"Player": [p1, p2], "Runs": [r1, r2]}),
        x="Player", y="Runs",
        height=550,
        color_discrete_sequence=["#0F2854"]
    )
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return ans, fig

# =====================================================
# 🎨 MODERN UI CSS
# =====================================================
custom_css = """
body {
    background: linear-gradient(135deg, #0F2854, #020617);
    font-family: 'Inter', system-ui, sans-serif;
}
.gradio-container {
    max-width: 1700px !important;
    padding: 36px !important;
}
h1, h2 {
    text-align: center !important;
    color: #BDE8F5;
    font-weight: 800;
    font-size: 40px !important;
}
"""

# =====================================================
# UI
# =====================================================
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("## 🏏 AI Cricket Analyst Dashboard")

    with gr.Tabs():
        with gr.Tab("🤖 Ask AI"):
            q = gr.Textbox(placeholder="Who is the top run scorer in IPL?")
            btn = gr.Button("Ask AI")
            ans = gr.Textbox(lines=7, label="AI Insight")
            chart = gr.Plot()
            btn.click(ask_ai, q, [ans, chart, q])

        with gr.Tab("Player Insights"):
            dd = gr.Dropdown(players, label="Select Player", filterable=True)
            card = gr.Markdown()
            trend = gr.Plot()

            def update_player(p):
                r, sr, m, best = player_stats(p)
                card_md = f"""
### {p}
**Runs:** {r}  
**Strike Rate:** {sr}  
**Matches:** {m}  
**Best Season:** {best}
"""
                fig = px.line(
                    player_trend(p),
                    x="season", y="batsman_runs",
                    markers=True,
                    height=550,
                    color_discrete_sequence=["#4988C4"]
                )
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
                return card_md, fig

            dd.change(update_player, dd, [card, trend])

        with gr.Tab("⚔️ Compare Players"):
            p1 = gr.Dropdown(players, label="Player A", filterable=True)
            p2 = gr.Dropdown(players, label="Player B", filterable=True)
            btn2 = gr.Button("Compare")
            ans2 = gr.Textbox(lines=8)
            chart2 = gr.Plot()
            btn2.click(compare_players, [p1, p2], [ans2, chart2])

demo.launch(ssr_mode=False)
