
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="TradingView Sports Terminal",
    layout="wide"
)

st.title("📈 TradingView Sports Trading Terminal")

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

# =====================================================
# TEAM SELECT
# =====================================================

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
# INDEPENDENT PERIOD SELECT
# =====================================================

home_period = st.sidebar.selectbox(
    "🏠 Home Candles",
    [20,50,75,100],
    index=1
)

away_period = st.sidebar.selectbox(
    "✈️ Away Candles",
    [20,50,75,100],
    index=1
)

# =====================================================
# DATA ENGINE
# =====================================================

def generate_team_data(team_name, periods):

    np.random.seed(len(team_name) + periods)

    dates = pd.date_range(
        end=pd.Timestamp.today(),
        periods=periods
    )

    rows = []

    current = 50

    for i in range(periods):

        gf = np.random.randint(0, 5)
        ga = np.random.randint(0, 5)

        if gf > ga:
            result = "WIN"

        elif gf == ga:
            result = "DRAW"

        else:
            result = "LOSS"

        open_price = current

        move = (gf * 2) - ga

        close_price = open_price + move

        high = max(open_price, close_price) + np.random.randint(0, 3)
        low = min(open_price, close_price) - np.random.randint(0, 3)

        current = close_price

        rows.append({
            "Date": dates[i],
            "Open": open_price,
            "High": high,
            "Low": low,
            "Close": close_price,
            "GF": gf,
            "GA": ga,
            "Result": result
        })

    return pd.DataFrame(rows)

home_df = generate_team_data(home_team, home_period)
away_df = generate_team_data(away_team, away_period)

# =====================================================
# AI PREDICTION
# =====================================================

home_strength = home_df["Close"].iloc[-1]
away_strength = away_df["Close"].iloc[-1]

total = abs(home_strength) + abs(away_strength)

home_pct = round((abs(home_strength) / total) * 100, 1)
away_pct = round((abs(away_strength) / total) * 100, 1)
draw_pct = round(np.random.randint(5, 15), 1)

st.subheader("🤖 AI Match Prediction")

c1, c2, c3 = st.columns(3)

c1.metric(
    f"{home_team}",
    f"{home_pct}%"
)

c2.metric(
    "Draw",
    f"{draw_pct}%"
)

c3.metric(
    f"{away_team}",
    f"{away_pct}%"
)

# =====================================================
# CHART FUNCTION
# =====================================================

def create_chart(df, title):

    colors = []

    for _, row in df.iterrows():

        if row["Result"] == "WIN":
            colors.append("red")

        elif row["Result"] == "DRAW":
            colors.append("green")

        else:
            colors.append("blue")

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        increasing_line_color='red',
        decreasing_line_color='blue'
    ))

    # draw overlay markers
    for idx, row in df.iterrows():

        if row["Result"] == "DRAW":

            fig.add_trace(
                go.Scatter(
                    x=[row["Date"]],
                    y=[row["Close"]],
                    mode="markers",
                    marker=dict(
                        size=10,
                        color="green"
                    ),
                    name="Draw"
                )
            )

    fig.update_layout(
        title=title,
        template="plotly_dark",
        xaxis_rangeslider_visible=True,
        dragmode='pan',
        height=650
    )

    return fig

# =====================================================
# SPLIT SCREEN
# =====================================================

st.subheader("📊 Split TradingView Charts")

left, right = st.columns(2)

with left:

    st.markdown(f"### 🏠 {home_team}")

    home_chart = create_chart(
        home_df,
        f"{home_team} Momentum"
    )

    st.plotly_chart(
        home_chart,
        use_container_width=True
    )

with right:

    st.markdown(f"### ✈️ {away_team}")

    away_chart = create_chart(
        away_df,
        f"{away_team} Momentum"
    )

    st.plotly_chart(
        away_chart,
        use_container_width=True
    )

# =====================================================
# DATA TABLES
# =====================================================

st.subheader("📋 Recent Match Candle Data")

c1, c2 = st.columns(2)

with c1:

    st.markdown(f"### {home_team}")

    st.dataframe(
        home_df.tail(10)
    )

with c2:

    st.markdown(f"### {away_team}")

    st.dataframe(
        away_df.tail(10)
    )

# =====================================================
# SIGNAL ENGINE
# =====================================================

st.subheader("🚨 AI Signal Engine")

def signal(value):

    if value > 70:
        return "🔥 Bullish"

    elif value < 30:
        return "❄️ Capitulation"

    return "📈 Neutral"

signal_df = pd.DataFrame([
    {
        "Team": home_team,
        "Signal": signal(home_strength)
    },
    {
        "Team": away_team,
        "Signal": signal(away_strength)
    }
])

st.dataframe(signal_df)

st.markdown("---")
st.markdown("📈 TradingView Sports Trading Terminal")
