import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
day_data_path = "data/day_data_bersih.csv"
hour_data_path = "data/hour_data_bersih.csv"

day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)

# Apply filters
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & (day_df['month'].isin(selected_month))]
if selected_day_type == "Hari Kerja":
    df_filtered = df_filtered[df_filtered['workingday'] == 1]
elif selected_day_type == "Libur":
    df_filtered = df_filtered[df_filtered['workingday'] == 0]

# Dashboard Title
st.title("Dashboard Penyewaan Sepeda")

# 1. Rata-rata penyewaan berdasarkan jam
hourly_avg = hour_df.groupby('hour')['count'].mean().reset_index()
fig1 = px.line(hourly_avg, x='hour', y='count', title="Rata-rata Penyewaan Sepeda per Jam")
st.plotly_chart(fig1)

# 2. Rata-rata penyewaan sepeda berdasarkan bulan
monthly_avg = day_df.groupby('month')['count'].mean().reset_index()
fig2 = px.bar(monthly_avg, x='month', y='count', title="Rata-rata Penyewaan Sepeda per Bulan")
st.plotly_chart(fig2)

# 3. Rata-rata penyewaan berdasarkan hari dalam seminggu
day_avg = day_df.groupby('weekday')['count'].mean().reset_index()
fig3 = px.bar(day_avg, x='weekday', y='count', title="Rata-rata Penyewaan Sepeda per Hari dalam Seminggu")
st.plotly_chart(fig3)

# 4. Rata-rata penyewaan berdasarkan cuaca
weather_avg = day_df.groupby('weather')['count'].mean().reset_index()
fig4 = px.bar(weather_avg, x='weather', y='count', title="Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
st.plotly_chart(fig4)

# 5. Perbandingan Penyewa Registered vs Casual
fig5 = px.bar(day_df, x='date', y=['casual', 'registered'], title="Perbandingan Penyewa Registered vs Casual", barmode='stack')
st.plotly_chart(fig5)

# 6. Perbandingan total penyewa antara hari kerja vs hari libur
workday_avg = day_df.groupby('workingday')['count'].mean().reset_index()
workday_avg['workingday'] = workday_avg['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur'})
fig6 = px.bar(workday_avg, x='workingday', y='count', title="Perbandingan Total Penyewa: Hari Kerja vs Hari Libur")
st.plotly_chart(fig6)

# 7. Perbandingan Tren Penyewaan Sepeda: 2011 vs 2012
yearly_trend = day_df.groupby([day_df['date'].dt.year, 'month'])['count'].sum().reset_index()
fig7 = px.line(yearly_trend, x='month', y='count', color='date', title="Perbandingan Tren Penyewaan Sepeda: 2011 vs 2012")
st.plotly_chart(fig7)
