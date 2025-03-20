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
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_season = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)
selected_customer_type = st.sidebar.radio("Pilih Jenis Pelanggan", ["Semua", "Registered", "Casual"], index=0)

# Filter dataset sesuai pilihan
df_filtered = day_df[
    (day_df['date'].dt.year.isin(selected_year)) &
    (day_df['season'].isin(selected_season)) &
    (day_df['month'].isin(selected_month))
]

if selected_day_type == "Hari Kerja":
    df_filtered = df_filtered[df_filtered['working_day'] == 1]
elif selected_day_type == "Libur":
    df_filtered = df_filtered[df_filtered['working_day'] == 0]

# Filter berdasarkan jenis pelanggan
if selected_customer_type == "Registered":
    df_filtered["total_rentals"] = df_filtered["registered_rentals"]
elif selected_customer_type == "Casual":
    df_filtered["total_rentals"] = df_filtered["casual_rentals"]

st.title("🚲 Dashboard Penyewaan Sepeda")
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered['total_rentals'].sum())
col2.metric("Rata-rata Harian", round(df_filtered['total_rentals'].mean(), 2))
col3.metric("Penyewaan Tertinggi", df_filtered['total_rentals'].max())

# Penyewaan Berdasarkan Bulan
day_df["month"] = pd.Categorical(day_df["month"], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
avg_rentals_by_month = df_filtered.groupby("month", observed=False)["total_rentals"].mean().reset_index()
avg_rentals_by_month["month"] = pd.Categorical(avg_rentals_by_month["month"], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
avg_rentals_by_month = avg_rentals_by_month.sort_values("month")
fig = px.bar(avg_rentals_by_month, x='total_rentals', y='month', orientation='h', labels={'total_rentals': 'Rata-rata Penyewaan', 'month': 'Bulan'}, color_discrete_sequence=["royalblue"])
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
st.plotly_chart(fig)

# Penyewaan Berdasarkan Tahun
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

# Penyewaan Berdasarkan jenis Penyewa 
total_registered = df_filtered['registered_rentals'].sum()
total_casual = df_filtered['casual_rentals'].sum()
data = pd.DataFrame({"Kategori": ["Registered", "Casual"], "Jumlah": [total_registered, total_casual]})

fig = px.pie(data, names="Kategori", values="Jumlah", color="Kategori", color_discrete_map={"Registered": "darkblue", "Casual": "lightblue"}, title="Perbandingan Penyewa Registered vs Casual", hole=0.3)

fig.update_traces(textinfo="none")

st.plotly_chart(fig, use_container_width=True)
