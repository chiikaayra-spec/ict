import streamlit as st
import os

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Fruitastic Four - Ticket System", page_icon="🎵", layout="wide")

# Custom CSS untuk mempercantik tampilan agar senada dengan tema Fruitastic Four
st.markdown("""
    <style>
    .main {
        background-color: #fffaf5;
    }
    h1, h2, h3 {
        color: #ff5e3a !important;
    }
    .stButton>button {
        background-color: #ff7e47;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff5e3a;
        color: white;
    }
    </style>
""", unsafe_index=True)

# ==========================================
# 1. INISIALISASI SESSION STATE (DATABASE GLOBAL)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "Home"

if 'antrean' not in st.session_state:
    st.session_state.antrean = [
        {"nama": "Ahmad", "code": "FTF-001", "tipe": "Reguler"},
        {"nama": "Jessica", "code": "FTF-002", "tipe": "VIP"},
        {"nama": "Budi", "code": "FTF-003", "tipe": "Palsu"},  # Menguji logika BREAK
        {"nama": "Siti", "code": "FTF-004", "tipe": "FastTrack"}
    ]

if 'counter_penonton' not in st.session_state:
    st.session_state.counter_penonton = 0

if 'log_proses' not in st.session_state:
    st.session_state.log_proses = []

if 'status_berhenti' not in st.session_state:
    st.session_state.status_berhenti = False

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
    st.session_state.current_user_name = ""


# ==========================================
# 2. HALAMAN HOME (MENU UTAMA)
# ==========================================
if st.session_state.page == "Home":
    # Menampilkan Banner Utama dari File Gambar 'Front screen.png'
    if os.path.exists("Front screen.png"):
        st.image("Front screen.png", use_container_width=True)
    else:
        st.title("🎵 Fruitastic Four Music Festival")
    
    st.markdown("<h2 style='text-align: center;'>Sistem Manajemen & Validasi Tiket Terpadu</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("Silakan pilih pintu masuk sistem sesuai dengan peran Anda:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 👨‍💼 Pintu Masuk Admin / Panitia")
        st.write("Digunakan oleh panitia untuk memvalidasi antrean tiket masuk sesuai dengan flowchart keamanan (Logika `WHILE`, `BREAK`, `CONTINUE`).")
        if st.button("Masuk Halaman Admin", use_container_width=True, type="primary"):
            st.session_state.page = "Admin"
            st.rerun()
            
    with col2:
        st.success("### 👤 Pintu Masuk Pengunjung")
        st.write("Digunakan oleh penonton untuk login, melakukan klaim tiket, dan konfirmasi kehadiran ke dalam sistem.")
        if st.button("Masuk Halaman User", use_container_width=True, type="secondary"):
            st.session_state.page = "User"
            st.rerun()


# ==========================================
# 3. HALAMAN ADMIN (DASHBOARD & LOGIKA FLOWCHART)
# ==========================================
elif st.session_state.page == "Admin":
    if st.button("⬅️ Kembali ke Home Menu"):
        st.session_state.page = "Home"
        st.rerun()
        
    st.title("👨‍💼 Dashboard Admin - Pemeriksaan Tiket")
    st.markdown("---")
    
    # PROTEKSI LOGIN ADMIN
    if not st.session_state.admin_logged_in:
        col_login1, col_login2 = st.columns([1, 1])
        
        with col_login1:
            st.warning("⚠️ Anda harus login terlebih dahulu untuk mengakses data tiket.")
            with st.form("admin_login_form"):
                st.subheader("Login Kredensial Admin")
                admin_user = st.text_input("Username Admin")
                admin_pass = st.text_input("Password Admin", type="password")
                btn_login_admin = st.form_submit_button("Masuk sebagai Admin")
                
                if btn_login_admin:
                    if admin_user == "admin" and admin_pass == "admin123":
                        st.session_state.admin_logged_in = True
                        st.success("🔑 Login Berhasil!")
                        st.rerun()
                    else:
                        st.error("Username atau password salah. (Hint: admin / admin123)")
                        
        with col_login2:
            # Menggunakan gambar Loading.png sebagai penghias halaman login
            if os.path.exists("Loading.png"):
                st.image("Loading.png", caption="Sistem Validasi Gate Fruitastic Four", use_container_width=True)
                    
    # JIKA ADMIN SUDAH LOGIN SUCCESSFULLY
    else:
        st.sidebar.write(f"Logged in as: **Admin**")
        if st.sidebar.button("🔓 Logout Admin", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        # Statistik Utama
        col_stat1, col_stat2 = st.columns(2)
        col_stat1.metric(label="Total Penonton Masuk Venue", value=st.session_state.counter_penonton)
        col_stat2.metric(label="Jumlah Tiket dalam Antrean", value=len(st.session_state.antrean))
        
        # Tampilkan Data Tiket yang Ada di Antrean saat ini
        st.subheader("📋 Daftar Data Antrean Tiket Masuk")
        if len(st.session_state.antrean) > 0:
            st.dataframe(st.session_state.antrean, use_container_width=True)
        else:
            st.info("Semua antrean kosong atau telah selesai diproses.")
            
        st.markdown("### ⚙️ Jalankan Simulasi Validasi")
        
        if st.button("▶️ Proses Antrean Berdasarkan Flowchart", use_container_width=True):
            if st.session_state.status_berhenti:
                st.error("🚨 SISTEM TERKUNCI! Investigasi keamanan sedang berlangsung karena ditemukan tiket palsu. Selesaikan investigasi dengan menekan tombol reset.")
            elif len(st.session_state.antrean) == 0:
                st.warning("Tidak ada data tiket untuk diproses.")
            else:
                antrean_lokal = st.session_state.antrean.copy()
                
                # --- LOGIKA UTAMA FLOWCHART (WHILE LOOP) ---
                while len(antrean_lokal) > 0:
                    tiket_sekarang = antrean_lokal.pop(0)  # Ambil tiket berikutnya
                    
                    # 1. Apakah tiketnya palsu?
                    if tiket_sekarang['tipe'] == "Palsu":
                        st.session_state.log_proses.append(
                            f"❌ BREAK: Tiket palsu terdeteksi atas nama {tiket_sekarang['nama']} ({tiket_sekarang['code']})! Sistem dihentikan total untuk Investigasi Keamanan."
                        )
                        st.session_state.status_berhenti = True
                        st.session_state.antrean = antrean_lokal  # Sisa antrean tertahan
                        break  # KELUAR DARI LOOP SECARA PAKSA (BREAK)
                        
                    # 2. Apakah tiket VIP atau FastTrack?
                    if tiket_sekarang['tipe'] in ["VIP", "FastTrack"]:
                        st.session_state.log_proses.append(
                            f"⚡ CONTINUE: {tiket_sekarang['nama']} ({tiket_sekarang['code']}) memegang tiket {tiket_sekarang['tipe']}. Langsung proses masuk (Status: Valid cepat)."
                        )
                        st.session_state.counter_penonton += 1
                        continue  # LANGSUNG KEMBALI KE WHILE (CONTINUE)
                        
                    # 3. Jika Tiket Reguler (Tidak Palsu, Tidak VIP/FastTrack)
                    st.session_state.log_proses.append(
