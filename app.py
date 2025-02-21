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
    query='SELECT date, duree_totale FROM diary.raw_data where date > (NOW() - INTERVAL 2 MONTH)'
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600 
    conn.close()
    return df

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("")

fig = px.line(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='Travail par jour')

# Afficher le graphique dans Streamlit
st.plotly_chart(fig)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
