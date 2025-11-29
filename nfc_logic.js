// nfc_logic.js
var ndef = null;
var abortController = null;
var isScanning = false;

function logStatus(message, color) {
    const statusEl = document.getElementById("status_text");
    statusEl.innerText = message;
    statusEl.style.color = color || "black";
    console.log(message);
}

function debugLog(msg) {
    const logArea = document.getElementById("debug_area");
    logArea.innerHTML += "> " + msg + "<br>";
}

async function startNFCScan() {
    // 1. Cek Dukungan Browser
    if (!("NDEFReader" in window)) {
        alert("Browser tidak support NFC. Wajib Chrome Android.");
        return;
    }

    // UI Update
    document.getElementById("btnScan").style.display = "none";
    document.getElementById("btnAbort").style.display = "inline-block";
    logStatus("⏳ Mengaktifkan NFC...", "orange");

    try {
        // 2. Inisialisasi Reader
        ndef = new NDEFReader();
        abortController = new AbortController();

        // 3. MULAI LISTENING (Penting: Await sampai benar-benar siap)
        await ndef.scan({ signal: abortController.signal });

        // Jika kode sampai sini, berarti Browser SUDAH SIAP menangkap kartu.
        // Android System tidak akan mengganggu lagi.
        logStatus("✅ SIAP! Tempelkan Kartu Sekarang.", "green");
        
        // Feedback getar tanda siap
        if (navigator.vibrate) navigator.vibrate(100);

        ndef.onreading = event => {
            const serialNumber = event.serialNumber;
            const message = event.message;
            
            // Tampilkan Data
            document.getElementById("rfid_result").innerText = serialNumber || "Data Terbaca (No ID)";
            logStatus("🎉 KARTU TERBACA!", "blue");
            debugLog("Serial Number: " + serialNumber);

            // Getar sukses panjang
            if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
        };

        ndef.onreadingerror = () => {
            logStatus("⚠️ Gagal baca chip. Tempel ulang.", "red");
        };

    } catch (error) {
        logStatus("❌ Error: " + error.name, "red");
        debugLog(error.message);
        alert("Gagal mengaktifkan NFC: " + error.message);
        stopNFCScan();
    }
}

function stopNFCScan() {
    if (abortController) {
        abortController.abort();
        abortController = null;
    }
    document.getElementById("btnScan").style.display = "inline-block";
    document.getElementById("btnAbort").style.display = "none";
    logStatus("Scan Dihentikan.", "black");
}
