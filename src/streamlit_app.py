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
# CSS CYBERPUNK NEON
# -------------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f0f1f, #1a0033);
    background-attachment: fixed;
    color: white;
}

.main {
    background: rgba(10, 10, 20, 0.6);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(138, 43, 226, 0.4);
    box-shadow: 0 0 25px rgba(138, 43, 226, 0.4);
}

h1 {
    font-size: 48px;
    color: #a855f7;
    font-weight: 900;
    text-shadow: 0 0 15px #c084fc;
    text-align: center;
}

.header-sub {
    text-align: center;
    margin-top: -10px;
    color: #c084fc;
    font-size: 19px;
    margin-bottom: 25px;
}

.card {
    background: rgba(20, 20, 40, 0.7);
    padding: 22px;
    margin-bottom: 20px;
    border-radius: 18px;
    border: 1px solid rgba(168, 85, 247, 0.4);
    box-shadow: 0 0 18px rgba(168, 85, 247, 0.3);
}

.stButton>button {
    background: linear-gradient(135deg, #7c3aed, #4c1d95);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    border: none;
    font-size: 20px;
    font-weight: 700;
    width: 100%;
    transition: 0.25s;
    box-shadow: 0 0 15px #9333ea;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #9d4edd, #5b21b6);
    transform: scale(1.03);
    box-shadow: 0 0 22px #c084fc;
}

.delete-btn>button {
    background: linear-gradient(135deg, #ef4444, #7f1d1d) !important;
    box-shadow: 0 0 15px #ef4444 !important;
}

.delete-btn>button:hover {
    background: linear-gradient(135deg, #dc2626, #450a0a) !important;
    box-shadow: 0 0 22px #f87171 !important;
}

.dataframe {
    border-radius: 10px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1>⚡ Luminous AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='header-sub'>Cyberpunk Neon Task Manager</div>", unsafe_allow_html=True)

# -------------------------------
# CARD INPUT
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("➤ Tambahkan Tugas Baru")

nama = st.text_input("Nama Tugas", placeholder="Contoh: PR Fisika Bab 5")
pelajaran = st.text_input("Mata Pelajaran", placeholder="Contoh: Fisika")
deadline = st.date_input("Deadline")
kesulitan = st.selectbox("Tingkat Kesulitan", ["Mudah", "Normal", "Sulit"])

if st.button("➕ Tambahkan Tugas Disini Kak!"):
    sisa_hari = (deadline - datetime.today().date()).days

    if sisa_hari <= 1 or kesulitan == "Sulit":
        prioritas = "Sulit"
    elif sisa_hari <= 3:
        prioritas = "Normal"
    else:
        prioritas = "Mudah"

    data = {
        "nama": nama.upper(),
        "pelajaran": pelajaran,
        "deadline": str(deadline),
        "kesulitan": kesulitan,
        "prioritas": prioritas
    }

    try:
        supabase.table("tasks").insert(data).execute()
        st.success("⚡ Yay! Tugas berhasil ditambahkan!")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# CARD LIST
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📋 Daftar Tugasmu!")

res = supabase.table("tasks").select("*").execute()
tasks = res.data

if tasks:
    df = pd.DataFrame(tasks)
    st.dataframe(df[["nama", "pelajaran", "deadline", "kesulitan", "prioritas"]])
else:
    st.info("Tidak ada tugas — Night City menunggu 🔮")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# DELETE BUTTON
# -------------------------------
st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)

if st.button("🗑️ Hapus Semua Tugas?"):
    try:
        supabase.table("tasks").delete().neq("id", -1).execute()
        st.warning("🔥 Yay! Semua tugas telah dihapus!")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)