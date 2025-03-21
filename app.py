import os.path
import altair as alt
import pandas as pd
import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import plotly.express as px
import numpy as np; np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import calmap
import matplotlib.pyplot as plt
import requests
import time

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
    query='SELECT DISTINCT date, duree_totale, brossette FROM diary.raw_data where date > (NOW() - INTERVAL 2 MONTH)'
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600 
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

st.title("Mes Heures")

if st.button("Mise à jour"):
    call_lambda_function()
    load_data.clear()
    st.rerun()

data_load_state = st.text("Chargement des données ...")
data = load_data()
data_load_state.text("")

data_brossette = data[['date', 'brossette']]
data_brossette.set_index('date', inplace=True)

fig = px.line(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='Travail par jour')

st.plotly_chart(fig)

fig_brossette, ax = calmap.calendarplot(data_brossette['brossette'], 
    daylabels=['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
    monthlabels=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novvembre', 'Décembre'],
    cmap='YlGn', 
    fig_kws={'figsize': (12, 4)})

st.pyplot(fig_brossette)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)