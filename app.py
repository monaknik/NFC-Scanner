import streamlit as st

st.set_page_config(page_title="NFC Scanner Final", page_icon="📲")

st.title("📲 NFC Scanner")
st.write("Versi: Direct HTML Injection (Anti-Raw Text)")

# --- KODE LENGKAP HTML + CSS + JS ---
# Kita masukkan semua ke dalam variabel string Python
nfc_app_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <style>
        /* CSS: TAMPILAN */
        .nfc-box {
            font-family: 'Segoe UI', sans-serif;
            border: 2px dashed #0083B8;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            background-color: #f0f8ff;
            margin-top: 20px;
        }
        
        .status-ready { color: green; font-weight: bold; font-size: 1.2em; }
        .status-wait { color: orange; font-weight: bold; }
        .status-error { color: red; font-weight: bold; }

        .btn-main {
            background-color: #0083B8;
            color: white;
            padding: 15px 30px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        .btn-stop { background-color: #d9534f; display: none; }
        
        #result_box {
            margin-top: 20px;
            padding: 10px;
            background: white;
            border-radius: 8px;
            font-size: 24px;
            font-weight: 800;
            color: #333;
            min-height: 50px;
        }
        
        #log_console {
            margin-top: 15px;
            font-size: 12px;
            color: #666;
            text-align: left;
            border-top: 1px solid #ccc;
            padding-top: 5px;
        }
    </style>
</head>
<body>

    <div class="nfc-box">
        <div id="status_indicator" class="status-wait">Menunggu Perintah...</div>
        
        <div id="result_box">-</div>

        <button id="btnScan" class="btn-main" onclick="startScan()">📡 MULAI SCAN</button>
        <button id="btnStop" class="btn-main btn-stop" onclick="stopScan()">🛑 STOP</button>

        <div id="log_console">Log Sistem: Siap.</div>
    </div>

    <script>
        var ndef = null;
        var abortController = null;

        function log(msg) {
            document.getElementById("log_console").innerHTML += "<br>> " + msg;
            console.log(msg);
        }

        function setStatus(text, type) {
            const el = document.getElementById("status_indicator");
            el.innerText = text;
            el.className = ""; // Reset class
            if(type === 'ready') el.classList.add('status-ready');
            else if(type === 'error') el.classList.add('status-error');
            else el.classList.add('status-wait');
        }

        async function startScan() {
            // 1. Cek Browser Support
            if (!("NDEFReader" in window)) {
                setStatus("Browser Tidak Support!", "error");
                alert("NFC Web API tidak didukung. Wajib pakai Chrome di Android.");
                return;
            }

            // UI Update
            document.getElementById("btnScan").style.display = "none";
            document.getElementById("btnStop").style.display = "inline-block";
            setStatus("⏳ Sedang mengaktifkan NFC...", "wait");
            log("Meminta izin NFC...");

            try {
                ndef = new NDEFReader();
                abortController = new AbortController();

                // 2. INI MOMEN PENTING: Await scan()
                // Browser akan minta izin di sini.
                await ndef.scan({ signal: abortController.signal });

                // 3. JIKA SUKSES LEWAT SINI -> BARU TEMPEL KARTU
                setStatus("✅ NFC AKTIF! Tempel Kartu Sekarang.", "ready");
                log("NFC Listener aktif.");
                
                // Getar pendek tanda siap
                if (navigator.vibrate) navigator.vibrate(100);

                ndef.onreading = event => {
                    const serial = event.serialNumber;
                    document.getElementById("result_box").innerText = serial;
                    setStatus("🎉 KARTU TERBACA!", "ready");
                    log("Dapat ID: " + serial);
                    
                    // Getar sukses
                    if (navigator.vibrate) navigator.vibrate([100, 50, 100]);
                };

                ndef.onreadingerror = () => {
                    setStatus("⚠️ Gagal baca. Geser kartu.", "error");
                    log("Reading error.");
                };

            } catch (error) {
                setStatus("❌ Gagal: " + error.name, "error");
                log("Error: " + error.message);
                alert("Gagal scan: " + error.message);
                stopScan();
            }
        }

        function stopScan() {
            if (abortController) {
                abortController.abort();
                abortController = null;
            }
            document.getElementById("btnScan").style.display = "inline-block";
            document.getElementById("btnStop").style.display = "none";
            setStatus("Scan Dihentikan.", "wait");
            log("Scan stopped.");
        }
    </script>
</body>
</html>
"""

# RENDER KE LAYAR
# Parameter unsafe_allow_html=True WAJIB ADA agar kode di atas jadi Tombol, bukan Teks.
st.markdown(nfc_app_code, unsafe_allow_html=True)
