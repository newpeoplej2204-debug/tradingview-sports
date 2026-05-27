
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Result Candle Sports AI",
    layout="wide"
)

st.title("📈 Result Candle Sports Trading Terminal")

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
# RESULT-ONLY CANDLE ENGINE
# =====================================================

def generate_team_data(team_name, periods):

    np.random.seed(len(team_name) + periods)

    dates = pd.date_range(
        end=pd.Timestamp.today(),
        periods=periods
    )

    rows = []

    price = 100

    for i in range(periods):

        gf = np.random.randint(0, 5)
        ga = np.random.randint(0, 5)

        # RESULT COLOR
        if gf > ga:
            result = "WIN"
            color = "red"
            close_price = price + 5

        elif gf == ga:
            result = "DRAW"
            color = "green"
            close_price = price

        else:
            result = "LOSS"
            color = "blue"
            close_price = price - 5

        open_price = price

        high = max(open_price, close_price) + 2
        low = min(open_price, close_price) - 2

        price = close_price

        rows.append({
            "Date": dates[i],
            "Open": open_price,
            "High": high,
            "Low": low,
            "Close": close_price,
            "GF": gf,
            "GA": ga,
            "Result": result,
            "Color": color
        })

    return pd.DataFrame(rows)

home_df = generate_team_data(home_team, home_period)
away_df = generate_team_data(away_team, away_period)

# =====================================================
# AI PREDICTION
# =====================================================

home_score = len(home_df[home_df["Result"] == "WIN"])
away_score = len(away_df[away_df["Result"] == "WIN"])

total = home_score + away_score

if total == 0:
    total = 1

home_pct = round((home_score / total) * 100, 1)
away_pct = round((away_score / total) * 100, 1)
draw_pct = round(np.random.randint(5,15),1)

st.subheader("🤖 AI Match Prediction")

c1,c2,c3 = st.columns(3)

c1.metric(f"{home_team}", f"{home_pct}%")
c2.metric("Draw", f"{draw_pct}%")
c3.metric(f"{away_team}", f"{away_pct}%")

# =====================================================
# CHART FUNCTION
# =====================================================

def create_chart(df, title):

    fig = go.Figure()

    for i in range(len(df)):

        row = df.iloc[i]

        if row["Result"] == "WIN":
            candle_color = "red"

        elif row["Result"] == "DRAW":
            candle_color = "green"

        else:
            candle_color = "blue"

        fig.add_trace(go.Candlestick(
            x=[row["Date"]],
            open=[row["Open"]],
            high=[row["High"]],
            low=[row["Low"]],
            close=[row["Close"]],
            increasing_line_color=candle_color,
            decreasing_line_color=candle_color,
            showlegend=False
        ))

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

left,right = st.columns(2)

with left:

    st.markdown(f"### 🏠 {home_team}")

    st.plotly_chart(
        create_chart(
            home_df,
            f"{home_team} Result Candles"
        ),
        use_container_width=True
    )

with right:

    st.markdown(f"### ✈️ {away_team}")

    st.plotly_chart(
        create_chart(
            away_df,
            f"{away_team} Result Candles"
        ),
        use_container_width=True
    )

# =====================================================
# RECENT DATA
# =====================================================

st.subheader("📋 Recent Match Results")

c1,c2 = st.columns(2)

with c1:

    st.markdown(f"### {home_team}")

    st.dataframe(
        home_df.tail(10)[
            [
                "GF",
                "GA",
                "Result",
                "Open",
                "Close"
            ]
        ]
    )

with c2:

    st.markdown(f"### {away_team}")

    st.dataframe(
        away_df.tail(10)[
            [
                "GF",
                "GA",
                "Result",
                "Open",
                "Close"
            ]
        ]
    )

st.markdown("---")
st.markdown("📈 Result Candle Sports Trading Terminal")
