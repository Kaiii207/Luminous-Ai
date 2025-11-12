import streamlit as st
import pandas as pd
from datetime import datetime
import os
from supabase import create_client, Client

SUPABASE_URL = "https://ojwwyymjmeneoqlvgbes.supabase.co"   # Ganti dengan URL kamu
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qd3d5eW1qbWVuZW9xbHZnYmVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NjI5MzUsImV4cCI6MjA3ODUzODkzNX0.-6tdIlFBLrQe-8tcN2smNpscKdh4AAHtszc4rB0rV_k"                        # Ganti dengan Anon key kamu
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Luminous AI – Pengingat Tugas",
    page_icon="moon.png",
    layout="centered"
)

# --- Gaya CSS Kustom ---
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: scale(1.02);
    }
    h1, h2, h3, h4 {
        color: #1e1e2f;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Judul Aplikasi ---
st.title("🤖 Luminous AI – Pengingat Tugas")
st.write("✨ Kelola dan pantau semua tugasmu dengan bantuan AI yang cerdas dan rapi!")

# --- File Penyimpanan ---
file_path = "data_tugas.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=["Nama", "Pelajaran", "Deadline", "Kesulitan", "Prioritas"])

# --- Form Input ---
with st.container():
    st.header("🧠 Tambah Tugas Baru")
    nama = st.text_input("Nama Tugas", placeholder="Contoh: PR Matematika Bab 3 atau Menjemput Barang")
    pelajaran = st.text_input("Mata Pelajaran", placeholder="Contoh: Matematika atau Hari senin mengambil barang")
    deadline = st.date_input("Deadline")
    kesulitan = st.selectbox("Tingkat Kesulitan", ["Rendah", "Sedang", "Tinggi"])

if st.button("➕ Tambah Tugas"):
    sisa_hari = (deadline - datetime.today().date()).days
    if sisa_hari <= 2 or kesulitan == "Tinggi":
        prioritas = "Tinggi"
    elif sisa_hari <= 3:
        prioritas = "Sedang"
    else:
        prioritas = "Rendah"

    data = {
        "nama": nama,
        "pelajaran": pelajaran,
        "deadline": str(deadline),
        "kesulitan": kesulitan,
        "prioritas": prioritas
    }
    supabase.table("tasks").insert(data).execute()
    st.success("✅ Tugas berhasil disimpan!")

# Ambil semua data
tasks = supabase.table("tasks").select("*").execute().data
st.dataframe(tasks)

st.markdown("---")

# --- Tabel Daftar Tugas ---
st.header("📋 Daftar Tugas Kamu")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada tugas yang ditambahkan.")

# --- Tombol Hapus Semua ---
if st.button("🗑️ Hapus Semua Tugas"):
    df = pd.DataFrame(columns=["Nama", "Pelajaran", "Deadline", "Kesulitan", "Prioritas"])
    df.to_csv(file_path, index=False)
    st.warning("Semua tugas berhasil dihapus.")