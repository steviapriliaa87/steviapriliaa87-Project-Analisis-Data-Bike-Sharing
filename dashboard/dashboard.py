import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load Data
day_data_path = "data/day_data_bersih.csv"
hour_data_path = "data/hour_data_bersih.csv"

day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_season = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)

df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & 
                      (day_df['season'].isin(selected_season)) & 
                      (day_df['month'].isin(selected_month))]
if selected_day_type == "Hari Kerja":
    df_filtered = df_filtered[df_filtered['working_day'] == 1]
elif selected_day_type == "Libur":
    df_filtered = df_filtered[df_filtered['working_day'] == 0]

# Main Dashboard
st.title("🚲 Dashboard Penyewaan Sepeda")
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered['total_rentals'].sum())
col2.metric("Rata-rata Harian", round(df_filtered['total_rentals'].mean(), 2))
col3.metric("Penyewaan Tertinggi", df_filtered['total_rentals'].max())

# 1. Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda Harian")
fig_trend = px.line(df_filtered, x='date', y='total_rentals', title='Tren Penyewaan Sepeda Harian', labels={'total_rentals': 'Total Penyewaan'})
st.plotly_chart(fig_trend)

# 2. Penyewaan Berdasarkan Musim
st.subheader("🌦️ Penyewaan Berdasarkan Musim")
fig_season = px.bar(df_filtered.groupby('season')['total_rentals'].sum().reset_index(), x='season', y='total_rentals', title='Total Penyewaan per Musim')
st.plotly_chart(fig_season)

# 3. Penyewaan Berdasarkan Hari dalam Seminggu
st.subheader("📅 Penyewaan Berdasarkan Hari dalam Seminggu")
fig_weekday = px.bar(day_df.groupby('one_of_week')['total_rentals'].sum().reset_index(), x='one_of_week', y='total_rentals', title="Total Penyewaan per Hari dalam Seminggu")
st.plotly_chart(fig_weekday)

# 4. Pola Penyewaan Sepeda per Jam
st.subheader("🕒 Pola Penyewaan Sepeda per Jam")
df_hourly = hour_df.groupby('hour')['total_rentals'].mean().reset_index()
fig_hourly = px.line(df_hourly, x='hour', y='total_rentals', markers=True, title='Rata-rata Penyewaan Sepeda per Jam')
st.plotly_chart(fig_hourly)

# 5. Scatter Plot Penyewaan vs. Suhu Udara
st.subheader("🌡️ Pengaruh Suhu terhadap Penyewaan")
fig_scatter = px.scatter(df_filtered, x='temperature', y='total_rentals', color='weather_condition', title="Hubungan Suhu dan Penyewaan Sepeda")
st.plotly_chart(fig_scatter)

# 6. Penyewaan Berdasarkan Bulan
st.subheader("📆 Penyewaan Berdasarkan Bulan")
fig_month = px.bar(df_filtered.groupby('month')['total_rentals'].sum().reset_index(), x='month', y='total_rentals', title='Total Penyewaan per Bulan')
st.plotly_chart(fig_month)
