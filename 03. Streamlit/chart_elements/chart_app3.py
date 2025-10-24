import streamlit as st
import pandas as pd
from datetime import date

df = pd.read_csv("avocado.csv")
df['date'] = df['date'].apply(lambda x: date.fromisoformat(x))

plot_table = {
    "geography": [
        "Boston",
        "California",
        "Los Angeles"
    ]
}

pivot_df = pd.pivot_table(df, index='date', columns='geography', values='average_price')

st.write(pivot_df[plot_table["geography"]])

# line chart를 시각화합니다.
st.bar_chart(pivot_df[plot_table["geography"]])