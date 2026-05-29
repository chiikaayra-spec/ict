import streamlit as st
import base64
import os

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Fruitastic Four - Ticket System", page_icon="🎵", layout="wide")

# ==========================================
# CUSTOM BACKGROUND IMAGE SOURCING (Base64)
# ==========================================
def add_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string.decode()});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            /* Tambahan transparansi sedikit agar form dan tabel tetap terbaca jelas di atas background */
            .stForm, .stDataFrame, .stAlert {{
                background-color: rgba(255, 255, 255, 0.9) !important;
                border-radius: 10px;
                padding: 15px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Memanggil fungsi background kustom (ganti nama file gambar jika ingin merubah latar belakang)
add_bg_from_local('Front screen (2).png')


# ==========================================
# CUSTOM CSS SOURCING (Dari style.css)
# ==========================================
def apply_custom_css(css_file):
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback inline style jika file style.css tidak ada
        st.markdown("""
            <style>
            h1, h2, h3 { color: #ff5e3a !important; font-weight: bold; }
            .stButton>button { background-color: #ff7e47; color: white; border-radius: 8px; font-weight: bold; }
            .stButton>button:hover { background-color: #ff5e3a; color: white; }
            </style>
        """, unsafe_allow_html=True)

# Memanggil fungsi kustom CSS
apply_custom_css('style.css')


# ==========================================
# 1. INISIALISASI SESSION STATE (DATABASE GLOBAL)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "Home"

if 'antrean' not in st.session_state:
    st.session_state.antrean = [
        {"nama": "Ahmad", "code": "FTF-001", "tipe": "Reguler"},
        {"nama": "Jessica", "code": "FTF-002", "tipe": "VIP"},
        {"nama": "Budi", "code": "FTF-003", "tipe": "Palsu"},  # Untuk menguji logika BREAK
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
    if os.path.exists("Front screen.png"):
        st.image("Front screen.png", use_container_width=True)
    else:
        st.title("🎵 Fruitastic Four Music Festival")
    
    st.markdown("<h2 style='text-align: center; background-color: rgba(255,255,255,0.7); border-radius: 8px; padding: 5px;'>Sistem Manajemen & Validasi Tiket Terpadu</h2>", unsafe_allow_html=True)
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
            if os.path.exists("Loading.png"):
                st.image("Loading.png", caption="Sistem Validasi Gate Fruitastic Four", use_container_width=True)
                    
    # JIKA ADMIN SUDAH LOGIN
    else:
        st.sidebar.write(f"Logged in as: **Admin**")
        if st.sidebar.button("🔓 Logout Admin", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        # Statistik Utama
        col_stat1, col_stat2 = st.columns(2)
        col_stat1.metric(label="Total Penonton Masuk Venue (counter_penonton)", value=st.session_state.counter_penonton)
        col_stat2.metric(label="Jumlah Tiket dalam Antrean", value=len(st.session_state.antrean))
        
        # Tampilkan Data Tiket
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
                    tiket_sekarang = antrean_lokal.pop(0)
                    
                    # 1. Apakah tiketnya palsu? (BREAK)
                    if tiket_sekarang['tipe'] == "Palsu":
                        st.session_state.log_proses.append(f"❌ BREAK: Tiket palsu terdeteksi atas nama {tiket_sekarang['nama']} ({tiket_sekarang['code']})! Tampilkan investigasi keamanan.")
                        st.session_state.status_berhenti = True
                        st.session_state.antrean = antrean_lokal
                        break
                        
                    # 2. Apakah tiket \"VIP\" atau \"FastTrack\"? (CONTINUE)
                    if tiket_sekarang['tipe'] in ["VIP", "FastTrack"]:
                        st.session_state.counter_penonton += 1
                        st.session_state.log_proses.append(f"⚡ CONTINUE: {tiket_sekarang['nama']} ({tiket_sekarang['code']}) - Tipe: {tiket_sekarang['tipe']} -> Langsung proses masuk. Status: 'Valid cepat'. counter_pen
