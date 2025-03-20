import streamlit as st
import pandas as pd
import plotly.express as px

# Membaca dataset
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar untuk filter
st.sidebar.header("Filter Data")

# Filter Tahun
all_years = sorted(day_df['date'].dt.year.unique())
selected_year = st.sidebar.multiselect("Pilih Tahun", ["Semua"] + all_years, default=["Semua"])

# Filter Musim
all_seasons = day_df['season'].unique()
selected_season = st.sidebar.multiselect("Pilih Musim", ["Semua"] + list(all_seasons), default=["Semua"])

# Filter Bulan
all_months = day_df['month'].unique()
selected_month = st.sidebar.multiselect("Pilih Bulan", ["Semua"] + list(all_months), default=["Semua"])

# Filter Jenis Hari
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)

# Filter dataset sesuai pilihan
if "Semua" not in selected_year:
    day_df = day_df[day_df['date'].dt.year.isin(selected_year)]
if "Semua" not in selected_season:
    day_df = day_df[day_df['season'].isin(selected_season)]
if "Semua" not in selected_month:
    day_df = day_df[day_df['month'].isin(selected_month)]
if selected_day_type == "Hari Kerja":
    day_df = day_df[day_df['working_day'] == 1]
elif selected_day_type == "Libur":
    day_df = day_df[day_df['working_day'] == 0]

st.title("🚲 Dashboard Penyewaan Sepeda")
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", day_df['total_rentals'].sum())
col2.metric("Rata-rata Harian", round(day_df['total_rentals'].mean(), 2))
col3.metric("Penyewaan Tertinggi", day_df['total_rentals'].max())

# Visualisasi
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
hourly_rentals = hour_df.groupby("hour")["total_rentals"].mean().reset_index()
fig = px.line(hourly_rentals, x='hour', y='total_rentals', markers=True)
st.plotly_chart(fig)

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
avg_rentals_by_month = day_df.groupby("month")["total_rentals"].mean().reset_index()
fig = px.bar(avg_rentals_by_month, x='month', y='total_rentals', color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)

st.subheader("Rata-rata Penyewaan Sepeda dalam Seminggu")
avg_rentals_by_weekday = day_df.groupby("one_of_week")["total_rentals"].mean().reset_index()
fig = px.bar(avg_rentals_by_weekday, x="one_of_week", y="total_rentals", color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
avg_rentals_by_weather = day_df.groupby('weather_condition')['total_rentals'].mean().reset_index()
fig = px.bar(avg_rentals_by_weather, x="weather_condition", y="total_rentals", color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)

st.subheader("Perbandingan Penyewa Registered vs Casual")
total_registered = day_df['registered_rentals'].sum()
total_casual = day_df['casual_rentals'].sum()
data = pd.DataFrame({"Kategori": ["Registered", "Casual"], "Jumlah": [total_registered, total_casual]})
fig = px.pie(data, names="Kategori", values="Jumlah", hole=0.3)
st.plotly_chart(fig)

st.subheader("Perbandingan Tren Penyewaan Sepeda Berdasarkan Tahun")
monthly_trend = day_df.groupby(["year", "month"])["total_rentals"].sum().reset_index()
fig = px.line(monthly_trend, x="month", y="total_rentals", color="year", markers=True)
st.plotly_chart(fig)
