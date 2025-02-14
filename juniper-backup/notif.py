import requests
import time

# Konfigurasi Telegram
TELEGRAM_BOT_TOKEN = "toker"
TELEGRAM_CHAT_ID = "chat-id"  # Ganti dengan chat ID yang benar

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
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = (
        "🔔 *Notifikasi Backup Juniper*\n"
        "✅ Status: *Berhasil*\n"
        "🔄 Backup Juniper ke FTP server berhasil di lakukan!\n"
        f"📅 Waktu: {current_time}"
    )
    send_telegram_message(message)
