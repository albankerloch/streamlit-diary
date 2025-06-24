import streamlit as st
import datetime

# Set the title of the app
st.title('Month Picker Example')

# Get the current year and month
current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

# Create a selectbox for the month
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
selected_month = st.selectbox("Select a month", months, index=current_month - 1)

# Create a number input for the year
selected_year = st.number_input("Select a year", min_value=1900, max_value=2100, value=current_year)

# Display the selected month and year
st.write(f'Selected month and year: {selected_month} {selected_year}')

# Optionally, you can convert the selected month and year to a datetime object
selected_date = datetime.datetime(selected_year, months.index(selected_month) + 1, 1)
st.write('Selected date as datetime object:', selected_date)