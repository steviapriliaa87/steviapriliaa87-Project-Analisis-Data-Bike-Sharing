import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Membaca dataset
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# buat filter
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

# 1. Penyewaan Sepeda berdasarkan Hari
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
# Mengelompokkan data berdasarkan jam dan menghitung rata-rata penyewaan
hourly_rentals = hour_df.groupby("hour")["total_rentals"].mean().reset_index()
# Membuat line plot menggunakan Plotly Express
fig = px.line(hourly_rentals, x='hour', y='total_rentals', 
              title='Rata-rata Penyewaan Sepeda per Jam', 
              labels={'hour': 'Jam', 'total_rentals': 'Jumlah Penyewaan'},
              markers=True)

st.plotly_chart(fig)


# 2. Penyewaan Berdasarkan bulan
# Grouping data berdasarkan bulan
avg_rentals_by_month = day_df.groupby("month")["total_rentals"].mean().reset_index()
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
avg_rentals_by_month['month_name'] = avg_rentals_by_month['month'].apply(lambda x: month_labels[x-1])
avg_rentals_by_month = avg_rentals_by_month.sort_values(by="month")
fig = px.bar(avg_rentals_by_month, 
             x='total_rentals', 
             y='month_name', 
             orientation='h', 
             title='Rata-rata Penyewaan Sepeda Berdasarkan Bulan',
             labels={'total_rentals': 'Rata-rata Penyewaan', 'month_name': 'Bulan'},
             color_discrete_sequence=["royalblue"])  # Semua warna biru
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
st.plotly_chart(fig)


# Penyewaan Berdasarkan Hari dalam Seminggu
st.subheader("Penyewaan Berdasarkan Hari dalam Seminggu")
fig_weekday = px.bar(day_df.groupby('one_of_week')['total_rentals'].sum().reset_index(), x='one_of_week', y='total_rentals', title="Total Penyewaan per Hari dalam Seminggu")
st.plotly_chart(fig_weekday)

# **Pola Penyewaan Sepeda per Jam (Line Chart dengan Marker)**
st.subheader("Pola Penyewaan Sepeda per Jam")

# Mengelompokkan data berdasarkan jam dalam sehari
df_hourly = hour_df.groupby('hour')['total_rentals'].mean().reset_index()

fig, ax = plt.subplots()
ax.plot(df_hourly['hour'], df_hourly['total_rentals'], marker='o', linestyle='-', color='b')

ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
ax.grid(True)

st.pyplot(fig)

# Scatter Plot Penyewaan vs. Suhu Udara
st.subheader("Pengaruh Suhu terhadap Penyewaan")
fig_scatter = px.scatter(df_filtered, x='temperature', y='total_rentals', color='weather_condition', title="Hubungan Suhu dan Penyewaan Sepeda")
st.plotly_chart(fig_scatter)

# Penyewaan Berdasarkan Bulan
st.subheader("Penyewaan Berdasarkan Bulan")
fig_month = px.bar(df_filtered.groupby('month')['total_rentals'].sum().reset_index(), x='month', y='total_rentals', title='Total Penyewaan per Bulan')
st.plotly_chart(fig_month)
