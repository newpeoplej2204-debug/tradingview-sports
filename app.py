
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="TradingView Sports AI",
    layout="wide"
)

st.title("📈 TradingView Style Sports AI")

# =====================================================
# LEAGUES
# =====================================================

league = st.sidebar.selectbox(
    "League",
    [
        "EPL",
        "K League 1",
        "K League 2",
        "J1 League",
        "J2 League",
        "KBO",
        "NPB",
        "MLB"
    ]
)

teams = {
    "EPL": ["Arsenal","Liverpool","Chelsea","Man City"],
    "K League 1": ["Ulsan","Jeonbuk","Pohang","Seoul"],
    "K League 2": ["Busan","Anyang","Suwon","Seongnam"],
    "J1 League": ["Kawasaki","Kobe","Urawa","Yokohama"],
    "J2 League": ["Jubilo","Shimizu","Tokyo Verdy","Vegalta"],
    "KBO": ["LG Twins","Doosan Bears","KIA Tigers","Lotte Giants"],
    "NPB": ["Yomiuri Giants","Hanshin Tigers","SoftBank Hawks","Yakult"],
    "MLB": ["Dodgers","Yankees","Astros","Braves"]
}

home_team = st.sidebar.selectbox(
    "🏠 Home Team",
    teams[league]
)

away_team = st.sidebar.selectbox(
    "✈️ Away Team",
    teams[league],
    index=1
)

# =====================================================
# GENERATE MATCH DATA
# =====================================================

np.random.seed(len(home_team) + len(away_team))

matches = 40

dates = pd.date_range(
    end=pd.Timestamp.today(),
    periods=matches
)

def create_team_data(team_name):

    rows = []

    current = 50

    for i in range(matches):

        gf = np.random.randint(0, 5)
        ga = np.random.randint(0, 5)

        if gf > ga:
            result = "WIN"
            color = "red"

        elif gf == ga:
            result = "DRAW"
            color = "green"

        else:
            result = "LOSS"
            color = "blue"

        open_price = current

        movement = (gf * 2) - ga

        close_price = open_price + movement

        high = max(open_price, close_price) + np.random.randint(0, 3)
        low = min(open_price, close_price) - np.random.randint(0, 3)

        current = close_price

        rows.append({
            "Date": dates[i],
            "Open": open_price,
            "Close": close_price,
            "High": high,
            "Low": low,
            "GF": gf,
            "GA": ga,
            "Result": result,
            "Color": color
        })

    return pd.DataFrame(rows)

home_df = create_team_data(home_team)
away_df = create_team_data(away_team)

# =====================================================
# AI PREDICTION
# =====================================================

home_strength = home_df["Close"].iloc[-1]
away_strength = away_df["Close"].iloc[-1]

total = abs(home_strength) + abs(away_strength)

home_pct = round(
    (abs(home_strength) / total) * 100,
    1
)

away_pct = round(
    (abs(away_strength) / total) * 100,
    1
)

draw_pct = round(
    np.random.randint(5, 20),
    1
)

st.subheader("🤖 AI Match Prediction")

c1, c2, c3 = st.columns(3)

c1.metric(
    f"{home_team} Win %",
    f"{home_pct}%"
)

c2.metric(
    "Draw %",
    f"{draw_pct}%"
)

c3.metric(
    f"{away_team} Win %",
    f"{away_pct}%"
)

# =====================================================
# TRADINGVIEW STYLE CHART
# =====================================================

st.subheader("📊 Sports Candlestick Momentum")

fig, ax = plt.subplots(
    figsize=(16, 8)
)

def draw_candles(df, offset):

    for idx, row in df.iterrows():

        x = idx + offset

        # wick
        ax.plot(
            [x, x],
            [row["Low"], row["High"]],
            linewidth=1.5
        )

        # candle body
        lower = min(row["Open"], row["Close"])
        height = abs(row["Close"] - row["Open"])

        ax.add_patch(
            plt.Rectangle(
                (x - 0.3, lower),
                0.6,
                max(height, 0.5)
            )
        )

        ax.patches[-1].set_color(row["Color"])

draw_candles(home_df, 0)
draw_candles(away_df, matches + 5)

ax.set_title(
    f"{home_team} vs {away_team} Trading Momentum"
)

ax.set_xlabel("Matches")
ax.set_ylabel("Performance Price")

st.pyplot(fig)

# =====================================================
# MATCH LOG
# =====================================================

st.subheader("📋 Recent Match Candle Data")

recent = pd.concat([
    home_df.tail(5).assign(Team=home_team),
    away_df.tail(5).assign(Team=away_team)
])

st.dataframe(
    recent[
        [
            "Team",
            "GF",
            "GA",
            "Result",
            "Open",
            "Close",
            "High",
            "Low"
        ]
    ]
)

# =====================================================
# SIGNAL ENGINE
# =====================================================

st.subheader("🚨 Signal Engine")

def signal(close_price):

    if close_price > 65:
        return "🔥 Strong Bull"

    elif close_price < 35:
        return "❄️ Capitulation"

    return "📈 Neutral"

signal_df = pd.DataFrame([
    {
        "Team": home_team,
        "Signal": signal(home_df["Close"].iloc[-1])
    },
    {
        "Team": away_team,
        "Signal": signal(away_df["Close"].iloc[-1])
    }
])

st.dataframe(signal_df)

st.markdown("---")
st.markdown("📈 TradingView Style Sports AI Dashboard")
