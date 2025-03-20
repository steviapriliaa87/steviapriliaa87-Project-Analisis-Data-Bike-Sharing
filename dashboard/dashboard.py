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
              labels={'hour': 'Jam', 'total_rentals': 'Jumlah Penyewaan'},
              markers=True)
st.plotly_chart(fig)


#2.Penyewaan Berdasarkan bulan
day_df["month"] = pd.Categorical(day_df["month"], 
                                 categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
avg_rentals_by_month = day_df.groupby("month", observed=False)["total_rentals"].mean().reset_index()
avg_rentals_by_month["month"] = pd.Categorical(avg_rentals_by_month["month"], 
                                               categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
                                               ordered=True)
avg_rentals_by_month = avg_rentals_by_month.sort_values("month")
fig = px.bar(avg_rentals_by_month, 
             x='total_rentals', 
             y='month', 
             orientation='h', 
             labels={'total_rentals': 'Rata-rata Penyewaan', 'month': 'Bulan'},
             color_discrete_sequence=["royalblue"])  # Semua warna biru
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
st.plotly_chart(fig)


#3.Penyewaan Berdasarkan Hari
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

# **Buat visualisasi dengan Plotly (VERTIKAL)**
fig = px.bar(
    avg_rentals_by_weekday, 
    x="one_of_week",  # X-axis: Hari
    y="total_rentals",  # Y-axis: Rata-rata Penyewaan
    title="Rata-rata Penyewaan Sepeda dalam Seminggu",
    labels={"total_rentals": "Rata-rata Penyewaan", "one_of_week": "Hari"},
    color_discrete_sequence=["royalblue"],  # Warna batang
    hover_data={"total_rentals": ":,.0f", "one_of_week": True}  # Tooltip interaktif
)

# **Tampilkan grafik di Streamlit**
st.plotly_chart(fig)





#4.Penyewaan Berdasarkan Kondisi Cuaca
avg_rentals_by_weather = hour_df.groupby('weather_condition', observed=True)['total_rentals'].mean().reset_index()
weather_order = ["clear", "misty", "light rain/light snow", "bad weather"]
avg_rentals_by_weather["weather_condition"] = pd.Categorical(
    avg_rentals_by_weather["weather_condition"], categories=weather_order, ordered=True
)
avg_rentals_by_weather = avg_rentals_by_weather.sort_values("weather_condition")
palette = sns.color_palette("coolwarm", n_colors=len(avg_rentals_by_weather))
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=avg_rentals_by_weather,
    x="weather_condition",
    y="total_rentals",
    palette=palette,
    ax=ax
)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight="bold")
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.set_xticklabels(weather_order, rotation=30)
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)


