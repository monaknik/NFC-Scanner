import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NFC Scanner Project", page_icon="📱")

st.title("📱 NFC Scanner (Debug Mode)")
st.write("Versi ini akan memunculkan pesan error jika scan gagal.")

nfc_component = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; }
        .btn {
            background-color: #0083B8; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            font-size: 18px;
            font-weight: bold;
            width: 100%;
            margin-bottom: 20px;
        }
        .btn-abort { background-color: #ff4b4b; display: none; }
        .status { font-size: 1.2em; margin-bottom: 10px; color: #333; }
        #rfid_result { font-size: 2em; font-weight: bold; color: #0083B8; word-break: break-all;}
        .error-log { color: red; font-size: 0.9em; margin-top: 20px; text-align: left;}
    </style>
</head>
<body>

    <div class="status" id="status_text">Siap Scan...</div>
    
    <button id="btnScan" class="btn" onclick="startScan()">📡 MULAI SCAN</button>
    <button id="btnAbort" class="btn btn-abort" onclick="stopScan()">🛑 BERHENTI</button>

    <div>ID Kartu:</div>
    <div id="rfid_result">-</div>
    
    <div class="error-log" id="log_area"></div>

    <script>
        let ndef = null;
        let abortController = null;
        let isScanning = false;

        function log(msg) {
            console.log(msg);
            // Tampilkan log di layar agar user bisa baca
            document.getElementById('log_area').innerHTML += ">> " + msg + "<br>";
        }

        async function startScan() {
            // 1. Cek apakah Browser mendukung
            if (!('NDEFReader' in window)) {
                alert("ERROR: Browser ini tidak mendukung Web NFC. Pastikan pakai Chrome di Android.");
                return;
            }

            document.getElementById('btnScan').style.display = 'none';
            document.getElementById('btnAbort').style.display = 'inline-block';
            document.getElementById('status_text').innerText = "Tempelkan Kartu Sekarang...";
            document.getElementById('log_area').innerHTML = ""; // Bersihkan log lama

            try {
                ndef = new NDEFReader();
                abortController = new AbortController();

                // 2. Request Scan
                await ndef.scan({ signal: abortController.signal });
                
                log("Sistem NFC Aktif. Menunggu kartu...");

                ndef.onreadingerror = () => {
                    log("Gagal membaca chip. Coba geser posisi kartu.");
                };

                ndef.onreading = (event) => {
                    // BERHASIL BACA
                    const serialNumber = event.serialNumber;
                    document.getElementById('rfid_result').innerText = serialNumber;
                    log("Kartu Ditemukan! ID: " + serialNumber);
                    
                    // Feedback getar
                    if (navigator.vibrate) navigator.vibrate(200);
                };

            } catch (error) {
                // TANGKAP ERROR DISINI
                document.getElementById('status_text').innerText = "Gagal Mengakses NFC";
                
                // Munculkan ALERT agar user sadar
                alert("SCAN GAGAL!\nPenyebab: " + error.name + "\nPesan: " + error.message);
                
                log("Error Name: " + error.name);
                log("Error Msg: " + error.message);
                
                stopScan();
            }
        }

        function stopScan() {
            if (abortController) {
                abortController.abort();
                abortController = null;
            }
            isScanning = false;
            document.getElementById('btnScan').style.display = 'inline-block';
            document.getElementById('btnAbort').style.display = 'none';
            document.getElementById('status_text').innerText = "Scan Dihentikan.";
        }
    </script>
</body>
</html>
"""

components.html(nfc_component, height=500)


st.info("Catatan: Web NFC API hanya berjalan di **Google Chrome Android** dan wajib menggunakan protokol **HTTPS** (atau Localhost).")
