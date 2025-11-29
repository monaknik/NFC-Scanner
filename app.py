import streamlit as st

st.set_page_config(page_title="NFC Project", page_icon="📱")

st.title("📱 Proyek NFC Scanner")
st.write("Karena batasan keamanan browser, Scanner harus dibuka di halaman khusus.")

# Ganti LINK_INI dengan link GitHub Pages yang kamu dapat tadi
# Contoh: https://budi.github.io/tugas-nfc/
github_pages_url = "LINK_GITHUB_PAGES_KAMU_DISINI" 

st.markdown(f"""
    <a href="{github_pages_url}" target="_blank">
        <button style="
            background-color: #0083B8;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
            border: none;
            width: 100%;">
            🚀 BUKA SCANNER NFC (FULL SCREEN)
        </button>
    </a>
    """, unsafe_allow_html=True)

st.info("Klik tombol di atas untuk membuka Scanner di tab baru. Pastikan menggunakan Chrome Android.")
