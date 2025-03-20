import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Membaca dataset
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_season = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)

# Filter dataset sesuai pilihan
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & 
                      (day_df['season'].isin(selected_season)) & 
                      (day_df['month'].isin(selected_month))]

if selected_day_type == "Hari Kerja":
    df_filtered = df_filtered[df_filtered['working_day'] == 1]
elif selected_day_type == "Libur":
    df_filtered = df_filtered[df_filtered['working_day'] == 0]

st.title("🚲 Dashboard Penyewaan Sepeda")
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered['total_rentals'].sum())
col2.metric("Rata-rata Harian", round(df_filtered['total_rentals'].mean(), 2))
col3.metric("Penyewaan Tertinggi", df_filtered['total_rentals'].max())

# 1. Penyewaan Sepeda berdasarkan Jam
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
hourly_rentals = hour_df.groupby("hour")["total_rentals"].mean().reset_index()
fig = px.line(hourly_rentals, x='hour', y='total_rentals', 
              labels={'hour': 'Jam', 'total_rentals': 'Jumlah Penyewaan'},
              markers=True)
st.plotly_chart(fig)

# 2. Penyewaan Berdasarkan Bulan
day_df["month"] = pd.Categorical(day_df["month"], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
avg_rentals_by_month = df_filtered.groupby("month", observed=False)["total_rentals"].mean().reset_index()
avg_rentals_by_month["month"] = pd.Categorical(avg_rentals_by_month["month"], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
avg_rentals_by_month = avg_rentals_by_month.sort_values("month")
fig = px.bar(avg_rentals_by_month, x='total_rentals', y='month', orientation='h', labels={'total_rentals': 'Rata-rata Penyewaan', 'month': 'Bulan'}, color_discrete_sequence=["royalblue"])
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
st.plotly_chart(fig)

# 3. Penyewaan Berdasarkan Hari
avg_rentals_by_weekday = df_filtered.groupby("one_of_week")["total_rentals"].mean().reset_index()
order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
avg_rentals_by_weekday["one_of_week"] = pd.Categorical(avg_rentals_by_weekday["one_of_week"], categories=order, ordered=True)
avg_rentals_by_weekday = avg_rentals_by_weekday.sort_values("one_of_week")
fig = px.bar(avg_rentals_by_weekday, x="one_of_week", y="total_rentals", title="Rata-rata Penyewaan Sepeda dalam Seminggu", labels={"total_rentals": "Rata-rata Penyewaan", "one_of_week": "Hari"}, color_discrete_sequence=["royalblue"], hover_data={"total_rentals": ":,.0f", "one_of_week": True})
st.plotly_chart(fig)

# 4. Penyewaan Berdasarkan Kondisi Cuaca
avg_rentals_by_weather = hour_df.groupby('weather_condition', observed=True)['total_rentals'].mean().reset_index()
weather_order = ["clear", "misty", "light rain/light snow", "bad weather"]
avg_rentals_by_weather["weather_condition"] = pd.Categorical(avg_rentals_by_weather["weather_condition"], categories=weather_order, ordered=True)
avg_rentals_by_weather = avg_rentals_by_weather.sort_values("weather_condition")
fig = px.bar(avg_rentals_by_weather, x="weather_condition", y="total_rentals", title="Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", labels={"total_rentals": "Rata-rata Penyewaan", "weather_condition": "Kondisi Cuaca"}, color_discrete_sequence=["royalblue"])
st.plotly_chart(fig)

# 5. Penyewaan Berdasarkan jenis Penyewa 
total_registered = df_filtered['registered_rentals'].sum()
total_casual = df_filtered['casual_rentals'].sum()
data = pd.DataFrame({"Kategori": ["Registered", "Casual"], "Jumlah": [total_registered, total_casual]})

fig = px.pie(data, names="Kategori", values="Jumlah", color="Kategori", color_discrete_map={"Registered": "darkblue", "Casual": "lightblue"}, title="Perbandingan Penyewa Registered vs Casual", hole=0.3)

# Menonaktifkan label langsung, tapi tetap bisa muncul saat hover
fig.update_traces(textinfo="none", hoverinfo="label+percent+value")

st.plotly_chart(fig, use_container_width=True)

#6.Penyewaan Sepeda Berdasarkan Tahun
st.subheader("Perbandingan Tren Penyewaan Sepeda Berdasarkan Tahun")

selected_compare_years = st.multiselect("Pilih Tahun untuk Dibandingkan", day_df['date'].dt.year.unique(), default=[2011, 2012])

monthly_trend = day_df.groupby(["year", "month"], observed=True)["total_rentals"].sum().reset_index()
monthly_trend["month"] = pd.Categorical(monthly_trend["month"], 
                                         categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
                                         ordered=True)
monthly_trend = monthly_trend[monthly_trend["year"].isin(selected_compare_years)]

fig = px.line(monthly_trend, x="month", y="total_rentals", color="year", 
              markers=True, labels={"month": "Bulan", "total_rentals": "Total Penyewaan", "year": "Tahun"}, 
              title="Perbandingan Tren Penyewaan Sepeda")
st.plotly_chart(fig)
