import os.path
import pandas as pd
import streamlit as st
import mysql.connector
import os
import calmap as calmap
from dotenv import load_dotenv
import plotly.express as px
import numpy as np; np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import matplotlib.pyplot as plt
import july
from datetime import datetime


load_dotenv()
password=os.getenv('DATABASE_PASSWORD')

st.title("Mes Heures")

@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host='diary-database.c1igk0esk62c.eu-west-3.rds.amazonaws.com',
        user='alban',
        password=password,
        database='diary'
    )
    query="SELECT DISTINCT date, duree_totale, brossette FROM diary.raw_data where date >= DATE_FORMAT(NOW(), '%Y-%m-01')"
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    conn.close()
    return df

with st.spinner('Chargement des données...'):
    data = load_data()

fig = px.line(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='Travail par jour')
st.plotly_chart(fig)

fig_brossette, ax = plt.subplots()
july.month_plot(data['date'], data['brossette'], cmap="github", weeknum_label=False, fontfamily="monospace", date_label=True, ax=ax)
st.pyplot(fig_brossette)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)