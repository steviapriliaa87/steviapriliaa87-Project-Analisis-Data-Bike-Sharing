import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
day_data_path = "day_data_bersih.csv"
hour_data_path = "hour_data_bersih.csv"

day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

# Convert date column to datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar filters
st.sidebar.header("📊 Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_season = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)

# Apply filters
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & 
                      (day_df['season'].isin(selected_season)) & 
                      (day_df['month'].isin(selected_month))]
if selected_day_type == "Hari Kerja":
    df_filtered = df_filtered[df_filtered['working_day'] == 1]
elif selected_day_type == "Libur":
    df_filtered = df_filtered[df_filtered['working_day'] == 0]

# Main Dashboard
st.title("🚲 Dashboard Penyewaan Sepeda")
st.markdown("### Analisis Tren dan Pola Penyewaan Sepeda")

# Metrics Section
col1, col2, col3 = st.columns(3)
col1.metric("📈 Total Penyewaan", df_filtered['total_rentals'].sum())
col2.metric("📊 Rata-rata Harian", round(df_filtered['total_rentals'].mean(), 2))
col3.metric("🏆 Penyewaan Tertinggi", df_filtered['total_rentals'].max())

# Line Chart Tren Penyewaan Sepeda
st.markdown("---")
st.subheader("📅 Tren Penyewaan Sepeda Harian")
fig = px.line(df_filtered, x='date', y='total_rentals', title='Tren Penyewaan Sepeda Harian', 
              labels={'total_rentals': 'Total Penyewaan'}, color_discrete_sequence=['#00A86B'])
st.plotly_chart(fig, use_container_width=True)

# Penyewaan Berdasarkan Musim
st.subheader("🌦️ Total Penyewaan Berdasarkan Musim")
fig_season = px.bar(df_filtered.groupby('season')['total_rentals'].sum().reset_index(), x='season', y='total_rentals', 
                    title='Total Penyewaan per Musim', color='season', color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_season, use_container_width=True)

# Penyewaan Berdasarkan Hari dalam Seminggu
st.subheader("📅 Penyewaan Berdasarkan Hari dalam Seminggu")
fig_weekday = px.bar(df_filtered.groupby('one_of_week')['total_rentals'].sum().reset_index(), x='one_of_week', 
                     y='total_rentals', title="Total Penyewaan per Hari dalam Seminggu", 
                     color='one_of_week', color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig_weekday, use_container_width=True)

# Heatmap Penyewaan Sepeda per Jam
st.subheader("🔥 Heatmap Penyewaan Sepeda per Jam")
heatmap_data = hour_df.groupby(['hour', 'one_of_week'])['total_rentals'].sum().reset_index()
fig_heatmap = px.density_heatmap(heatmap_data, x='hour', y='one_of_week', z='total_rentals', 
                                 color_continuous_scale='Viridis', title="Pola Penyewaan per Jam")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Scatter Plot Penyewaan vs. Suhu Udara
st.subheader("🌡️ Pengaruh Suhu terhadap Penyewaan")
fig_scatter = px.scatter(df_filtered, x='temperature', y='total_rentals', color='weather_condition', 
                         title="Hubungan Suhu dan Penyewaan Sepeda", color_discrete_sequence=px.colors.qualitative.T10)
st.plotly_chart(fig_scatter, use_container_width=True)

# Penyewaan Berdasarkan Bulan
st.subheader("📆 Penyewaan Berdasarkan Bulan")
fig_month = px.bar(df_filtered.groupby('month')['total_rentals'].sum().reset_index(), x='month', y='total_rentals', 
                   title='Total Penyewaan per Bulan', color='month', color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig_month, use_container_width=True)

# Tombol Download Data
st.sidebar.markdown("---")
st.sidebar.subheader("⬇️ Download Data")
st.sidebar.download_button(label="Unduh Data yang Difilter", data=df_filtered.to_csv(index=False), file_name="filtered_data.csv", mime="text/csv")

st.write("Dashboard ini memberikan wawasan mendalam tentang pola penyewaan sepeda berdasarkan berbagai faktor seperti musim, cuaca, dan waktu.")
