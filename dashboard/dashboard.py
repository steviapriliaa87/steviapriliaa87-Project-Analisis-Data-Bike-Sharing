import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
day_data_path = "data/day_data_bersih.csv"
hour_data_path = "data/hour_data_bersih.csv"

day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

# Convert date column to datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
selected_years = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_season = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
selected_months = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())

# Apply Filters
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_years)) & 
                      (day_df['season'].isin(selected_season)) & 
                      (day_df['month'].isin(selected_months))]

# Dashboard Header
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("Lihat tren penyewaan sepeda berdasarkan musim, waktu, dan faktor lainnya.")

# Ringkasan Statistik
st.subheader("📊 Ringkasan Statistik")
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered['total_rentals'].sum())
col2.metric("Rata-rata Harian", round(df_filtered['total_rentals'].mean(), 2))
col3.metric("Penyewaan Tertinggi", df_filtered['total_rentals'].max())

# Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda")
grafik_tren = st.radio("Pilih Rentang Waktu", ["Harian", "Mingguan", "Bulanan"], index=0)

if grafik_tren == "Harian":
    tren_df = df_filtered
    x_col = 'date'
elif grafik_tren == "Mingguan":
    tren_df = df_filtered.resample('W', on='date').sum().reset_index()
    x_col = 'date'
elif grafik_tren == "Bulanan":
    tren_df = df_filtered.resample('M', on='date').sum().reset_index()
    x_col = 'date'

fig_tren = px.line(tren_df, x=x_col, y='total_rentals', title=f'Tren Penyewaan Sepeda ({grafik_tren})')
st.plotly_chart(fig_tren)

# Perbandingan Penyewaan Antar Tahun
st.subheader("📅 Perbandingan Penyewaan per Tahun")
fig_yearly = px.bar(day_df.groupby(day_df['date'].dt.year)['total_rentals'].sum().reset_index(),
                    x='date', y='total_rentals', title='Total Penyewaan Sepeda per Tahun')
st.plotly_chart(fig_yearly)

# Penyewaan Berdasarkan Hari dalam Seminggu
st.subheader("📆 Penyewaan per Hari dalam Seminggu")
fig_weekday = px.bar(day_df.groupby('day_of_week')['total_rentals'].sum().reset_index(),
                     x='day_of_week', y='total_rentals',
                     title="Total Penyewaan per Hari dalam Seminggu",
                     color='total_rentals', color_continuous_scale='Blues')
st.plotly_chart(fig_weekday)

# Distribusi Penyewaan Sepeda per Jam
st.subheader("🕒 Distribusi Penyewaan Sepeda per Jam")
fig_hour = px.bar(hour_df.groupby('hour')['total_rentals'].sum().reset_index(),
                  x='hour', y='total_rentals',
                  title='Total Penyewaan Sepeda per Jam',
                  color='total_rentals', color_continuous_scale='Oranges')
st.plotly_chart(fig_hour)

# Tombol Download Data
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Download Data")
st.sidebar.download_button(label="Unduh Data yang Difilter", 
                           data=df_filtered.to_csv(index=False), 
                           file_name="filtered_data.csv", 
                           mime="text/csv")

st.write("Dashboard ini memungkinkan eksplorasi interaktif dari tren penyewaan sepeda.")
