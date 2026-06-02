import streamlit as st
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Gate System - FruiTastic Four",
    page_icon="🎵",
    layout="centered"
)

# --- INITIALIZATION (SESSION STATE) ---
# Menggunakan session state agar data tidak hilang saat halaman di-refresh oleh tombol
if "counter_penonton" not in st.session_state:
    st.session_state.counter_penonton = 0

if "log_aktivitas" not in st.session_state:
    st.session_state.log_aktivitas = []

if "antrean_tiket" not in st.session_state:
    # Antrean awal tiruan berdasarkan tipe tiket yang ada di festival
    st.session_state.antrean_tiket = [
        "VIP + CAMP", "GA", "VIP", "GA + CAMP", "FastTrack", 
        "GA", "Palsu", "VIP", "GA"
    ]

if "sistem_terkunci" not in st.session_state:
    st.session_state.sistem_terkunci = False

# --- UI HEADER & LOGO ---
st.title("🎵 FruiTastic Four Music Festival")
st.subheader("Gate Entry & Validation System")
st.markdown("---")

# --- DASHBOARD STATISTIK (COUNTER) ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="👥 Penonton di Dalam Venue", value=st.session_state.counter_penonton)
with col2:
    status_sistem = "🚨 TERKUNCI (Investigasi Keamanan)" if st.session_state.sistem_terkunci else "🟢 AKTIF / AMAN"
    st.metric(label="🛡️ Status Sistem Gerbang", value=status_sistem)

st.markdown("---")

# --- KONTROL SIMULASI ---
st.write("### 🎫 Kendali Antrean Masuk")

if st.session_state.sistem_terkunci:
    st.error("❌ SISTEM BERHENTI TOTAL: Ditemukan tiket PALSU dalam antrean! Investigasi keamanan sedang berlangsung.")
    if st.button("🔓 Reset & Buka Kembali Sistem"):
        st.session_state.sistem_terkunci = False
        st.session_state.antrean_tiket = ["VIP", "GA", "GA + CAMP", "VIP + CAMP"]  # Reset antrean baru
        st.session_state.log_aktivitas.append("🔄 Sistem di-reset dan dibuka kembali oleh petugas.")
        st.rerun()
else:
    if len(st.session_state.antrean_tiket) > 0:
        st.info(f"📋 **Total tiket dalam antrean saat ini:** {len(st.session_state.antrean_tiket)} orang.")
        st.write(f"👉 **Tiket berikutnya yang akan diperiksa:** `{st.session_state.antrean_tiket[0]}`")
        
        if st.button("⏭️ Proses Tiket Berikutnya"):
            # Mengambil tiket paling depan (index 0)
            tiket = st.session_state.antrean_tiket.pop(0)
            
            # --- LOGIKA TEKNIS GERBANG ---
            if tiket == "Palsu":
                st.session_state.sistem_terkunci = True
                st.session_state.log_aktivitas.insert(0, "🚨 ERROR: Ditemukan TIKET PALSU! Sistem otomatis dikunci.")
                st.rerun()
                
            elif tiket in ["VIP", "VIP + CAMP", "FastTrack"]:
                # Jalur cepat: Langsung proses masuk tanpa cek tas mendalam (Continue)
                st.session_state.counter_penonton += 1
                st.session_state.log_aktivitas.insert(
                    0, f"✨ [FAST TRACK] Tiket '{tiket}' valid. Bebas cek tas mendalam. Silakan masuk!"
                )
                st.success(f"🎟️ '{tiket}' berhasil masuk via Jalur Cepat!")
                
            else:
                # Jalur Regular (GA / GA + CAMP)
                with st.spinner("🔍 Melakukan pengecekan tas mendalam untuk tiket GA..."):
                    time.sleep(1) # Simulasi waktu pengecekan fisik
                st.session_state.counter_penonton += 1
                st.session_state.log_aktivitas.insert(
                    0, f"✅ [REGULAR] Tiket '{tiket}' valid. Pengecekan tas selesai. Silakan masuk."
                )
                st.success(f"🎟️ '{tiket}' berhasil masuk setelah pemeriksaan.")
                
            st.rerun()
    else:
        st.success("🎉 Semua antrean tiket telah selesai diproses!")
        if st.button("➕ Tambah Antrean Baru"):
            st.session_state.antrean_tiket = ["GA", "VIP + CAMP", "Palsu", "GA + CAMP"]
            st.rerun()

# --- MANAJEMEN ANTREAN KUSTOM ---
with st.sidebar:
    st.header("⚙️ Panel Petugas")
    st.write("Tambahkan penonton kustom ke dalam antrean:")
    tipe_tiket_baru = st.selectbox(
        "Pilih Tipe Tiket:", 
        ["GA", "GA + CAMP", "VIP", "VIP + CAMP", "FastTrack", "Palsu"]
    )
    if st.button("➕ Masukkan ke Antrean"):
        if not st.session_state.sistem_terkunci:
            st.session_state.antrean_tiket.append(tipe_tiket_baru)
            st.sidebar.success(f"Tiket {tipe_tiket_baru} ditambahkan ke urutan belakang.")
            st.rerun()
        else:
            st.sidebar.error("Sistem terkunci, tidak bisa menambah antrean.")

    if st.button("🧹 Reset Jumlah Penonton (Set ke 0)"):
        st.session_state.counter_penonton = 0
        st.session_state.log_aktivitas.insert(0, "🧹 Counter penonton di-reset ke 0.")
        st.rerun()

# --- LIVE LOG AKTIVITAS ---
st.markdown("---")
st.write("### 📜 Log Validasi Gerbang (Terbaru di atas)")
if st.session_state.log_aktivitas:
    for log in st.session_state.log_aktivitas:
        if "🚨" in log:
            st.error(log)
        elif "✨" in log:
            st.info(log)
        else:
            st.text(log)
else:
    st.caption("Belum ada aktivitas pemeriksaan.")
