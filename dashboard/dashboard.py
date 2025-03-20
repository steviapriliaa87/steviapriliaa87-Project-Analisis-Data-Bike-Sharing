import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

#1.Penyewaan Sepeda berdasarkan Jam
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
hourly_rentals = hour_df.groupby("hour")["total_rentals"].mean().reset_index()
fig = px.line(hourly_rentals, x='hour', y='total_rentals', 
              title='Rata-rata Penyewaan Sepeda per Jam', 
              labels={'hour': 'Jam', 'total_rentals': 'Jumlah Penyewaan'},
              markers=True)
st.plotly_chart(fig)


#2.Penyewaan Berdasarkan bulan
# **Grouping data berdasarkan hari dalam seminggu**
avg_rentals_by_weekday = (
    day_df.groupby("one_of_week")["total_rentals"]
    .mean()
    .reset_index()
)

# **Urutan hari dalam seminggu**
order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
avg_rentals_by_weekday["one_of_week"] = pd.Categorical(
    avg_rentals_by_weekday["one_of_week"], categories=order, ordered=True
)
avg_rentals_by_weekday = avg_rentals_by_weekday.sort_values("one_of_week")

# **Buat visualisasi dengan Plotly**
fig = px.bar(
    avg_rentals_by_weekday, 
    x="total_rentals", 
    y="one_of_week", 
    orientation="h",  # Horizontal bar
    title="Rata-rata Penyewaan Sepeda dalam Seminggu",
    labels={"total_rentals": "Rata-rata Penyewaan", "one_of_week": "Hari"},
    color_discrete_sequence=["royalblue"],  # Warna batang
    hover_data={"total_rentals": ":,.0f", "one_of_week": True}  # Tooltip interaktif
)

# **Tampilkan grafik di Streamlit**
st.plotly_chart(fig)


# Scatter Plot Penyewaan vs. Suhu Udara
st.subheader("Pengaruh Suhu terhadap Penyewaan")
fig_scatter = px.scatter(df_filtered, x='temperature', y='total_rentals', color='weather_condition', title="Hubungan Suhu dan Penyewaan Sepeda")
st.plotly_chart(fig_scatter)

# Penyewaan Berdasarkan Bulan
st.subheader("Penyewaan Berdasarkan Bulan")
fig_month = px.bar(df_filtered.groupby('month')['total_rentals'].sum().reset_index(), x='month', y='total_rentals', title='Total Penyewaan per Bulan')
st.plotly_chart(fig_month)
