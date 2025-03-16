import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("bike_data.csv")  # Gantilah dengan file yang sesuai

def plot_rentals_per_month():
    monthly_data = df.groupby("month")["total_rentals"].sum()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_data.index, y=monthly_data.values, palette="Blues")
    plt.xlabel("Bulan")
    plt.ylabel("Total Penyewaan")
    plt.title("Total Penyewaan Sepeda per Bulan")
    st.pyplot(plt)

def plot_rentals_per_day():
    daily_data = df.groupby("day_of_week")["total_rentals"].sum()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=daily_data.index, y=daily_data.values, palette="Greens")
    plt.xlabel("Hari")
    plt.ylabel("Total Penyewaan")
    plt.title("Total Penyewaan Sepeda per Hari")
    st.pyplot(plt)

def plot_rentals_per_hour():
    hourly_data = df.groupby("hour")["total_rentals"].sum()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=hourly_data.index, y=hourly_data.values, marker="o", color="red")
    plt.xlabel("Jam")
    plt.ylabel("Total Penyewaan")
    plt.title("Pola Penyewaan Sepeda per Jam")
    st.pyplot(plt)

def plot_registered_vs_casual():
    reg_vs_cas = df[["registered", "casual"]].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(reg_vs_cas, labels=["Registered", "Casual"], autopct="%1.1f%%", colors=["blue", "orange"])
    plt.title("Perbandingan Registered vs Casual Users")
    st.pyplot(plt)

def plot_rentals_by_weather():
    weather_data = df.groupby("weather")["total_rentals"].sum()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=weather_data.index, y=weather_data.values, palette="coolwarm")
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Total Penyewaan")
    plt.title("Total Penyewaan Sepeda berdasarkan Cuaca")
    st.pyplot(plt)

# Streamlit UI
st.title("Dashboard Penyewaan Sepeda")
st.sidebar.header("Pilihan Visualisasi")
option = st.sidebar.selectbox("Pilih Grafik:", 
    ["Penyewaan per Bulan", "Penyewaan per Hari", "Penyewaan per Jam", "Registered vs Casual", "Penyewaan berdasarkan Cuaca"])

if option == "Penyewaan per Bulan":
    plot_rentals_per_month()
elif option == "Penyewaan per Hari":
    plot_rentals_per_day()
elif option == "Penyewaan per Jam":
    plot_rentals_per_hour()
elif option == "Registered vs Casual":
    plot_registered_vs_casual()
elif option == "Penyewaan berdasarkan Cuaca":
    plot_rentals_by_weather()

st.sidebar.header("Filter Data")
season = st.sidebar.selectbox("Pilih Musim:", df["season"].unique())
filtered_data = df[df["season"] == season]
st.write(f"Menampilkan data untuk musim: {season}")
st.dataframe(filtered_data)
