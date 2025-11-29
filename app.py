import streamlit as st

st.set_page_config(page_title="NFC Scanner Project", page_icon="📱")

st.title("📱 NFC Scanner (Direct Injection)")
st.write("Versi ini berjalan langsung di DOM browser untuk menghindari blokir Iframe.")

# --- KODE JAVASCRIPT & HTML ---
# Perhatikan: Kita tidak pakai 'components.html', tapi string biasa
html_code = """
<style>
    .nfc-container {
        font-family: sans-serif; 
        padding: 20px; 
        border: 2px dashed #0083B8; 
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        background-color: #f0f8ff;
    }
    .btn {
        background-color: #0083B8; 
        color: white; 
        padding: 15px 32px; 
        border: none; 
        border-radius: 8px; 
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        margin: 10px;
        transition: 0.3s;
    }
    .btn:active { transform: scale(0.95); }
    .btn-abort { background-color: #ff4b4b; display: none; }
    
    #status_text { font-size: 1.2em; color: #333; margin-bottom: 10px; }
    #rfid_result { 
        font-size: 2em; 
        font-weight: bold; 
        color: #0083B8; 
        margin: 20px 0; 
        word-break: break-all;
    }
    #debug_log { font-size: 0.8em; color: red; margin-top: 20px; text-align: left; }
</style>

<div class="nfc-container">
    <div id="status_text">Siap Scan...</div>
    
    <button id="btnScan" class="btn" onclick="startNFCScan()">📡 MULAI SCAN</button>
    <button id="btnAbort" class="btn btn-abort" onclick="stopNFCScan()">🛑 STOP</button>

    <div>ID KARTU:</div>
    <div id="rfid_result">-</div>
    
    <div id="debug_log"></div>
</div>

<script>
    // Kita gunakan var agar variabel global bisa diakses ulang
    var ndef = null;
    var abortController = null;
    var isScanning = false;

    function debug(msg) {
        console.log(msg);
        // Tampilkan pesan error ke layar user agar kamu tahu kenapa gagal
        const logArea = document.getElementById('debug_log');
        if (logArea) logArea.innerHTML += ">> " + msg + "<br>";
    }

    async function startNFCScan() {
        const btnScan = document.getElementById('btnScan');
        const btnAbort = document.getElementById('btnAbort');
        const statusText = document.getElementById('status_text');
        const resultText = document.getElementById('rfid_result');
        const logArea = document.getElementById('debug_log');

        // Bersihkan log lama
        logArea.innerHTML = ""; 

        // 1. Cek Fitur Browser
        if (!("NDEFReader" in window)) {
            statusText.innerText = "❌ Browser Tidak Support";
            alert("Fitur NFC tidak ada di browser ini. Wajib pakai Chrome di Android.");
            return;
        }

        // Update UI
        btnScan.style.display = "none";
        btnAbort.style.display = "inline-block";
        statusText.innerText = "Tempelkan Kartu Sekarang...";
        resultText.innerText = "-";

        try {
            // Inisialisasi
            ndef = new NDEFReader();
            abortController = new AbortController();

            // 2. REQUEST IZIN (Ini yang biasanya gagal di Iframe)
            await ndef.scan({ signal: abortController.signal });

            debug("NFC Aktif! Menunggu kartu...");

            ndef.onreading = event => {
                const serialNumber = event.serialNumber;
                resultText.innerText = serialNumber;
                statusText.innerText = "✅ Berhasil Membaca!";
                debug("Ditemukan ID: " + serialNumber);
                
                // Getar HP
                if (navigator.vibrate) navigator.vibrate(200);
            };

            ndef.onreadingerror = () => {
                debug("Gagal baca chip. Geser posisi kartu.");
            };

        } catch (error) {
            statusText.innerText = "❌ Gagal: " + error.name;
            debug("Error Name: " + error.name);
            debug("Error Msg: " + error.message);
            
            // Tampilkan Alert agar jelas
            alert("SCAN GAGAL! " + error.name + "\\n" + error.message);
            
            stopNFCScan();
        }
    }

    function stopNFCScan() {
        if (abortController) {
            abortController.abort();
            abortController = null;
        }
        document.getElementById('btnScan').style.display = "inline-block";
        document.getElementById('btnAbort').style.display = "none";
        document.getElementById('status_text').innerText = "Scan Dihentikan.";
    }
</script>
"""

# INI KUNCINYA: Pakai st.markdown dengan unsafe_allow_html=True
# Ini menyuntikkan kode langsung ke halaman, bukan ke dalam iframe.
st.markdown(html_code, unsafe_allow_html=True)

st.info("Tips: Jika scan gagal, klik ikon 🔒 (Gembok) di sebelah URL browser HP kamu, pilih 'Permissions', dan pastikan NFC diizinkan atau klik 'Reset Permissions'.")
