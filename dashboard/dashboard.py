import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("day_data_bersih.csv")
hour_df = pd.read_csv("hour_data_bersih.csv")

# Konfigurasi layout
st.set_page_config(layout="wide")
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar filter bulan
st.sidebar.header("Filter Data")
month_filter = st.sidebar.selectbox("Pilih Bulan:", day_df["month"].unique())
filtered_data = day_df[day_df["month"] == month_filter]

# Visualisasi 1: Tren Penyewaan Sepeda Bulanan
st.subheader("Tren Penyewaan Sepeda Bulanan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=day_df["month"], y=day_df["total_rental"], marker="o", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# Visualisasi 2: Perbandingan Penyewaan pada Hari Kerja vs Hari Libur
st.subheader("Perbandingan Penyewaan: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=day_df["weekday"], y=day_df["total_rental"], hue=day_df["workingday"], ax=ax)
ax.set_xlabel("Hari")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# Visualisasi 3: Distribusi Penyewaan Sepeda berdasarkan Jam dalam Sehari
st.subheader("Distribusi Penyewaan Sepeda per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hour_df["hour"], y=hour_df["total_rental"], marker="o", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# Visualisasi 4: Perbandingan Penyewa Registered vs Casual
st.subheader("Perbandingan Penyewa Registered vs Casual")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=["Registered", "Casual"], y=[day_df["registered"].sum(), day_df["casual"].sum()], ax=ax)
ax.set_ylabel("Jumlah Penyewa")
st.pyplot(fig)

# Menampilkan data berdasarkan filter bulan
st.subheader("Data Penyewaan Berdasarkan Bulan yang Dipilih")
st.dataframe(filtered_data)
