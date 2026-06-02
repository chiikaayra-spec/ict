import streamlit as st

# Konfigurasi Halaman Utama
st.set_page_config(page_title="FruiTastic Four Ticket System", page_icon="🎵", layout="wide")

# ==========================================
# INJEKSI CUSTOM CSS (Optimasi Kontras & Aksesibilitas)
# ==========================================
st.markdown("""
    <style>
    /* 1. Mengubah Background Utama Aplikasi (Gradient Sunset) */
    .stApp {
        background: linear-gradient(135deg, #FF7E40 0%, #FFB03A 50%, #FFD066 100%);
        color: #2D0B03 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 2. Mengubah Font dan Warna Judul / Teks */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #2D0B03 !important;
        font-weight: 700 !important;
    }
    
    /* Style Khusus Title Utama agar bergaya Retro Pop */
    .main-title {
        font-size: 3rem !important;
        text-shadow: 2px 2px 0px #FFFBEB, 4px 4px 0px #EA580C;
        color: #EA580C !important;
        text-align: center;
        margin-bottom: 10px;
    }

    /* 3. Desain Kontainer/Card di dalam Aplikasi dengan Kontras Lebih Baik */
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        background-color: #FFFBEB !important;
        border: 3px solid #2D0B03 !important;
        border-radius: 16px !important;
        box-shadow: 5px 5px 0px #2D0B03 !important;
        color: #2D0B03 !important;
    }
    
    /* Menjaga warna teks di dalam form agar konsisten pekat */
    div[data-testid="stForm"] p, div[data-testid="stForm"] label {
        color: #2D0B03 !important;
    }

    /* 4. Custom Tombol (Sesuai Desain Sebelumnya yang Anda Sukai) */
    /* Tombol Utama (Primary) */
    button[data-testid="baseButton-primary"] {
        background-color: #EA580C !important;
        color: #FFFBEB !important;
        border: 2px solid #2D0B03 !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #2D0B03 !important;
        font-weight: bold !important;
        transition: all 0.2s ease;
    }
    button[data-testid="baseButton-primary"]:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 5px 5px 0px #2D0B03 !important;
    }

    /* Tombol Sekunder / Biasa */
    button[data-testid="baseButton-secondary"] {
        background-color: #FFFBEB !important;
        color: #2D0B03 !important;
        border: 2px solid #2D0B03 !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #2D0B03 !important;
        font-weight: bold !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #FFB03A !important;
        color: #2D0B03 !important;
    }

    /* 5. Kustomisasi Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFBEB !important;
        border-right: 3px solid #2D0B03 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p {
        color: #2D0B03 !important;
    }

    /* 6. Komponen Input dengan Background Putih Bersih (Lebih Mudah Dibaca) */
    input, select, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #2D0B03 !important;
        border-radius: 8px !important;
        color: #2D0B03 !important;
    }
    
    /* Memperbaiki warna teks ketikan di dalam input */
    input[type="text"], input[type="password"] {
        color: #2D0B00 !important;
        font-weight: 500 !important;
    }

    /* 7. Metrik Data Dashboard */
    div[data-testid="stMetricValue"] {
        color: #EA580C !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #2D0B03 !important;
    }

    /* 8. Dataframe / Tabel Styling */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 2px solid #2D0B03 !important;
        border-radius: 8px !important;
    }
    
    /* 9. Menormalkan Teks Alert (Mencegah Tabrakan Warna Background Alert Bawaan) */
    .stAlert p {
        color: inherit !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 1. INISIALISASI SESSION STATE (DATABASE GLOBAL)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "Home"

if 'antrean' not in st.session_state:
    st.session_state.antrean = [
        {"nama": "Ahmad", "code": "FT4-001", "tipe": "Reguler"},
        {"nama": "Jessica", "code": "FT4-002", "tipe": "VIP"},
        {"nama": "Budi", "code": "FT4-003", "tipe": "Palsu"},
        {"nama": "Siti", "code": "FT4-004", "tipe": "FastTrack"}
    ]

if 'counter_penonton' not in st.session_state:
    st.session_state.counter_penonton = 0

if 'log_proses' not in st.session_state:
    st.session_state.log_proses = []

if 'status_berhenti' not in st.session_state:
    st.session_state.status_berhenti = False

# Status Login
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in =
