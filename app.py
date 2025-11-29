import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="NFC Scanner", page_icon="📲")

st.title("📲 NFC Scanner")

# --- KODE APLIKASI HTML/JS ---
# Kita simpan kode HTML ke dalam variabel string Python
nfc_app = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* TAMPILAN (CSS) */
        .box {
            border: 2px dashed #0083B8;
            padding: 20px;
            text-align: center;
            background-color: #f9f9f9;
            border-radius: 10px;
            margin-top: 20px;
        }
        .status { font-weight: bold; margin-bottom: 10px; color: #333; }
        .result { 
            font-size: 24px; 
            font-weight: bold; 
            color: #0083B8; 
            margin: 20px 0; 
            min-height: 40px; 
        }
        button {
            background-color: #0083B8;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        button:active { background-color: #005f85; }
        #log { font-size: 12px; color: gray; text-align: left; margin-top: 15px; border-top: 1px solid #ccc; }
    </style>
</head>
<body>

    <div class="box">
        <div id="status_text" class="status">Menunggu Perintah...</div>
        
        <div id="scan_result" class="result">-</div>

        <button id="btn_scan" onclick="startScan()">📡 MULAI SCAN</button>

        <div id="log">Log Sistem: Siap.</div>
    </div>

    <script>
        var ndef = null;

        function log(msg) {
            document.getElementById("log").innerHTML += "<br>> " + msg;
        }

        function setStatus(msg) {
            document.getElementById("status_text").innerText = msg;
        }

        async function startScan() {
            // 1. Cek Apakah Browser Support
            if (!("NDEFReader" in window)) {
                alert("Browser tidak support NFC! Pakai Chrome Android.");
                setStatus("Browser Tidak Support");
                return;
            }

            // Update UI jadi Loading
            document.getElementById("btn_scan").style.display = "none";
            setStatus("⏳ Mengaktifkan NFC... Tunggu...");
            log("Meminta izin NFC...");

            try {
                ndef = new NDEFReader();
                
                // 2. INI YANG MEMBUAT POP-UP MUNCUL
                await ndef.scan(); 

                // 3. JIKA SUKSES LEWAT SINI
                setStatus("✅ SIAP! Tempelkan Kartu Sekarang.");
                log("NFC Aktif. Silakan tempel kartu.");
                
                // Getar pendek tanda siap
                if (navigator.vibrate) navigator.vibrate(100);

                // 4. SAAT KARTU DITEMPEL
                ndef.onreading = event => {
                    var serial = event.serialNumber;
                    document.getElementById("scan_result").innerText = serial;
                    setStatus("🎉 BERHASIL BACA!");
                    log("ID Terbaca: " + serial);
                    
                    // Getar sukses
                    if (navigator.vibrate) navigator.vibrate([100, 50, 100]);
                    
                    // Kembalikan tombol (Opsional)
                    // document.getElementById("btn_scan").style.display = "block";
                };

                ndef.onreadingerror = () => {
                    setStatus("⚠️ Gagal baca. Coba lagi.");
                    log("Error membaca chip.");
                };

            } catch (error) {
                setStatus("❌ Gagal: " + error.name);
                log("Error: " + error.message);
                alert("Gagal: " + error.message);
                document.getElementById("btn_scan").style.display = "block";
            }
        }
    </script>
</body>
</html>
"""

# --- INI BAGIAN TERPENTING ---
# Jangan pakai st.write() atau st.code()
# Wajib pakai st.markdown(..., unsafe_allow_html=True)
st.markdown(nfc_app, unsafe_allow_html=True)
