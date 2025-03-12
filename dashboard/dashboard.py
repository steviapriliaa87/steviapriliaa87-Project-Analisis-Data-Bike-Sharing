
import streamlit as st
import pandas as pd

# Judul Dashboard
st.title('📊 Dashboard Analisis Data Bike Sharing')

# Load data
import pandas as pd

day_df = pd.read_csv('data/day_data_bersih.csv')
hour_df = pd.read_csv('data/hour_data_bersih.csv')


# Tampilkan data
st.subheader('Data Harian')
st.dataframe(day_df.head())

st.subheader('Data Per Jam')
st.dataframe(hour_df.head())

# Tambahkan metrik
st.metric(label="Total Rentals (Daily)", value=day_df['total_rentals'].sum())
st.metric(label="Total Rentals (Hourly)", value=hour_df['total_rentals'].sum())
