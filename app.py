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
from july.utils import date_range


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
    query="SELECT DISTINCT date, duree_totale, brossette FROM diary.raw_data where date >= DATE_FORMAT(NOW(), '%Y-%m-01')"
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600 
    conn.close()
    return df

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("")

data_brossette = data[['date', 'brossette']]
data_brossette['date'] = pd.to_datetime(data_brossette['date']).dt.strftime('%Y-%m-%d')

fig = px.line(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='Travail par jour')
st.plotly_chart(fig)

fig_brossette, ax = plt.subplots()
july.month_plot(data_brossette['date'], data_brossette['brossette'], month=3, date_label=True, ax=ax, colorbar=True)
st.pyplot(fig_brossette)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)