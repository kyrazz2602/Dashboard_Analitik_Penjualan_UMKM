# Dashboard Analitik Penjualan UMKM

Aplikasi dashboard interaktif untuk menganalisis data penjualan UMKM (Usaha Mikro Kecil Menengah) dengan visualisasi yang informatif dan menarik.

## 🚀 Fitur

- Visualisasi tren penjualan dan keuntungan
- Perbandingan penjualan antar produk
- Analisis distribusi penjualan per kategori
- Grafik interaktif menggunakan Plotly
- Visualisasi statis dengan Seaborn
- Insight analitik otomatis
- Tampilan responsif dengan tema gelap
- Halaman informasi tim pengembang

## 📋 Persyaratan Sistem

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- Seaborn
- Matplotlib
- Numpy
- Pillow

## 🛠️ Instalasi

1. Clone repository ini:
   ```bash
   git clone [url-repository]
   ```

2. Buat dan aktifkan virtual environment (disarankan):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

## 🚀 Cara Menjalankan

1. Pastikan file `data_penjualan.csv` sudah tersedia di direktori yang sama dengan `app_dashboard.py`
2. Jalankan aplikasi dengan perintah:
   ```bash
   streamlit run app_dashboard.py
   ```
3. Buka browser dan akses `http://localhost:8501`

## 📊 Format Data

File `data_penjualan.csv` harus memiliki format berikut:
- `Produk` (string): Nama produk
- `Bulan` (string): Periode waktu (contoh: "Januari 2023")
- `Penjualan` (numeric): Jumlah penjualan
- `Keuntungan` (numeric): Jumlah keuntungan
- `Kategori` (string): Kategori produk
- `Rating` (numeric): Rating produk (0-5)

## 🎨 Tema

Aplikasi menggunakan tema gelap dengan latar belakang yang dapat disesuaikan. Pastikan file `background.png` dan `logo.png` tersedia di direktori yang sama untuk tampilan yang optimal.

## 👥 Anggota Tim

- Reyhan Abi Sukoco
- Robi Armasta Wijaya
- Ardelia Syifa
- Septiani
- Athfal Fahlefi
- Arizal Anshori
- Galih Setyaji
