# --- LOGIKA UTAMA FLOWCHART (WHILE LOOP) ---
                while len(antrean_lokal) > 0:
                    tiket_sekarang = antrean_lokal.pop(0)
                    
                    # 1. Apakah tiketnya palsu? (BREAK)
                    if tiket_sekarang['tipe'] == "Palsu":
                        log_palsu = f"❌ BREAK: Tiket palsu {tiket_sekarang['nama']} ({tiket_sekarang['code']})! Sistem terkunci."
                        st.session_state.log_proses.append(log_palsu)
                        st.session_state.status_berhenti = True
                        st.session_state.antrean = antrean_lokal
                        break
                        
                    # 2. Apakah tiket VIP atau FastTrack? (CONTINUE)
                    if tiket_sekarang['tipe'] in ["VIP", "FastTrack"]:
                        st.session_state.counter_penonton += 1
                        log_cepat = f"⚡ CONTINUE: {tiket_sekarang['nama']} ({tiket_sekarang['code']}) - {tiket_sekarang['tipe']}. Status: Valid cepat."
                        st.session_state.log_proses.append(log_cepat)
                        continue
                        
                    # 3. Jika Tiket Reguler (Normal / Lakukan pengecekan tas)
                    log_normal = f"🎒 NORMAL: {tiket_sekarang['nama']} ({tiket_sekarang['code']}). Cek tas mendalam. Status: Valid normal."
                    st.session_state.log_proses.append(log_normal)
                    st.session_state.counter_penonton += 1
