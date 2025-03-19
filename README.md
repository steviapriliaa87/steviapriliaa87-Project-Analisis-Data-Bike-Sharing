# 🎯 Submission Dicoding: *Analisis Data dengan Python*

## 🚀 Preview
![Bike Sharing Dashboard Streamlit Preview](https://github.com/steviapriliaa87/steviapriliaa87-Project-Analisis-Data-Bike-Sharing/blob/639d9c804ee159b333f1d48e04c6db2a3402aa16/preview/preview%201.png)

---

## 📊 Project Analisis Data

Selamat datang di repository *Project Analisis Data Bike Sharing*! Proyek ini dikembangkan menggunakan **Google Colab** untuk analisis data dan **Streamlit** <img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" alt="Streamlit logo" width="20"> untuk membangun dashboard interaktif.

---

## 📚 Deskripsi

Proyek ini bertujuan untuk menganalisis *Bike Sharing Dataset* guna mendapatkan wawasan mendalam mengenai pola penggunaan sepeda. Dengan eksplorasi dan visualisasi data, proyek ini diharapkan dapat:
- Mengidentifikasi tren penyewaan sepeda.
- Menganalisis faktor yang memengaruhi jumlah penyewaan.
- Memberikan informasi berharga untuk pengambilan keputusan berbasis data.

---

## 🗂️ Struktur Direktori

- **dashboard/** → Berisi file `dashboard.py` untuk membangun dashboard dengan Streamlit.
- **data/** → Memuat data mentah dan bersih dalam format `.csv`.
- **preview/** → Cuplikan visualisasi dashboard.
- **notebook.ipynb** → Notebook analisis data lengkap.
- **requirements.txt** → Daftar library yang digunakan.
- **url.txt** → Tautan menuju dashboard yang sudah di-deploy.

---

## ⚙️ Instalasi

1. **Clone repository** ini ke komputer lokal Anda:

   ```bash
   git clone https://github.com/steviapriliaa87/Project-Analisis-Data-Bike-Sharing.git
   ```

2. **Setup Virtual Environment** (disarankan untuk menjaga isolasi library):

   ```bash
   # Membuat virtual environment
   python -m venv env

   # Mengaktifkan virtual environment
   # Windows
   .\env\Scripts\activate
   # Mac/Linux
   source env/bin/activate
   ```

3. **Install library** yang dibutuhkan menggunakan `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## 📊 Menjalankan Dashboard

Untuk melihat visualisasi interaktif dari hasil analisis data:

1. Pastikan Anda sudah berada di direktori utama proyek setelah clone repository.
2. Pastikan folder `data/` tetap berada di lokasi yang sama seperti saat di-clone.
3. Jalankan Streamlit:

   ```bash
   streamlit run dashboard/dashboard.py
   ```

📌 **Catatan:**
Pastikan file `dashboard.py` menggunakan path relatif yang benar agar dataset bisa diakses:

```python
import pandas as pd

data_day = pd.read_csv("../data/day_data_bersih.csv")
data_hour = pd.read_csv("../data/hour_data_bersih.csv")
```

---

## 🔗 Penggunaan

Jika ingin langsung melihat hasil akhirnya, bisa kunjungi [Dashboard Penyewaan Sepeda🚲](https://dashboardbikeanalysis.streamlit.app/)

---

## 🔍 Troubleshooting
Jika dashboard mengalami error karena file data tidak ditemukan, periksa kembali struktur folder:

```
/project-root
│── dashboard/
│   ├── dashboard.py
│── data/
│   ├── day_data_bersih.csv
│   ├── hour_data_bersih.csv
```

**Solusi:**
- ✅ Pastikan file CSV berada di dalam folder `data/`, bukan di folder lain.
- ✅ Periksa apakah path relatif di `dashboard.py` sudah sesuai (`../data/nama_file.csv`).
- ✅ Jika error tetap terjadi, coba jalankan perintah berikut untuk melihat isi folder:

   ```bash
   ls -R  # Untuk Linux/Mac
   dir /s # Untuk Windows
   ```

---

##❓ Bantuan
Jika Anda memiliki pertanyaan, saran, atau menemukan masalah, silakan ajukan melalui GitHub Issues.

---

✨ Terima kasih telah mengunjungi proyek ini! Semoga bermanfaat. ✨

