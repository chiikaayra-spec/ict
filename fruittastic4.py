import streamlit as st
import time

st.set_page_config(page_title="Admin Dashboard - Summer Fest", page_icon="🎟️")

st.title("🎟️ Dashboard Admin Pemeriksaan Tiket")
st.markdown("---")

# 1. Inisialisasi Data & Variabel di Session State
if 'antrean' not in st.session_state:
    # Simulasi antrean tiket
    st.session_state.antrean = [
        {"id": "TKT-001", "tipe": "Reguler"},
        {"id": "TKT-002", "tipe": "VIP"},
        {"id": "TKT-003", "tipe": "Reguler"},
        {"id": "TKT-004", "tipe": "Palsu"}, # Ini akan memicu BREAK
        {"id": "TKT-005", "tipe": "FastTrack"},
        {"id": "TKT-006", "tipe": "Reguler"}
    ]
if 'counter_penonton' not in st.session_state:
    st.session_state.counter_penonton = 0 # Set counter_penonton = 0
if 'log_proses' not in st.session_state:
    st.session_state.log_proses = []
if 'status_berhenti' not in st.session_state:
    st.session_state.status_berhenti = False

# Tampilkan Counter
col1, col2 = st.columns(2)
col1.metric(label="Total Penonton Masuk", value=st.session_state.counter_penonton)
col2.metric(label="Sisa Antrean", value=len(st.session_state.antrean))

st.markdown("### Kontrol Antrean")

# 2. Logika Utama sesuai Flowchart
if st.button("▶️ Proses Antrean", use_container_width=True):
    if st.session_state.status_berhenti:
        st.error("🚨 SISTEM TERKUNCI! Investigasi keamanan sedang berlangsung. Harap reset sistem.")
    elif len(st.session_state.antrean) == 0:
        st.warning("Antrean sudah kosong. Selesai!")
    else:
        # Pindahkan sisa antrean ke variabel sementara untuk diproses
        antrean_sementara = st.session_state.antrean.copy()
        
        # LOGIKA FLOWCHART: WHILE antrean masih ada
        while len(antrean_sementara) > 0:
            # Ambil tiket berikutnya
            tiket = antrean_sementara.pop(0) 
            
            # Apakah tiketnya palsu?
            if tiket['tipe'] == "Palsu":
                st.session_state.log_proses.append(f"❌ {tiket['id']} - IYA (Palsu) -> Tampilkan Investigasi Keamanan")
                st.session_state.status_berhenti = True
                st.session_state.antrean = antrean_sementara # Simpan sisa antrean yang tertahan
                break # BREAK - Keluar dari perulangan
            
            # Apakah tiket VIP atau FastTrack?
            if tiket['tipe'] == "VIP" or tiket['tipe'] == "FastTrack":
                st.session_state.log_proses.append(f"⚡ {tiket['id']} - IYA ({tiket['tipe']}) -> Langsung proses masuk. Status: Valid cepat")
                st.session_state.counter_penonton += 1
                continue # CONTINUE - Kembali ke awal WHILE
            
            # Jika TIDAK (Reguler)
            st.session_state.log_proses.append(f"🎒 {tiket['id']} - TIDAK (Reguler) -> Lakukan pengecekan tas. Status: Valid normal")
            st.session_state.counter_penonton += 1
            
        # Jika loop selesai tanpa break (tidak ada tiket palsu), kosongkan antrean utama
        if not st.session_state.status_berhenti:
            st.session_state.antrean = []
        
        st.rerun()

if st.button("🔄 Reset Sistem"):
    st.session_state.clear()
    st.rerun()

st.markdown("---")
st.markdown("### Riwayat Pemeriksaan")
# Menampilkan log proses dari yang terbaru
for log in reversed(st.session_state.log_proses):
    if "❌" in log:
        st.error(log)
    elif "⚡" in log:
        st.success(log)
    else:
        st.info(log)
