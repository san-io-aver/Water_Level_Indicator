import streamlit as st
import requests
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

AIO_USERNAME = st.secrets["AIO_USERNAME"]
AIO_KEY = st.secrets["AIO_KEY"]

# Auto-refresh every 15 seconds
st_autorefresh(interval=20000, key="my_autorefresh_key")

st.title("Water Tank Level Dashboard")

feeds = [
    {"name": "Water Tank 1", "feed": "tank1-level"}
]

cols_per_row = 3


for i in range(0, len(feeds), cols_per_row):
    cols = st.columns(min(cols_per_row, len(feeds) - i))
    for j, feed in enumerate(feeds[i:i+cols_per_row]):
        if not feed.get("feed"):
            continue
        url = f"https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{feed['feed']}"
        headers = {"X-AIO-Key": AIO_KEY}
        
        r = requests.get(url, headers=headers)
        if r.status_code == 200 and r.json():
            data = r.json()
            value = float(data["last_value"])
            
            # Dynamic inner bar color (blue for high range)
            bar_color = "blue"
            
            # Create gauge chart
            fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={'suffix': '%', 'font': {'size': 36}},
            title={'text': feed["name"], 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': bar_color, 'thickness': 0.6},  # chunky inner bar
                'borderwidth': 1,  # thin outer boundary
                'steps': [
                    {'range': [0, 30], 'color': "red", 'thickness': 0.1},
                    {'range': [30, 70], 'color': "yellow", 'thickness': 0.1},
                    {'range': [70, 100], 'color': "green", 'thickness': 0.1}
                ],
            }
        ))

            
            fig.update_layout(
                height=200, 
                margin={"t": 20, "b": 10, "l": 10, "r": 10},
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            cols[j].plotly_chart(fig, use_container_width=True)
        else:
            cols[j].warning(f"Could not fetch data for {feed['name']}")
