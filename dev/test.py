import streamlit as st
from calendar import month_abbr
from datetime import datetime

with st.expander('Report month'):
    this_year = datetime.now().year
    this_month = datetime.now().month
    report_year = st.selectbox("", range(this_year, this_year - 2, -1))
    month_abbr = month_abbr[1:]
    report_month_str = st.radio("", month_abbr, index=this_month - 1, horizontal=True)
    report_month = month_abbr.index(report_month_str) + 1

# Result
st.text(f'{report_year} {report_month_str}')