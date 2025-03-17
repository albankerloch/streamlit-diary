import os.path
import altair as alt
import pandas as pd
import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()
password=os.getenv('DATABASE_PASSWORD')

HERE = os.path.dirname(os.path.abspath(__file__))

st.title("Mes Heures")

DATA = os.path.join(HERE, "data.csv")

@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host='diary-database.c1igk0esk62c.eu-west-3.rds.amazonaws.com',
        user='alban',
        password=password,
        database='diary'
    )
    query='SELECT distinct date, duree_totale FROM diary.raw_data where date > (NOW() - INTERVAL 2)'
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600 
    conn.close()
    return df

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("")

chart = (
    alt.Chart(data).mark_area(
    color="lightblue",
    interpolate='step-after',
    line=True
).encode(
    x='date',
    y='duree_heure'
)
)

st.altair_chart(chart, use_container_width=True)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)