#########################################
# DASHBOARD ANALITIK PENJUALAN UMKM
#########################################

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
import os

# ==============================
# LOAD GAMBAR BASE64
# ==============================
@st.cache_data(show_spinner=False)
def load_image_base64(path):
    """
    Membaca gambar dan mengubahnya menjadi base64.
    Mengembalikan None jika file tidak ditemukan atau rusak.
    """
    if os.path.exists(path):
        try:
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            st.warning(f"⚠️ Tidak bisa membaca gambar {path}")
    return None

# ==============================
# GLOBAL CHART THEME FUNCTION
# ==============================
def apply_chart_theme(fig):
    """
    Menerapkan tema visual gelap untuk semua chart Plotly.
    """
    fig.update_layout(
        font_color="white",
        title_font=dict(size=20, family="Arial", color="white"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#555",
            zeroline=False,
            color="white",
            title_font=dict(color="white")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#555",
            zeroline=False,
            color="white",
            title_font=dict(color="white")
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# ==============================
# APPLY CHART BACKGROUND WITH IMAGE
# ==============================
def apply_chart_background_with_image(fig, img_base64):
    """
    Menambahkan background gambar ke chart bila tersedia.
    """
    if img_base64:
        fig.update_layout(
            images=[dict(
                source=f"data:image/png;base64,{img_base64}",
                xref="paper", yref="paper",
                x=0, y=1,
                sizex=1, sizey=1,
                sizing="stretch",
                opacity=0.22,
                layer="below"
            )]
        )
    return fig

# ==============================
# APPLY BACKGROUND HALAMAN
# ==============================
bg_base64 = load_image_base64("background.png")
if bg_base64:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bg_base64}");
                background-size: cover;
                background-repeat: repeat;
                background-attachment: fixed;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==============================
# JUDUL DASHBOARD
# ==============================
st.markdown(
    "<h1 style='font-size:26px; text-align:center; margin-bottom:20px; color:white;'>Dashboard Analitik Penjualan UMKM</h1>",
    unsafe_allow_html=True
)

# ==============================
# MENU SIDEBAR
# ==============================
menu = st.sidebar.radio("Pilih Halaman", ["Dashboard", "Anggota Kelompok"])

# ==============================
# HALAMAN ANGGOTA
# ==============================
if menu == "Anggota Kelompok":
    logo_b64 = load_image_base64("logo.png")

    anggota = [
        "Reyhan Abi Sukoco",
        "Robi Armasta Wijaya",
        "Ardelia Syifa",
        "Septiani",
        "Athfal Fahlefi",
        "Arizal Anshori",
        "Galih Setyaji"
    ]

    # Membuat tabel anggota
    tabel_html = "<table style='border-collapse:collapse;'>"
    tabel_html += "<tr style='background-color:#333; color:white;'><th style='padding:5px 10px;'>Nama Anggota</th></tr>"
    for nama in anggota:
        tabel_html += f"<tr><td style='padding:4px 10px; color:white;'>{nama}</td></tr>"
    tabel_html += "</table>"

    if logo_b64:
        st.markdown(
            f"""
            <div style='display:flex; align-items:flex-start; justify-content:center; gap:50px;'>
                <div style='flex:0 0 auto; margin-top:50px;'>
                    <img src="data:image/png;base64,{logo_b64}" width="350" style='display:block;'>
                </div>
                <div style='flex:0 0 auto;'>
                    <h2 style='color:white; margin:0 0 10px 0;'>Kelompok 4 - Teknik Elektro</h2>
                    {tabel_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Logo tidak ditemukan!")

# ==============================
# HALAMAN DASHBOARD
# ==============================
elif menu == "Dashboard":

    @st.cache_data(show_spinner=False)
    def load_csv(file):
        """Membaca CSV dengan caching."""
        return pd.read_csv(file, sep=";")

    if not os.path.exists("data_penjualan.csv"):
        st.error("⚠️ File data_penjualan.csv tidak ditemukan!")
        st.stop()

    data = load_csv("data_penjualan.csv")

    kolom_wajib = {"Produk", "Bulan", "Penjualan", "Keuntungan", "Kategori", "Rating"}
    if not kolom_wajib.issubset(data.columns):
        st.error("⚠️ Format CSV tidak sesuai!")
        st.stop()

    # Konversi dan sorting bulan
    data["Rating"] = data["Rating"].astype(str).str.replace(",", ".", regex=False).astype(float)
    data = data.sort_values(by="Bulan")

    produk = st.sidebar.selectbox("Pilih Produk:", data["Produk"].unique())
    data_filter = data[data["Produk"] == produk]

    if data_filter.empty:
        st.warning("Tidak ada data produk ini.")
        st.stop()

    # ==============================
    # GRAFIK INTERAKTIF (PLOTLY)
    # ==============================
    for col, title in [("Penjualan", "Tren Penjualan"), ("Keuntungan", "Tren Keuntungan")]:
        fig = px.line(data_filter, x="Bulan", y=col, markers=True, title=f"{title} {produk}")
        st.plotly_chart(apply_chart_background_with_image(apply_chart_theme(fig), bg_base64))

    fig3 = px.bar(data, x="Bulan", y="Penjualan", color="Produk", title="Perbandingan Penjualan per Produk")
    st.plotly_chart(apply_chart_background_with_image(apply_chart_theme(fig3), bg_base64))

    fig4 = px.pie(data, names="Kategori", values="Penjualan", title="Distribusi Penjualan per Kategori")
    st.plotly_chart(apply_chart_background_with_image(apply_chart_theme(fig4), bg_base64))

    # ==============================
    # GRAFIK STATIS (SEABORN)
    # ==============================
    st.markdown("<h3 style='color:white;'>Grafik Statis Seaborn</h3>", unsafe_allow_html=True)
    fig_sns, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=data_filter, x="Bulan", y="Penjualan", marker="o", ax=ax, linewidth=1.2)
    ax.set_title(f"Tren Penjualan {produk} (Seaborn)", color="white")
    ax.set_xlabel("Bulan", color="white")
    ax.set_ylabel("Penjualan", color="white")
    ax.tick_params(colors='white')
    fig_sns.patch.set_facecolor('#222')
    st.pyplot(fig_sns)

    # ==============================
    # INSIGHT ANALITIK DENGAN NUMPY
    # ==============================
    total_penjualan = np.sum(data_filter["Penjualan"])
    total_keuntungan = np.sum(data_filter["Keuntungan"])
    bulan_tertinggi = data_filter.loc[data_filter["Penjualan"].idxmax(), "Bulan"]
    bulan_keuntungan = data_filter.loc[data_filter["Keuntungan"].idxmax(), "Bulan"]

    pertumbuhan = data_filter.groupby("Produk")["Penjualan"].agg(["first", "last"])
    pertumbuhan["growth"] = pertumbuhan["last"] - pertumbuhan["first"]
    produk_tertinggi = pertumbuhan["growth"].idxmax()
    nilai_pertumbuhan = pertumbuhan["growth"].max()

    kategori_populer = data_filter.groupby("Kategori")["Penjualan"].sum().idxmax()
    total_kategori = data_filter.groupby("Kategori")["Penjualan"].sum().max()

    # ==============================
    # STORYTELLING INSIGHT
    # ==============================
    st.subheader("Insight Cerita Data")

    data_filter_sorted = data_filter.sort_values("Bulan")
    data_filter_sorted["Change"] = data_filter_sorted["Penjualan"].diff().fillna(0)

    why_text = (
        "Peningkatan ini kemungkinan karena minat pasar yang meningkat atau strategi promosi yang efektif."
        if data_filter_sorted["Change"].iloc[-1] > 0 else
        "Penurunan ini mungkin dipengaruhi oleh permintaan yang menurun atau persaingan meningkat."
        if data_filter_sorted["Change"].iloc[-1] < 0 else
        "Penjualan relatif stabil dibanding bulan sebelumnya."
    )

    st.write(
        f"**What:** Produk **{produk}** menunjukkan tren penjualan yang positif. "
        f"Penjualan tertinggi terjadi pada bulan **{bulan_tertinggi}** dengan total **{total_penjualan} unit**, "
        f"menghasilkan keuntungan sebesar **{total_keuntungan}**.\n\n"
        f"**Why:** {why_text}\n\n"
        f"**So what:** Produk **{produk_tertinggi}** memiliki pertumbuhan penjualan tertinggi (**{nilai_pertumbuhan} unit**), "
        f"sementara kategori **{kategori_populer}** paling diminati pelanggan (**{total_kategori} unit**). "
        f"Fokus pada produk dan kategori ini dapat membantu meningkatkan penjualan dan keuntungan lebih lanjut."
    )

    # ==============================
    # TABEL INSIGHT DETAIL
    # ==============================
    st.markdown(f"""
    <table style='width:60%; margin:auto; border-collapse:collapse;'>
        <tr style='background-color:#333; color:white;'>
            <th style='padding:10px; border:1px solid #555; text-align:center;' colspan="2">
                Insight Analitik — {produk}
            </th>
        </tr>
        <tr><td style='padding:8px;'>Total Penjualan</td><td>{total_penjualan} unit</td></tr>
        <tr><td style='padding:8px;'>Total Keuntungan</td><td>{total_keuntungan}</td></tr>
        <tr><td style='padding:8px;'>Bulan Tertinggi</td><td>{bulan_tertinggi}</td></tr>
        <tr><td style='padding:8px;'>Bulan Paling Menguntungkan</td><td>{bulan_keuntungan}</td></tr>
        <tr><td style='padding:8px;'>Produk Pertumbuhan Tertinggi</td><td>{produk_tertinggi} (naik {nilai_pertumbuhan})</td></tr>
        <tr><td style='padding:8px;'>Kategori Paling Populer</td><td>{kategori_populer} ({total_kategori} unit)</td></tr>
    </table><br>
    """, unsafe_allow_html=True)
