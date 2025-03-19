import os
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# Mendapatkan path absolut ke folder 'dashboard'
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path ke file CSV
day_data_path = os.path.join(script_dir, "day.csv")
hour_data_path = os.path.join(script_dir, "hour.csv")

# 🔍 Debugging: Cek apakah path-nya benar
st.write(f"Path ke day.csv: {day_data_path}")
st.write(f"Path ke hour.csv: {hour_data_path}")

# Coba baca file
try:
    day_df = pd.read_csv(day_data_path)
    hour_df = pd.read_csv(hour_data_path)
    st.write("✅ File berhasil dibaca!")
except FileNotFoundError:
    st.error("❌ File tidak ditemukan! Cek kembali lokasi file di dalam repository GitHub.")

# Konversi kolom date ke datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Sidebar filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect("Pilih Tahun", day_df['date'].dt.year.unique(), default=day_df['date'].dt.year.unique())
selected_month = st.sidebar.multiselect("Pilih Bulan", day_df['month'].unique(), default=day_df['month'].unique())
selected_day_type = st.sidebar.radio("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Libur"], index=0)

# Apply filters
df_filtered = day_df[(day_df['date'].dt.year.isin(selected_year)) & (day_df['month'].isin(selected_month))]
if selected_day_type == "Hari Kerja":
    df_filtered = df_filtered[df_filtered['workingday'] == 1]
elif selected_day_type == "Libur":
    df_filtered = df_filtered[df_filtered['workingday'] == 0]

# Dashboard Title
st.title("Dashboard Penyewaan Sepeda")

# 1. Rata-rata penyewaan berdasarkan jam
st.subheader("Distribusi Rata-rata Penyewaan Sepeda per Jam")
rentals_by_hour = hour_df.groupby("hour", as_index=False)["total_rentals"].mean()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=rentals_by_hour, x="hour", y="total_rentals", marker="o", color="blue", linewidth=2, ax=ax)
ax.set_title("Distribusi Rata-rata Penyewaan Sepeda per Jam", fontsize=14, fontweight="bold")
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

# 2. Rata-rata penyewaan sepeda berdasarkan bulan
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
avg_rentals_by_month = day_df.groupby("month", as_index=False)["total_rentals"].mean()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=avg_rentals_by_month, x="month", y="total_rentals", color="seagreen", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Bulan", fontsize=14, fontweight="bold")
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

# 3. Rata-rata penyewaan berdasarkan hari dalam seminggu
st.subheader("Rata-rata Penyewaan Sepeda dalam Seminggu")
avg_rentals_by_weekday = day_df.groupby("one_of_week", as_index=False)["total_rentals"].mean()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=avg_rentals_by_weekday, x="one_of_week", y="total_rentals", color="seagreen", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda dalam Seminggu", fontsize=14, fontweight="bold")
ax.set_xlabel("Hari", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

# 4. Rata-rata penyewaan berdasarkan cuaca
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
avg_rentals_by_weather = hour_df.groupby('weather_condition', as_index=False)['total_rentals'].mean()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_rentals_by_weather, x="weather_condition", y="total_rentals", palette="coolwarm", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight="bold")
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

# 5. Perbandingan Penyewa Registered vs Casual
st.subheader("Perbandingan Penyewa Registered vs Casual")
total_registered = hour_df['registered_rentals'].sum()
total_casual = hour_df['casual_rentals'].sum()

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie([total_registered, total_casual], labels=["Registered", "Casual"], autopct='%1.1f%%', colors=['darkblue', 'lightblue'])
ax.set_title('Perbandingan Penyewa Registered vs Casual')
st.pyplot(fig)

# 6. Perbandingan total penyewa antara hari kerja vs hari libur
st.subheader("Perbandingan Total Penyewaan antara Hari Kerja vs Hari Libur")
rentals_by_day_type = day_df.groupby("working_day", as_index=False)["total_rentals"].sum()
rentals_by_day_type["working_day"] = rentals_by_day_type["working_day"].map({0: "Hari Libur", 1: "Hari Kerja"})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=rentals_by_day_type, x="working_day", y="total_rentals", palette={"Hari Libur": "red", "Hari Kerja": "blue"}, ax=ax)
ax.set_title("Perbandingan Total Penyewaan antara Hari Kerja vs Hari Libur", fontsize=14, fontweight="bold")
ax.set_xlabel("Jenis Hari", fontsize=12)
ax.set_ylabel("Total Penyewaan Sepeda", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig)

# 7 
month_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
day_df["month"] = pd.Categorical(day_df["month"], categories=month_order, ordered=True)

# Hitung total penyewaan per bulan dan tahun
monthly_trend = day_df.groupby(["year", "month"], observed=True)["total_rentals"].sum().reset_index()
monthly_trend = monthly_trend.sort_values(by=["year", "month"])  # Urutkan agar tidak acak

# Buat figure dan axis
fig, ax = plt.subplots(figsize=(8, 5))

# Plot tahun 2011
ax.plot(
    monthly_trend[monthly_trend["year"] == 2011]["month"],
    monthly_trend[monthly_trend["year"] == 2011]["total_rentals"],
    marker="o", linestyle="-", color="blue", markersize=6, linewidth=2, label="2011"
)

# Plot tahun 2012
ax.plot(
    monthly_trend[monthly_trend["year"] == 2012]["month"],
    monthly_trend[monthly_trend["year"] == 2012]["total_rentals"],
    marker="s", linestyle="-", color="red", markersize=6, linewidth=2, label="2012"
)

# Atur tampilan
ax.set_title("Perbandingan Tren Penyewaan Sepeda: 2011 vs 2012", fontsize=14, fontweight="bold")
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Penyewaan Sepeda", fontsize=12)
ax.set_xticks(range(len(month_order)))  # Pastikan jumlah xticks sesuai jumlah bulan
ax.set_xticklabels(month_order)  # Pakai nama bulan
ax.legend(title="Tahun", fontsize=10, frameon=True, loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()

# Tampilkan di Streamlit
st.pyplot(fig)
