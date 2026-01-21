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
password=os.getenv('DATABASE_PASSWORD')

style = "<style>h1 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
style2 = "<style>h3 {text-align: center;}</style>"
st.markdown(style2, unsafe_allow_html=True)

st.title("Journ-Alban")
st.markdown('</div>', unsafe_allow_html=True)

if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now()

