import streamlit as st
import base64
import os

# Fungsi enkripsi gambar lokal ke Base64 CSS
def set_canva_full_page_bg():
    # File poster utama dari aset Canva Anda
    target_bg = "On line screen!.png" 
    
    # Deteksi fallback otomatis jika formatnya adalah .jpg
    if not os.path.exists(target_bg) and os.path.exists("On line screen!.jpg"):
        target_bg = "On line screen!.jpg"
        
    if os.path.exists(target_bg):
        with open(target_bg, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        st.markdown(
            f"""
            <style>
            /* Mengunci background agar memenuhi seluruh layar aplikasi tanpa pergeseran */
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Membuat wadah input form, tabel, dan card menjadi semi-transparan yang estetik */
            .stForm, .stDataFrame, .stAlert, [data-testid="stMetricValue"], .stTable {{
                background-color: rgba(255, 255, 255, 0.93) !important;
                border-radius: 16px !important;
                padding: 24px !important;
                box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.2) !important;
                backdrop-filter: blur(4px);
            }}
            
            /* Optimalisasi keterbacaan teks utama di atas background cerah */
            h1, h2, h3, p, label, .stMarkdown {{
                color: #2c3e50;
                text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.9);
            }}
            
            /* Modifikasi sidebar agar senada dengan nuansa konser */
            [data-testid="stSidebar"] {{
                background-color: rgba(255, 240, 235, 0.85) !important;
                backdrop-filter: blur(8px);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # Peringatan di terminal jika file gambar tidak ditemukan di folder kerja
        print(f"Peringatan: File gambar background '{target_bg}' tidak ditemukan.")

# Panggil fungsi background secara global
set_canva_full_page_bg()
