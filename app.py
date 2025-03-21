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
import requests
import time
from matplotlib.colors import ListedColormap
import july
from datetime import datetime

load_dotenv()
password=os.getenv('DATABASE_PASSWORD')


@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host='diary-database.c1igk0esk62c.eu-west-3.rds.amazonaws.com',
        user='alban',
        password=password,
        database='diary'
    )
    query="SELECT DISTINCT date, duree_totale, brossette, manger FROM diary.raw_data where date >= DATE_FORMAT(NOW(), '%Y-%m-01')"
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    conn.close()
    return df

api_url = "https://rdvdej6yilynmf5byxza4id4ke0vhplq.lambda-url.eu-west-3.on.aws/"

def call_lambda_function():
    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            st.success("Données mises à jour !")
        else:
            st.error(f"Erreur lors de l'appel de la fonction Lambda: {response.status_code}")
    except Exception as e:
        st.error(f"Erreur: {e}")

st.title("Journ-Alban")

if st.button("Mise à jour"):
    call_lambda_function()
    load_data.clear()
    st.rerun()

with st.spinner('Chargement des données...'):
    data = load_data()

fig = px.bar(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='')
fig.update_xaxes(
    dtick="D1",
    tickformat="%d",
    ticklabelmode="instant")
st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
    fig_brossette, ax = plt.subplots()
    july.month_plot(data['date'], data['brossette'], cmap= ListedColormap(["#F5F5F5", "#FFFFE5", "green"]), weeknum_label=False, fontfamily="monospace", date_label=True, ax=ax)
    st.pyplot(fig_brossette)

with col2:
    fig_manger, ax = plt.subplots()
    july.month_plot(data['date'], data['manger'], cmap=ListedColormap(["#F5F5F5", "#FFFFE5", "green"]), weeknum_label=False, fontfamily="monospace", date_label=True, ax=ax)
    st.pyplot(fig_manger)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)