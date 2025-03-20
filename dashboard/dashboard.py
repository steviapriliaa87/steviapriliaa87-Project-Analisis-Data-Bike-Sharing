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
selected_year = st.sidebar.multiselect("Pilih Tahun", sorted(day_df['date'].dt.year.unique()), default=sorted(day_df['date'].dt.year.unique()))
selected_month = st.sidebar.multiselect("Pilih Bulan", sorted(day_df['month'].unique()), default=sorted(day_df['month'].unique()))
selected_weekday = st.sidebar.multiselect("Pilih Hari dalam Seminggu", ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], default=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
selected_hour = st.sidebar.multiselect("Pilih Jam dalam Sehari", sorted(hour_df['hour'].unique()), default=sorted(hour_df['hour'].unique()))
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", hour_df['weather_condition'].unique(), default=hour_df['weather_condition'].unique())
selected_user_type = st.sidebar.radio("Pilih Jenis Pengguna", ["Semua", "Registered", "Casual"], index=0)

# Filter dataset sesuai pilihan
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & 
                      (day_df['month'].isin(selected_month)) & 
                      (day_df['one_of_week'].isin(selected_weekday))]

hour_filtered = hour_df[(hour_df['date'].dt.year.isin(selected_year)) & 
                         (hour_df['hour'].isin(selected_hour)) & 
                         (hour_df['weather_condition'].isin(selected_weather))]

if selected_user_type == "Registered":
    df_filtered['total_rentals'] = df_filtered['registered_rentals']
    hour_filtered['total_rentals'] = hour_filtered['registered_rentals']
elif selected_user_type == "Casual":
    df_filtered['total_rentals'] = df_filtered['casual_rentals']
    hour_filtered['total_rentals'] = hour_filtered['casual_rentals']

st.title("🚲 Dashboard Penyewaan Sepeda")
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered['total_rentals'].sum())
col2.metric("Rata-rata Harian", round(df_filtered['total_rentals'].mean(), 2))
col3.metric("Penyewaan Tertinggi", df_filtered['total_rentals'].max())

# 1. Penyewaan Sepeda berdasarkan Jam
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
hourly_rentals = hour_filtered.groupby("hour")["total_rentals"].mean().reset_index()
fig = px.line(hourly_rentals, x='hour', y='total_rentals', 
              labels={'hour': 'Jam', 'total_rentals': 'Jumlah Penyewaan'},
              markers=True)
st.plotly_chart(fig)

# 2. Penyewaan Berdasarkan Bulan
day_df["month"] = pd.Categorical(day_df["month"], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
avg_rentals_by_month = df_filtered.groupby("month", observed=False)["total_rentals"].mean().reset_index()
fig = px.bar(avg_rentals_by_month, x='total_rentals', y='month', orientation='h', labels={'total_rentals': 'Rata-rata Penyewaan', 'month': 'Bulan'}, color_discrete_sequence=["royalblue"])
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
st.plotly_chart(fig)

# 3. Penyewaan Berdasarkan Hari
avg_rentals_by_weekday = df_filtered.groupby("one_of_week")["total_rentals"].mean().reset_index()
order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
avg_rentals_by_weekday["one_of_week"] = pd.Categorical(avg_rentals_by_weekday["one_of_week"], categories=order, ordered=True)
fig = px.bar(avg_rentals_by_weekday, x="one_of_week", y="total_rentals", title="Rata-rata Penyewaan Sepeda dalam Seminggu", labels={"total_rentals": "Rata-rata Penyewaan", "one_of_week": "Hari"}, color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)

# 4. Penyewaan Berdasarkan Kondisi Cuaca
avg_rentals_by_weather = hour_filtered.groupby('weather_condition', observed=True)['total_rentals'].mean().reset_index()
fig = px.bar(avg_rentals_by_weather, x="weather_condition", y="total_rentals", title="Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", labels={"total_rentals": "Rata-rata Penyewaan", "weather_condition": "Kondisi Cuaca"}, color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)

# 5. Penyewaan Berdasarkan jenis Penyewa 
total_registered = df_filtered['registered_rentals'].sum()
total_casual = df_filtered['casual_rentals'].sum()
data = pd.DataFrame({"Kategori": ["Registered", "Casual"], "Jumlah": [total_registered, total_casual]})
fig = px.pie(data, names="Kategori", values="Jumlah", color="Kategori", color_discrete_map={"Registered": "darkblue", "Casual": "lightblue"}, title="Perbandingan Penyewa Registered vs Casual", hole=0.3)
st.plotly_chart(fig)

# 6. Penyewaan Sepeda Berdasarkan Tahun
st.subheader("Perbandingan Tren Penyewaan Sepeda Berdasarkan Tahun")
monthly_trend = df_filtered.groupby(["year", "month"], observed=True)["total_rentals"].sum().reset_index()
fig = px.line(monthly_trend, x="month", y="total_rentals", color="year", 
              markers=True, labels={"month": "Bulan", "total_rentals": "Total Penyewaan", "year": "Tahun"}, 
              title="Perbandingan Tren Penyewaan Sepeda")
st.plotly_chart(fig)
