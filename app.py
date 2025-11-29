import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NFC Scanner Project", page_icon="📱")

st.title("📱 NFC Scanner for Streamlit")
st.write("Aplikasi ini menggunakan Web NFC API untuk membaca Serial Number kartu.")

# --- CSS & JAVASCRIPT INJECTION ---
# Kita membungkus logika JS kamu ke dalam string HTML
nfc_component = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; padding: 10px; }
        .btn {
            background-color: #ff4b4b; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        .btn-scan { background-color: #0083B8; } /* Biru Streamlit */
        .btn-abort { background-color: #ff4b4b; display: none; } /* Merah */
        
        .status-box {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        #rfid_result { font-weight: bold; color: #0083B8; font-size: 1.2em; }
        #log_area { font-size: 0.9em; color: #666; margin-top: 10px; }
    </style>
</head>
<body>

    <button id="btnScan" class="btn btn-scan" onclick="startScan()">📡 Scan NFC</button>
    <button id="btnAbort" class="btn btn-abort" onclick="stopScan()">🛑 Stop Scan</button>

    <div class="status-box">
        <p>Status: <span id="status_text">Siap...</span></p>
        <p>RFID Serial Number: <br><span id="rfid_result">-</span></p>
    </div>
    <div id="log_area"></div>

    <script>
        let ndef = null;
        let abortController = null;
        let isScanning = false;

        function log(msg) {
            console.log(msg);
            document.getElementById('log_area').innerHTML = "Log: " + msg;
        }

        function updateStatus(msg) {
            document.getElementById('status_text').innerText = msg;
        }

        async function startScan() {
            // 1. Cek Support Browser
            if (!('NDEFReader' in window)) {
                alert('Browser ini tidak mendukung NFC! Pastikan pakai Chrome di Android & HTTPS.');
                log('NFC not supported');
                return;
            }

            if (isScanning) {
                log("Scan masih berjalan...");
                return;
            }

            // UI Updates
            document.getElementById('btnScan').style.display = 'none';
            document.getElementById('btnAbort').style.display = 'inline-block';
            updateStatus("Silakan tempelkan kartu NFC ke belakang HP...");

            try {
                isScanning = true;
                ndef = new NDEFReader();
                abortController = new AbortController();

                // 2. Mulai Scanning
                await ndef.scan({ signal: abortController.signal });
                log("Scan started...");

                ndef.onreadingerror = () => {
                    log("Gagal membaca kartu. Coba posisikan ulang.");
                };

                ndef.onreading = (event) => {
                    log("Kartu Terdeteksi!");
                    
                    if (event.serialNumber) {
                        // Tampilkan Hasil di Layar
                        document.getElementById('rfid_result').innerText = event.serialNumber;
                        log("Serial Number: " + event.serialNumber);
                        
                        // Opsional: Bunyikan getar
                        if (navigator.vibrate) navigator.vibrate(200);
                        
                        // Di sini kamu bisa kirim data ke Python nanti (via URL parameter atau library tambahan)
                    } else {
                        log("Kartu terbaca, tapi tidak ada Serial Number.");
                    }
                };

            } catch (error) {
                log("Error: " + error);
                stopScan();
            }
        }

        function stopScan() {
            log("Menghentikan scan...");
            if (abortController) {
                abortController.abort();
                abortController = null;
            }
            ndef = null;
            isScanning = false;
            
            // Reset UI
            document.getElementById('btnScan').style.display = 'inline-block';
            document.getElementById('btnAbort').style.display = 'none';
            updateStatus("Scan dihentikan.");
        }
    </script>
</body>
</html>
"""

# Render komponen HTML ke dalam Streamlit
components.html(nfc_component, height=400)

st.info("Catatan: Web NFC API hanya berjalan di **Google Chrome Android** dan wajib menggunakan protokol **HTTPS** (atau Localhost).")