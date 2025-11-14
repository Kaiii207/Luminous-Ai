import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# -------------------------------
# KONFIGURASI SUPABASE
# -------------------------------
SUPABASE_URL = st.secrets["https://ojwwyymjmeneoqlvgbes.supabase.co"]     # Ambil dari HuggingFace Secrets
SUPABASE_KEY = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qd3d5eW1qbWVuZW9xbHZnYmVzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NjI5MzUsImV4cCI6MjA3ODUzODkzNX0.-6tdIlFBLrQe-8tcN2smNpscKdh4AAHtszc4rB0rV_k"]     # Ambil dari HuggingFace Secrets

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
# CHECK SESSION USER
# -------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# -------------------------------
# LOGIN PAGE
# -------------------------------
if st.session_state["user"] is None:

    st.title("🔐 Luminous AI – Login / Register")
    st.markdown("### Login Cepat")

    # -----------------------
    # LOGIN DENGAN GOOGLE
    # -----------------------
    if st.button("🔵 Login dengan Google"):
        redirect_url = "https://YOUR-HUGGINGFACE-SPACE.hf.space"   # GANTI!
        
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {"redirect_to": redirect_url}
        })

        # Tampilkan link login Google
        st.markdown(f"[Klik untuk login Google]({res.url})")
        st.stop()

    st.markdown("---")
    st.markdown("### Login atau Daftar Manual")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # -----------------------
    # LOGIN EMAIL
    # -----------------------
    with col1:
        if st.button("Login"):
            try:
                user = supabase.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )
                st.session_state["user"] = user.user
                st.success("Yay! Berhasil login!")
                st.rerun()
            except:
                st.error("Email Kamu atau Password Kamu Salah, Check Lagi Ya!.")

    # -----------------------
    # REGISTER EMAIL
    # -----------------------
    with col2:
        if st.button("Daftar"):
            try:
                supabase.auth.sign_up({"email": email, "password": password})
                st.success("Horee! Akun berhasil dibuat! Silahkan login kak!.")
            except:
                st.error("Yahh Kasian! Gagal membuat akun. Email mungkin sudah terdaftar. Coba lagi ya.")

    st.stop()

# -------------------------------
# DASHBOARD (SETELAH LOGIN)
# -------------------------------
st.title("🌙 Luminous AI – Pengingat Tugas")
st.success(f"Logged in sebagai: {st.session_state['user'].email}")

# Logout
if st.button("Logout"):
    st.session_state["user"] = None
    st.rerun()

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
        "user_id": st.session_state["user"].id,
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

user_id = st.session_state["user"].id
res = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
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
        supabase.table("tasks").delete().eq("user_id", user_id).execute()
        st.warning("Hore! Semua tugas telah dihapus.")
        st.rerun()
    except Exception as e:
        st.error(f"Yah! Gagal menghapus tugas: {e}")