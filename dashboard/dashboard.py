import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Pastikan path file benar
data_path = "data"
day_file = os.path.join(data_path, "day_data_bersih.csv")
hour_file = os.path.join(data_path, "hour_data_bersih.csv")

# Load dataset
day_df = pd.read_csv(day_file)
hour_df = pd.read_csv(hour_file)

# Dashboard Streamlit
st.title("Dashboard Analisis Data Bike Sharing")

# Sidebar untuk eksplorasi data
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim:", day_df['season'].unique())
filtered_data = day_df[day_df['season'] == selected_season]

# Visualisasi 1: Jumlah peminjaman sepeda per musim
st.subheader("Jumlah Peminjaman Sepeda per Musim")
plt.figure(figsize=(8, 5))
sns.barplot(x='season', y='count', data=day_df, palette='coolwarm')
st.pyplot(plt)

# Visualisasi 2: Tren peminjaman sepeda berdasarkan bulan
st.subheader("Tren Peminjaman Sepeda per Bulan")
plt.figure(figsize=(10, 5))
sns.lineplot(x='month', y='count', data=day_df, marker='o', color='b')
st.pyplot(plt)

# Visualisasi 3: Pengaruh suhu terhadap peminjaman sepeda
st.subheader("Pengaruh Suhu terhadap Peminjaman Sepeda")
plt.figure(figsize=(8, 5))
sns.scatterplot(x='temp', y='count', data=day_df, alpha=0.6, color='g')
st.pyplot(plt)

# Visualisasi 4: Distribusi peminjaman sepeda berdasarkan jam
st.subheader("Distribusi Peminjaman Sepeda per Jam")
plt.figure(figsize=(10, 5))
sns.boxplot(x='hour', y='count', data=hour_df, palette='viridis')
st.pyplot(plt)

# Interaktif: Menampilkan data berdasarkan filter
st.subheader("Data Berdasarkan Filter")
st.write(filtered_data.head())

st.write("Dashboard ini dibuat untuk menganalisis data peminjaman sepeda berdasarkan musim, bulan, suhu, dan waktu harian.")
