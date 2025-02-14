import paramiko
from datetime import datetime
from ftplib import FTP
import subprocess

# Konfigurasi perangkat Juniper
DEVICE = {
    "host": "10.10.10.1",
    "username": "admin",
    "password": "password123",
    "port": 9922
}

# Konfigurasi FTP
FTP_SERVER = {
    "host": "10.10.10.4",
    "username": "admin",
    "password": "password123",
    "remote_dir": ""
}

def ssh_command(device, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(device["host"], port=device["port"], username=device["username"], password=device["password"], timeout=180, banner_timeout=180)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode("utf-8")
        client.close()
        return output
    except Exception as e:
        print(f"❌ ERROR: Gagal terhubung ke {device['host']}: {e}")
        return None

def upload_to_ftp(filename):
    try:
        with FTP(FTP_SERVER["host"]) as ftp:
            ftp.login(FTP_SERVER["username"], FTP_SERVER["password"])
            ftp.cwd(FTP_SERVER["remote_dir"])
            with open(filename, 'rb') as file:
                ftp.storbinary(f'STOR {filename}', file)
        print(f"✅ Berhasil mengunggah {filename} ke FTP server")
        # Eksekusi script notifikasi jika upload berhasil
        subprocess.run(["python3", "notif.py"], check=True)
    except Exception as e:
        print(f"❌ ERROR: Gagal mengunggah file ke FTP: {e}")

def backup_config():
    # Ambil hostname
    hostname_output = ssh_command(DEVICE, 'show configuration system host-name | display set | no-more')
    if not hostname_output:
        print("❌ Gagal mengambil hostname")
        return
    hostname = hostname_output.split()[-1].strip(';')
    print(f"📛 Hostname: {hostname}")

    # Ambil konfigurasi dalam format set
    config_output = ssh_command(DEVICE, 'show configuration | display set | no-more')
    if not config_output:
        print("❌ Gagal mengambil konfigurasi")
        return

    # Format nama file
    tanggal = datetime.now().strftime('%Y%m%d')
    filename = f"{hostname}-{tanggal}.xml"

    # Simpan ke file lokal
    with open(filename, 'w') as file:
        file.write(config_output)

    print(f"✅ Konfigurasi berhasil disimpan di {filename}")
    # Upload ke FTP
    upload_to_ftp(filename)

if __name__ == "__main__":
    backup_config()
