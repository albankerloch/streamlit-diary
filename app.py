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
    query="SELECT DISTINCT date, duree_totale, brossette FROM diary.raw_data where date >= STR_TO_DATE('01/03/2025', '%d/%m/%Y') "
    df = pd.read_sql(query, conn)
    df['duree_heure'] = df['duree_totale'].dt.total_seconds() / 3600 
    conn.close()
    return df

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("")

data_brossette = data[['date', 'brossette']]
data_brossette.set_index('date', inplace=True)

fig = px.line(data, x='date', y='duree_heure', labels={'date': 'Date', 'duree_heure': 'Travail (heures)'}, title='Travail par jour')

# Afficher le graphique
st.plotly_chart(fig)

# Afficher le calendrier
fig_brossette, ax = calmap.calendarplot(data_brossette['brossette'], 
    daylabels=['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
    monthlabels=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novvembre', 'Décembre'],
    cmap='YlGn', 
    fig_kws={'figsize': (12, 4)})
st.pyplot(fig_brossette)

## Create data
dates_july = date_range("2025-03-01", "2025-03-20")
data_july = np.random.randint(0, 100, len(dates_july))

## Create a figure with a single axes
fig, ax = plt.subplots()

## Tell july to make a plot in a specific axes
july.month_plot(dates_july, data_brossette['brossette'], month=3, date_label=True, ax=ax, colorbar=True)

## Tell streamlit to display the figure
st.pyplot(fig)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)