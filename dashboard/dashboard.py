import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
day_data_path = "day_data_bersih.csv"
hour_data_path = "hour_data_bersih.csv"

day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

# Convert date column to datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_season = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)
selected_temp = st.sidebar.slider("Pilih Rentang Suhu", float(day_df['temperature'].min()), float(day_df['temperature'].max()), (float(day_df['temperature'].min()), float(day_df['temperature'].max())))

# Apply filters
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & 
                      (day_df['season'].isin(selected_season)) & 
                      (day_df['month'].isin(selected_month)) &
                      (day_df['temperature'].between(selected_temp[0], selected_temp[1]))]
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

# Line Chart Penyewaan Sepeda
st.subheader("Tren Penyewaan Sepeda")
fig = px.line(df_filtered, x='date', y='total_rentals', title='Tren Penyewaan Sepeda Harian', labels={'total_rentals': 'Total Penyewaan'})
st.plotly_chart(fig)

# Perbandingan Penyewaan Antar Tahun
st.subheader("Perbandingan Penyewaan Antar Tahun")
fig_yearly = px.bar(day_df.groupby(day_df['date'].dt.year)['total_rentals'].sum().reset_index(), x='date', y='total_rentals', title='Total Penyewaan Sepeda per Tahun')
st.plotly_chart(fig_yearly)

# Heatmap Penyewaan Sepeda per Jam
st.subheader("Heatmap Penyewaan Sepeda per Jam")
heatmap_data = hour_df.groupby(['hour', 'one_of_week']).sum()['total_rentals'].reset_index()
fig_heatmap = px.density_heatmap(heatmap_data, x='hour', y='one_of_week', z='total_rentals', color_continuous_scale='Viridis', title="Pola Penyewaan per Jam")
st.plotly_chart(fig_heatmap)

# Scatter Plot Faktor Cuaca
st.subheader("Pengaruh Suhu terhadap Penyewaan")
fig_scatter = px.scatter(df_filtered, x='temperature', y='total_rentals', color='weather_condition', title="Hubungan Suhu dan Penyewaan Sepeda")
st.plotly_chart(fig_scatter)

# Distribusi Penyewaan Sepeda per Jam
st.subheader("Distribusi Penyewaan Sepeda per Jam")
fig_hist = px.histogram(hour_df, x='hour', y='total_rentals', nbins=24, title="Distribusi Penyewaan per Jam", labels={'total_rentals': 'Total Penyewaan'})
st.plotly_chart(fig_hist)

# Penyewaan berdasarkan Hari dalam Seminggu
st.subheader("Penyewaan Berdasarkan Hari dalam Seminggu")
fig_weekday = px.bar(day_df.groupby('one_of_week')['total_rentals'].sum().reset_index(), x='one_of_week', y='total_rentals', title="Total Penyewaan per Hari dalam Seminggu")
st.plotly_chart(fig_weekday)

# Tombol Download Data
st.sidebar.markdown("---")
st.sidebar.subheader("Download Data")
st.sidebar.download_button(label="Unduh Data yang Difilter", data=df_filtered.to_csv(index=False), file_name="filtered_data.csv", mime="text/csv")

st.write("Dashboard interaktif ini memungkinkan pengguna untuk menganalisis tren penyewaan sepeda berdasarkan musim, cuaca, waktu, dan faktor lainnya.")
