import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# -------------------------------
# KONFIGURASI SUPABASE
# -------------------------------
SUPABASE_URL = "https://ojwwyymjmeneoqlvgbes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qd3d5eW1qbWVuZW9xbHZnYmVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NjI5MzUsImV4cCI6MjA3ODUzODkzNX0.-6tdIlFBLrQe-8tcN2smNpscKdh4AAHtszc4rB0rV_k"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# KONFIGURASI HALAMAN
# -------------------------------
st.set_page_config(
    page_title="Luminous AI – Pengingat Tugas",
    page_icon="🌙",
    layout="centered",
)

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
body {background-color: #f5f7fa;}
.main {background-color: #ffffff; padding: 30px; border-radius: 20px;
box-shadow: 0px 4px 15px rgba(0,0,0,0.1);}
.stButton>button {background-color: #4F46E5; color: white; border-radius: 10px;
height: 3em; width: 100%; font-weight: bold; border: none; transition: 0.3s;}
.stButton>button:hover {background-color: #4338CA; transform: scale(1.02);}
h1, h2, h3 {text-align: center;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# DASHBOARD TANPA LOGIN
# -------------------------------
st.title("🌙 Luminous AI – Pengingat Tugas")
st.markdown("---")
st.header("🧠 Tambah Tugas Baru")

# -------------------------------
# INPUT FORM
# -------------------------------
nama = st.text_input("Nama Tugas", placeholder="Contoh: PR Matematika Bab 3")
pelajaran = st.text_input("Mata Pelajaran", placeholder="Contoh: Matematika")
deadline = st.date_input("Deadline")
kesulitan = st.selectbox("Tingkat Kesulitan", ["Mudah", "Normal", "Sulit"])

# -------------------------------
# TAMBAH DATA KE SUPABASE
# -------------------------------
if st.button("➕ Tambahin Tugas Disini!"):
    
    sisa_hari = (deadline - datetime.today().date()).days

    if sisa_hari <= 1 or kesulitan == "Sulit":
        prioritas = "Sulit"
    elif sisa_hari <= 3:
        prioritas = "Normal"
    else:
        prioritas = "Mudah"

    data = {
        "nama": nama,
        "pelajaran": pelajaran,
        "deadline": str(deadline),
        "kesulitan": kesulitan,
        "prioritas": prioritas
    }

    try:
        supabase.table("tasks").insert(data).execute()
        st.success("Yay! Tugas berhasil disimpan!")
        st.rerun()
    except Exception as e:
        st.error(f"Sorry! Gagal menyimpan tugas: {e}")

# -------------------------------
# TAMPILKAN DATA
# -------------------------------
st.markdown("---")
st.header("📋 Daftar-Daftar Tugas Kamu")

res = supabase.table("tasks").select("*").execute()
tasks = res.data

if tasks:
    df = pd.DataFrame(tasks)
    st.dataframe(df[["nama", "pelajaran", "deadline", "kesulitan", "prioritas"]])
else:
    st.info("Belum ada tugas yang ditambahin nih.")

# -------------------------------
# DELETE ALL
# -------------------------------
if st.button("🗑️ Hapus Semua Tugasnya?"):
    try:
        supabase.table("tasks").delete().neq("id", -1).execute()
        st.warning("Hore! Semua tugas telah dihapus.")
        st.rerun()
    except Exception as e:
        st.error(f"Yah! Gagal menghapus tugas: {e}")