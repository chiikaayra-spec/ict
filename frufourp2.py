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
