import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

day_data_path = "../data/day.csv"
hour_data_path = "../data/hour.csv"

# Coba baca file
day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

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
rentals_by_hour = hour_df.groupby("hour", observed=True, as_index=False)["total_rentals"].mean()
print("Tabel Rata-rata Penyewaan Sepeda per Jam:")
display(rentals_by_hour)

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=rentals_by_hour,
    x="hour",
    y="total_rentals",
    marker="o",
    color="blue",
    linewidth=2
)

plt.title("Distribusi Rata-rata Penyewaan Sepeda per Jam", fontsize=14, fontweight="bold")
plt.xlabel("Jam", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.xticks(range(0, 24))
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()

# 2. Rata-rata penyewaan sepeda berdasarkan bulan
avg_rentals_by_month = day_df.groupby("month", observed=True)["total_rentals"].mean().reset_index()
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
avg_rentals_by_month["month"] = pd.Categorical(avg_rentals_by_month["month"], categories=month_order, ordered=True)
avg_rentals_by_month = avg_rentals_by_month.sort_values("month")

print("Tabel Rata-rata Penyewaan Sepeda Berdasarkan Bulan:")
display(avg_rentals_by_month)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=avg_rentals_by_month,
    y="month",
    x="total_rentals",
    color="seagreen",
    orient="h"
)

plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Bulan", fontsize=14, fontweight="bold")
plt.ylabel("Bulan", fontsize=12)
plt.xlabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.show()

# 3. Rata-rata penyewaan berdasarkan hari dalam seminggu
avg_rentals_by_weekday = (
    day_df.groupby("one_of_week", observed=False)["total_rentals"]
    .mean()
    .reset_index()
)

order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
avg_rentals_by_weekday["one_of_week"] = pd.Categorical(
    avg_rentals_by_weekday["one_of_week"], categories=order, ordered=True
)
avg_rentals_by_weekday = avg_rentals_by_weekday.sort_values("one_of_week")
print("Tabel Rata-rata Penyewaan Sepeda dalam Seminggu:")
display(avg_rentals_by_weekday)

plt.figure(figsize=(10, 5))
sns.barplot(
    data=avg_rentals_by_weekday,
    x="one_of_week",
    y="total_rentals",
    color="seagreen",
)
plt.title("Rata-rata Penyewaan Sepeda dalam Seminggu", fontsize=14, fontweight="bold")
plt.xlabel("Hari", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()

# 4. Rata-rata penyewaan berdasarkan cuaca
avg_rentals_by_weather = hour_df.groupby('weather_condition', observed=True)['total_rentals'].mean().reset_index()
print(avg_rentals_by_weather)

palette = sns.color_palette("coolwarm", n_colors=len(avg_rentals_by_weather))
plt.figure(figsize=(8, 5))
ax = sns.barplot(
    data=avg_rentals_by_weather,
    x="weather_condition",
    y="total_rentals",
    hue="weather_condition",
    palette=palette,
    legend=False
)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight="bold")
plt.xlabel("Kondisi Cuaca", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.xticks(rotation=30)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()

# 5. Perbandingan Penyewa Registered vs Casual
plt.rcParams['font.family'] = 'DejaVu Sans'
total_registered = hour_df['registered_rentals'].sum()
total_casual = hour_df['casual_rentals'].sum()
labels = [f'Registered ({total_registered})', f'Casual ({total_casual})']
sizes = [total_registered, total_casual]
colors = ['darkblue', 'lightblue']

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'white'})
plt.title('Perbandingan Penyewa Registered vs Casual')
plt.show()

# 6. Perbandingan total penyewa antara hari kerja vs hari libur
rentals_by_day_type = day_df.groupby("working_day", observed=True)["total_rentals"].sum().reset_index()
rentals_by_day_type["working_day"] = rentals_by_day_type["working_day"].map({0: "Hari Libur", 1: "Hari Kerja"})

color_mapping = {"Hari Libur": "red", "Hari Kerja": "blue"}

plt.figure(figsize=(8, 5))
ax = sns.barplot(
    data=rentals_by_day_type,
    x="working_day",
    y="total_rentals",
    hue="working_day",
    palette=color_mapping,
    legend=False
)

for p in ax.patches:
    ax.annotate(f'{int(p.get_height()):,}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.title("Perbandingan Total Penyewaan antara Hari Kerja vs Hari Libur", fontsize=14, fontweight="bold")
plt.xlabel("Jenis Hari", fontsize=12)
plt.ylabel("Total Penyewaan Sepeda", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.show()

# 7. Perbandingan Tren Penyewaan Sepeda: 2011 vs 2012
monthly_trend = day_df.groupby(["year", "month"], observed=True)["total_rentals"].sum().reset_index()

plt.figure(figsize=(8, 5))
plt.plot(
    monthly_trend[monthly_trend["year"] == 2011]["month"],
    monthly_trend[monthly_trend["year"] == 2011]["total_rentals"],
    marker="o", linestyle="-", color="blue", label="2011"
)

plt.plot(
    monthly_trend[monthly_trend["year"] == 2012]["month"],
    monthly_trend[monthly_trend["year"] == 2012]["total_rentals"],
    marker="s", linestyle="-", color="red", label="2012"
)

plt.title("Perbandingan Tren Penyewaan Sepeda: 2011 vs 2012", fontsize=14, fontweight="bold")
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Total Penyewaan Sepeda", fontsize=12)
plt.xticks(range(1, 13), ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
plt.legend(title="Tahun")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()
