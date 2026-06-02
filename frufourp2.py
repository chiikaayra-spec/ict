import streamlit as st

# Konfigurasi Halaman Utama
st.set_page_config(page_title="FruiTastic Four Ticket System", page_icon="🎵", layout="wide")

# ==========================================
# INJEKSI CUSTOM CSS (FruiTastic Four Vibe Palette)
# ==========================================
st.markdown("""
    <style>
    /* 1. Mengubah Background Utama Aplikasi (Gradient Sunset) */
    .stApp {
        background: linear-gradient(135deg, #FF7E40 0%, #FFB03A 50%, #FFD066 100%);
        color: #431407 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 2. Mengubah Font dan Warna Judul / Subjudul */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #431407 !important;
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

    /* 3. Desain Kontainer/Card di dalam Aplikasi */
    div[data-testid="stForm"], div[data-testid="stExpander"], .stAlert {
        background-color: #FFFBEB !important;
        border: 3px solid #431407 !important;
        border-radius: 16px !important;
        box-shadow: 5px 5px 0px #431407 !important;
        color: #431407 !important;
    }

    /* 4. Custom Tombol (Buttons) */
    /* Tombol Utama (Primary) */
    button[data-testid="baseButton-primary"] {
        background-color: #EA580C !important;
        color: #FFFBEB !important;
        border: 2px solid #431407 !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #431407 !important;
        font-weight: bold !important;
        transition: all 0.2s ease;
    }
    button[data-testid="baseButton-primary"]:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 5px 5px 0px #431407 !important;
    }

    /* Tombol Sekunder / Biasa */
    button[data-testid="baseButton-secondary"] {
        background-color: #FFFBEB !important;
        color: #431407 !important;
        border: 2px solid #431407 !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #431407 !important;
        font-weight: bold !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #FFB03A !important;
        color: #431407 !important;
    }

    /* 5. Kustomisasi Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFBEB !important;
        border-right: 3px solid #431407 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p {
        color: #431407 !important;
    }

    /* 6. Komponen Input (Text Input & Select Box) */
    input, select, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #431407 !important;
        border-radius: 8px !important;
        color: #431407 !important;
    }

    /* 7. Metrik Data Dashboard */
    div[data-testid="stMetricValue"] {
        color: #EA580C !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #431407 !important;
    }

    /* 8. Dataframe / Tabel Styling */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 2px solid #431407 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 1. INISIALISASI SESSION STATE (DATABASE GLOBAL)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "Home"  # Halaman pertama kali dibuka

if 'antrean' not in st.session_state:
    # Dummy data awal disesuaikan dengan tipe tiket FruiTastic Four
    st.session_state.antrean = [
        {"nama": "Ahmad", "code": "FT4-001", "tipe": "Reguler"},
        {"nama": "Jessica", "code": "FT4-002", "tipe": "VIP"},
        {"nama": "Budi", "code": "FT4-003", "tipe": "Palsu"},  # Untuk menguji logika BREAK
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
    st.session_state.user_logged_in = False
    st.session_state.current_user_name = ""


# ==========================================
# 2. HALAMAN HOME (MENU UTAMA)
# ==========================================
if st.session_state.page == "Home":
    # Menggunakan class main-title dari Custom CSS untuk efek pop retro
    st.markdown('<h1 class="main-title">🍊 FruiTastic Four Music Festival</h1>', unsafe_allow_html=True)
    st.subheader("Gate Entry & Validation System")
    st.markdown("---")
    
    st.write("Silakan pilih pintu masuk sistem sesuai dengan peran Anda:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 👨‍💼 Pintu Masuk Admin")
        st.write("Digunakan oleh panitia untuk memvalidasi antrean tiket masuk sesuai dengan flowchart keamanan.")
        if st.button("Masuk Halaman Admin", use_container_width=True, type="primary"):
            st.session_state.page = "Admin"
            st.rerun()
            
    with col2:
        st.success("### 👤 Pintu Masuk Pengunjung")
        st.write("Digunakan oleh penonton untuk login, melakukan klaim tiket, dan konfirmasi kehadiran.")
        if st.button("Masuk Halaman User", use_container_width=True, type="secondary"):
            st.session_state.page = "User"
            st.rerun()


# ==========================================
# 3. HALAMAN ADMIN (DASHBOARD & LOGIKA FLOWCHART)
# ==========================================
elif st.session_state.page == "Admin":
    # Tombol Kembali ke Home
    if st.button("⬅️ Kembali ke Home Menu", type="secondary"):
        st.session_state.page = "Home"
        st.rerun()
        
    st.markdown('<h1 style="color:#EA580C !important;">👨‍💼 Dashboard Admin - Pemeriksaan Tiket</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # PROTEKSI LOGIN ADMIN
    if not st.session_state.admin_logged_in:
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
                    
    # JIKA ADMIN SUDAH LOGIN SUCCESSFULLY
    else:
        st.sidebar.write(f"Logged in as: **Admin**")
        if st.sidebar.button("🔓 Logout Admin", use_container_width=True, type="secondary"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        # Statistik Utama (Menggunakan Metric Custom CSS)
        col_stat1, col_stat2 = st.columns(2)
        col_stat1.metric(label="Total Penonton Masuk Venue", value=st.session_state.counter_penonton)
        col_stat2.metric(label="Jumlah Tiket dalam Antrean", value=len(st.session_state.antrean))
        
        # Tampilkan Data Tiket yang Ada di Antrean saat ini
        st.subheader("📋 Daftar Data Tiket Saat Ini")
        if len(st.session_state.antrean) > 0:
            st.dataframe(st.session_state.antrean, use_container_width=True)
        else:
            st.info("Semua antrean kosong atau telah selesai diproses.")
            
        st.markdown("### ⚙️ Jalankan Simulasi Validasi")
        
        if st.button("▶️ Proses Antrean Berdasarkan Flowchart", use_container_width=True, type="primary"):
            if st.session_state.status_berhenti:
                st.error("🚨 SISTEM TERKUNCI! Investigasi keamanan sedang berlangsung karena ditemukan tiket palsu. Selesaikan investigasi dengan menekan tombol reset.")
            elif len(st.session_state.antrean) == 0:
                st.warning("Tidak ada data tiket untuk diproses.")
            else:
                antrean_lokal = st.session_state.antrean.copy()
                
                # --- LOGIKA UTAMA FLOWCHART (WHILE LOOP) ---
                while len(antrean_lokal) > 0:
                    tiket_sekarang = antrean_lokal.pop(0)
                    
                    # 1. Apakah tiketnya palsu?
                    if tiket_sekarang['tipe'] == "Palsu":
                        st.session_state.log_proses.append(
                            f"❌ BREAK: Tiket palsu terdeteksi atas nama {tiket_sekarang['nama']} ({tiket_sekarang['code']})! Sistem dihentikan total untuk Investigasi Keamanan."
                        )
                        st.session_state.status_berhenti = True
                        st.session_state.antrean = antrean_lokal
                        break
                        
                    # 2. Apakah tiket VIP atau FastTrack?
                    if tiket_sekarang['tipe'] in ["VIP", "FastTrack"]:
                        st.session_state.log_proses.append(
                            f"⚡ CONTINUE: {tiket_sekarang['nama']} ({tiket_sekarang['code']}) memegang tiket {tiket_sekarang['tipe']}. Langsung proses masuk (Status: Valid cepat)."
                        )
                        st.session_state.counter_penonton += 1
                        continue
                        
                    # 3. Jika Tiket Reguler
                    st.session_state.log_proses.append(
                        f"🎒 NORMAL: {tiket_sekarang['nama']} ({tiket_sekarang['code']}) memegang tiket Reguler. Lakukan pengecekan tas mendalam (Status: Valid normal)."
                    )
                    st.session_state.counter_penonton += 1
                
                if not st.session_state.status_berhenti:
                    st.session_state.antrean = []
                    
                st.rerun()
                
        if st.button("🔄 Reset Simulasi & Muat Ulang Antrean", type="secondary"):
            st.session_state.counter_penonton = 0
            st.session_state.status_berhenti = False
            st.session_state.log_proses = []
            st.session_state.antrean = [
                {"nama": "Ahmad", "code": "FT4-001", "tipe": "Reguler"},
                {"nama": "Jessica", "code": "FT4-002", "tipe": "VIP"},
                {"nama": "Budi", "code": "FT4-003", "tipe": "Palsu"},
                {"nama": "Siti", "code": "FT4-004", "tipe": "FastTrack"}
            ]
            st.success("Sistem berhasil di-reset!")
            st.rerun()
            
        # Log Riwayat Pemrosesan
        st.markdown("---")
        st.subheader("📜 Log Hasil Validasi Keamanan")
        for log in reversed(st.session_state.log_proses):
            if "❌" in log:
                st.error(log)
            elif "⚡" in log:
                st.success(log)
            else:
                st.info(log)


# ==========================================
# 4. HALAMAN USER (LOGIN & CLAIM TIKET)
# ==========================================
elif st.session_state.page == "User":
    if st.button("⬅️ Kembali ke Home Menu", type="secondary"):
        st.session_state.page = "Home"
        st.rerun()
        
    st.markdown('<h1 style="color:#EA580C !important;">👤 Portal Pengunjung - Klaim Tiket</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # PROTEKSI LOGIN USER
    if not st.session_state.user_logged_in:
        st.warning("⚠️ Silakan login menggunakan akun pengunjung Anda.")
        
        with st.form("user_login_form"):
            st.subheader("Login Pengunjung")
            user_input = st.text_input("Username / Email")
            pass_input = st.text_input("Password", type="password")
            btn_login_user = st.form_submit_button("Log In")
            
            if btn_login_user:
                if user_input.strip() != "" and pass_input.strip() != "":
                    st.session_state.user_logged_in = True
                    st.session_state.current_user_name = user_input
                    st.success(f"Selamat datang {user_input}!")
                    st.rerun()
                else:
                    st.error("Username dan Password tidak boleh kosong!")
                    
    # JIKA USER SUDAH LOGIN
    else:
        st.sidebar.write(f"Logged in as: **{st.session_state.current_user_name}**")
        if st.sidebar.button("🔓 Logout User", use_container_width=True, type="secondary"):
            st.session_state.user_logged_in = False
            st.session_state.current_user_name = ""
            st.rerun()
            
        st.write("Lengkapi form di bawah ini untuk melakukan klaim dan konfirmasi kehadiran di FruiTastic Four:")
        
        with st.form("claim_tiket_form", clear_on_submit=True):
            nama_pemegang = st.text_input("Nama Lengkap Pemegang Tiket")
            kode_tiket = st.text_input("Kode Tiket (Contoh: FT4-789)")
            tipe_tiket = st.selectbox("Pilih Tipe Tiket", ["Reguler", "VIP", "FastTrack", "Palsu"]) 
            
            btn_claim = st.form_submit_button("Claim & Konfirmasi Kehadiran")
            
            if btn_claim:
                if nama_pemegang and kode_tiket:
                    data_tiket_baru = {
                        "nama": nama_pemegang,
                        "code": kode_tiket,
                        "tipe": tipe_tiket
                    }
                    st.session_state.antrean.append(data_tiket_baru)
                    
                    st.success("🎉 Berhasil Melakukan Klaim & Konfirmasi Tiket!")
                    st.balloons()
                    st.info(f"Tiket Anda (**{kode_tiket}** - Tipe **{tipe_tiket}**) telah terdaftar masuk ke antrean utama panitia.")
                else:
                    st.error("Gagal! Semua kolom (Nama, Kode Tiket, dan Tipe) wajib diisi.")
