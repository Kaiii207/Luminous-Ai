import streamlit as st
import pandas as pd
from datetime import datetime
import os
from supabase import create_client, Client

# --- Konfigurasi Supabase ---
SUPABASE_URL = "https://<YOUR_PROJECT>.supabase.co"   # ganti dengan URL dari Supabase Settings > API
SUPABASE_KEY = "<YOUR_ANON_KEY>"                      # ganti dengan anon public key dari Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Luminous AI – Pengingat Tugas",
    page_icon="🌙",
    layout="centered"
)

# --- CSS ---
st.markdown("""
<style>
body {background-color: #f5f7fa;}
.main {background-color: #ffffff; padding: 30px; border-radius: 20px;
box-shadow: 0px 4px 15px rgba(0,0,0,0.1);}
.stButton>button {background-color: #4F46E5; color: white; border-radius: 10px;
height: 3em; width: 100%; font-weight: bold; border: none; transition: 0.3s;}
.stButton>button:hover {background-color: #4338CA; transform: scale(1.02);}
h1, h2, h3, h4 {color: #1e1e2f; text-align: center;}
</style>
""", unsafe_allow_html=True)

# --- Login Section ---
st.title("🔐 Luminous AI – Login / Register")

if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            try:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state["user"] = user.user
                st.success(f"Berhasil login sebagai {email}")
                st.rerun()
            except Exception as e:
                st.error("Login gagal. Periksa email atau password.")
    with col2:
        if st.button("Daftar Akun"):
            try:
                supabase.auth.sign_up({"email": email, "password": password})
                st.success("Akun berhasil dibuat! Silakan login.")
            except Exception as e:
                st.error(f"Gagal daftar: {e}")

    st.stop()

# --- Tombol Logout ---
if st.button("Logout"):
    st.session_state["user"] = None
    st.success("Berhasil logout.")
    st.rerun()

st.markdown("---")
st.header("🧠 Tambah Tugas Baru")

# --- Input Form ---
nama = st.text_input("Nama Tugas", placeholder="Contoh: PR Matematika Bab 3")
pelajaran = st.text_input("Mata Pelajaran", placeholder="Contoh: Matematika")
deadline = st.date_input("Deadline")
kesulitan = st.selectbox("Tingkat Kesulitan", ["Rendah", "Sedang", "Tinggi"])

# --- Tambah Tugas ---
if st.button("➕ Tambah Tugas"):
    try:
        sisa_hari = (deadline - datetime.today().date()).days
        if sisa_hari <= 1 or kesulitan == "Tinggi":
            prioritas = "Tinggi"
        elif sisa_hari <= 3:
            prioritas = "Sedang"
        else:
            prioritas = "Rendah"

        data = {
            "user_id": st.session_state["user"].id,
            "nama": nama,
            "pelajaran": pelajaran,
            "deadline": str(deadline),
            "kesulitan": kesulitan,
            "prioritas": prioritas
        }

        supabase.table("tasks").insert(data).execute()
        st.success("✅ Tugas berhasil disimpan!")
        st.rerun()
    except Exception as e:
        st.error(f"Gagal menambah tugas: {e}")

st.markdown("---")

# --- Tampilkan Daftar Tugas ---
st.header("📋 Daftar Tugas Kamu")

try:
    user_id = st.session_state["user"].id
    response = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    tasks = response.data

    if tasks and len(tasks) > 0:
        df = pd.DataFrame(tasks)
        st.table(df[["nama", "pelajaran", "deadline", "kesulitan", "prioritas"]])
    else:
        st.info("Belum ada tugas yang ditambahkan.")
except Exception as e:
    st.error(f"Gagal mengambil data tugas: {e}")

# --- Tombol Hapus Semua ---
if st.button("🗑️ Hapus Semua Tugas"):
    try:
        user_id = st.session_state["user"].id
        supabase.table("tasks").delete().eq("user_id", user_id).execute()
        st.warning("Semua tugas kamu telah dihapus.")
        st.rerun()
    except Exception as e:
        st.error(f"Gagal menghapus tugas: {e}")