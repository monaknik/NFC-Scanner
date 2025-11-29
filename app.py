import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NFC Project", page_icon="📱")

st.title("📱 Integrasi NFC & Streamlit")
st.write("Menggunakan logika JavaScript untuk membaca serial number kartu.")

# --- KODE JAVASCRIPT & HTML (Adaptasi dari kode Magangmu) ---
# Saya menerjemahkan 'this.f().doScan()' menjadi function biasa
# dan 'this.form.get("rfidno")' menjadi manipulasi elemen ID.

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; padding: 10px; }
        
        /* Gaya Tombol meniru style Streamlit */
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: #fff;
            border: none;
            border-radius: 5px;
            box-shadow: 0 2px #999;
        }

        .btn-scan { background-color: #0083B8; } /* Biru */
        .btn-abort { background-color: #ff4b4b; display: none; } /* Merah */
        .btn-save { background-color: #28a745; margin-top: 20px;} /* Hijau */
        
        .btn:active { transform: translateY(4px); }

        .input-group { margin-top: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #333;}
        input { 
            width: 95%; 
            padding: 8px; 
            border: 1px solid #ccc; 
            border-radius: 4px;
            font-size: 16px;
        }
        input[readonly] { background-color: #e9ecef; }
        
        #log_area { 
            margin-top: 20px; 
            color: red; 
            font-size: 12px; 
            font-family: monospace; 
        }
    </style>
</head>
<body>

    <div>
        <button id="btnScan" class="btn btn-scan" onclick="doScan()">Scan NFC</button>
        <button id="btnAbort" class="btn btn-abort" onclick="doAbort()">Abort Scan</button>
    </div>

    <div class="input-group">
        <label>RFID Number</label>
        <input type="text" id="rfidno" placeholder="Hasil scan muncul di sini..." readonly>
    </div>

    <div class="input-group">
        <label>Nama Lokasi</label>
        <input type="text" id="namalokasi" placeholder="Masukkan nama lokasi">
    </div>

    <div class="input-group">
        <button class="btn btn-save" onclick="btnSaveClicked()">Simpan Data</button>
    </div>

    <div id="log_area"></div>

    <script>
        // Variabel Global (pengganti 'this')
        let ndef = null;
        let abortController = null;
        let isScanning = false;

        // Fungsi Helper untuk Log
        function log(msg) {
            console.log(msg);
            // Opsional: Tampilkan error di layar jika user bingung
            if(msg.includes("Error") || msg.includes("Gagal")) {
                document.getElementById('log_area').innerHTML = msg;
            }
        }

        // --- FUNGSI UTAMA (Dari kode kamu) ---

        // 1. Cek Support
        function checkIfNFCSupported() {
            if (!('NDEFReader' in window)) {
                alert('Perangkat/Browser ini tidak mendukung NFC Web.');
                log('Error: NFC tidak didukung di perangkat ini!');
                return false;
            }
            return true;
        }

        // 2. Fungsi Scan
        async function doScan() {
            log('Memulai scan NFC...');
            
            if (!checkIfNFCSupported()) return;
            
            if (isScanning) {
                console.warn("Scan NFC masih berjalan!");
                return;
            }

            // Reset UI
            doAbort(); 
            isScanning = true;
            document.getElementById('btnScan').style.display = 'none';
            document.getElementById('btnAbort').style.display = 'inline-block';
            document.getElementById('log_area').innerHTML = "Menunggu Kartu...";

            try {
                ndef = new NDEFReader();
                abortController = new AbortController();

                // INI MOMEN REQUEST IZIN POP-UP
                await ndef.scan({ signal: abortController.signal });
                
                log('Scan NFC telah dimulai...');

                ndef.onreadingerror = () => {
                    alert('Tidak dapat membaca data dari NFC Tag. Coba tempel ulang.');
                    console.error('Error membaca NFC Tag');
                };

                ndef.onreading = (event) => {
                    console.log("Tag NFC Terbaca:", event);
                    
                    if (event.serialNumber) {
                        console.log("Serial Number NFC:", event.serialNumber);
                        
                        // Masukkan data ke Input Form HTML (pengganti this.form.setValue)
                        document.getElementById("rfidno").value = event.serialNumber;
                        document.getElementById('log_area').innerHTML = "Sukses Baca!";
                        
                        // Efek Getar
                        if (navigator.vibrate) navigator.vibrate(200);

                    } else {
                        console.warn("Tag NFC tidak memiliki Serial Number!");
                    }
                    
                    // Otomatis stop setelah baca 1 kartu (opsional)
                    // isScanning = false;
                    // doAbort();
                };

            } catch (error) {
                console.error(`Kesalahan saat scan NFC: ${error}`);
                log("Error: " + error.message);
                alert("Gagal: " + error.message);
                doAbort();
            }
        }

        // 3. Fungsi Abort
        function doAbort() {
            console.log('Menghentikan semua proses scan NFC...');
            if (abortController) {
                abortController.abort();
                abortController = null;
            }
            isScanning = false;
            
            // Kembalikan Tombol
            document.getElementById('btnScan').style.display = 'inline-block';
            document.getElementById('btnAbort').style.display = 'none';
        }

        // 4. Fungsi Simpan (Simulasi)
        function btnSaveClicked() {
            let rfid = document.getElementById("rfidno").value;
            let lokasi = document.getElementById("namalokasi").value;

            if(rfid === "") {
                alert("Belum ada kartu yang discan!");
                return;
            }

            alert("SIMPAN DATA:\nID: " + rfid + "\nLokasi: " + lokasi);
            // Disini nanti logika kirim ke Python/Database
        }

    </script>
</body>
</html>
"""

# Render kode HTML/JS tersebut ke dalam Streamlit
# Height disesuaikan agar tombol terlihat semua
components.html(html_code, height=450)
