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
from matplotlib.colors import ListedColormap, BoundaryNorm
import july
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

style = "<style>h1 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
style2 = "<style>h3 {text-align: center;}</style>"
st.markdown(style2, unsafe_allow_html=True)

st.title("Journ-Alban")
st.markdown('</div>', unsafe_allow_html=True)

if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="vertical-align">', unsafe_allow_html=True)
    if st.button("", icon=":material/arrow_back:", use_container_width=True):
        st.session_state.start_date = st.session_state.start_date - relativedelta(months=1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f"### {st.session_state.start_date.strftime('%B %Y')}")

with col3:    
    st.markdown('<div class="vertical-align">', unsafe_allow_html=True)
    if st.button(" ", icon=":material/arrow_forward:", use_container_width=True):
        st.session_state.start_date = st.session_state.start_date + relativedelta(months=1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data
def load_data(startdate = datetime.now()):
    enddate = startdate + relativedelta(months=1)
    startdate = startdate.strftime('%Y-%m-01')
    enddate = enddate.strftime('%Y-%m-01')
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    try:
        query=f"SELECT DISTINCT date, duree_totale, brossette, manger FROM raw_data where date >= '{startdate}' and date < '{enddate}'"
        df = pd.read_sql(query, conn)
        if len(df) != 0:
            df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600
            date_range = pd.date_range(start=pd.to_datetime(max(df['date'])) + relativedelta(days=1), end=pd.to_datetime(enddate) - relativedelta(days=1))
            dt = pd.DataFrame(date_range, columns=['date'])
            df = pd.merge(dt, df, on='date', how='outer')
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    finally:
        conn.close()
    return df

def call_update():
    api_url = "https://uhttp://192.168.1.28:8000/run-sync"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            st.success("Données mises à jour !")
        else:
            st.error(f"Erreur lors de l'appel de l'api: {response.status_code}")
    except Exception as e:
        st.error(f"Erreur: {e}")

with st.spinner('Chargement des données...'):
    data = load_data(startdate = st.session_state.start_date)

fig = px.bar(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='')
fig.update_xaxes(
    dtick="D1",
    tickformat="%d",
    ticklabelmode="instant")
fig.update_yaxes(range=[0, 10])
st.plotly_chart(fig)

col1, col2 = st.columns(2)

if data['brossette'].nunique() == 1 and data['brossette'].iloc[0] == 1:
    colors = ["green"]
else:
    colors = ["#F5F5F5", "#FFFFE5", "green"]

with col1:
    fig_brossette, ax = plt.subplots()
    july.month_plot(data['date'], data['brossette'], cmap=ListedColormap(colors), weeknum_label=False, fontfamily="monospace", date_label=True, ax=ax)
    ax.set_title("Brossette")
    st.pyplot(fig_brossette)

with col2:
    if st.button("Mise à jour"):
        call_update()
        load_data.clear()
        st.rerun()

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
    
