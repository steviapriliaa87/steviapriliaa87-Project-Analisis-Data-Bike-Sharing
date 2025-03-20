import streamlit as st
import pandas as pd
import plotly.express as px

# Membaca dataset
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

# Konversi tipe data datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar untuk filter
st.sidebar.header("🔍 Filter Data")

# Filter Pilih Tahun (Dropdown)
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(day_df['date'].dt.year.unique()), index=0)

# Filter Pilih Hari dalam Seminggu (Dropdown)
days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
selected_day = st.sidebar.selectbox("Pilih Hari", days_order, index=0)

# Filter Pilih Kondisi Cuaca (Dropdown)
weather_options = day_df["weather_condition"].unique()
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca", weather_options, index=0)

# Filter Pilih Jenis Hari (Dropdown)
day_type_options = {"Semua": None, "Hari Kerja": 1, "Libur": 0}
selected_day_type = st.sidebar.selectbox("Pilih Jenis Hari", list(day_type_options.keys()), index=0)

# Filter Pilih Jenis Penyewa (Dropdown)
renter_options = {"Semua": None, "Registered": "registered_rentals", "Casual": "casual_rentals"}
selected_renter = st.sidebar.selectbox("Pilih Jenis Penyewa", list(renter_options.keys()), index=0)

# Filter dataset sesuai pilihan
df_filtered = day_df[day_df['date'].dt.year == selected_year]

if selected_day_type != "Semua":
    df_filtered = df_filtered[df_filtered["working_day"] == day_type_options[selected_day_type]]

if selected_weather:
    df_filtered = df_filtered[df_filtered["weather_condition"] == selected_weather]

if selected_renter != "Semua":
    df_filtered = df_filtered[["date", selected_renter]]

# Tampilan Dashboard
st.title("🚲 Dashboard Penyewaan Sepeda")
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered["total_rentals"].sum())
col2.metric("Rata-rata Harian", round(df_filtered["total_rentals"].mean(), 2))
col3.metric("Penyewaan Tertinggi", df_filtered["total_rentals"].max())

# Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Hari
avg_rentals_by_weekday = df_filtered.groupby("one_of_week")["total_rentals"].mean().reset_index()
avg_rentals_by_weekday["one_of_week"] = pd.Categorical(avg_rentals_by_weekday["one_of_week"], categories=days_order, ordered=True)
fig = px.bar(avg_rentals_by_weekday, x="one_of_week", y="total_rentals",
             title="Rata-rata Penyewaan Sepeda Berdasarkan Hari",
             labels={"one_of_week": "Hari", "total_rentals": "Jumlah Penyewaan"},
             color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)
