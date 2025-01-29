import requests # type: ignore

# Konfigurasi Telegram
TELEGRAM_BOT_TOKEN = "1qejdkhwaala"  # Ganti dengan token bot Anda
TELEGRAM_CHAT_ID = "1234567890"  # Ganti dengan chat ID Anda

def send_telegram_message(message):
    """Mengirim notifikasi ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Notifikasi terkirim ke Telegram!")
    else:
        print(f"❌ Gagal mengirim ke Telegram: {response.text}")

if __name__ == "__main__":
    message = (
        "🔔 *Notifikasi Sinkronisasi Juniper*\n"
        "✅ Status: *Berhasil*\n"
        "🔄 Sinkronisasi antara Master dan Backup telah selesai!\n"
        "📅 Waktu: "
    )
    send_telegram_message(message)