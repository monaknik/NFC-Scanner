import streamlit as st

st.set_page_config(page_title="Modular NFC", page_icon="💳")

st.title("💳 Modular NFC Scanner")
st.write("Versi Modular: Python membaca file HTML & JS terpisah.")

# --- FUNGSI PEMBACA FILE ---
def load_file(filename):
    with open(filename, "r") as f:
        return f.read()

# 1. Baca isi file eksternal
try:
    html_content = load_file("nfc_style.html")
    js_content = load_file("nfc_logic.js")
except FileNotFoundError:
    st.error("Error: Pastikan file 'nfc_style.html' dan 'nfc_logic.js' ada di folder yang sama!")
    st.stop()

# 2. Gabungkan menjadi satu blok HTML lengkap
# Kita membungkus JS dengan tag <script> agar bisa dieksekusi
full_code = f"""
{html_content}
<script>
{js_content}
</script>
"""

# 3. Render ke Browser (Direct Injection)
# Penting: unsafe_allow_html=True agar tidak terblokir iframe
st.markdown(full_code, unsafe_allow_html=True)

st.info("ℹ️ CARA PENGGUNAAN AGAR TIDAK MUNCUL POP-UP SYSTEM:")
st.markdown("""
1. Buka web ini di **Chrome Android**.
2. Klik tombol **'AKTIFKAN SCANNER'** dulu.
3. **TUNGGU** sampai tulisan berubah jadi **"✅ SIAP! Tempelkan Kartu Sekarang"**.
4. Baru tempelkan kartu ke belakang HP.
5. Jika kamu tempel kartu *sebelum* tulisan "SIAP" muncul, HP akan mengeluarkan pop-up sistem (itu salah timing).
""")
