import os.path

import altair as alt
import pandas as pd
import streamlit as st

import mysql.connector
import os
from dotenv import load_dotenv

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
    query='SELECT * FROM diary.raw_data'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
