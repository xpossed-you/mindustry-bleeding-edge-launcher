import requests
from tqdm import tqdm
import os, subprocess, time

### FUNCTION ###

def cek_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

### EO FUNCTION ###

if not cek_internet():
    print("Koneksi internet bermasalah, update batal...")

else:
    url = "https://api.github.com/repos/anuken/mindustrybuilds/releases/latest"
    response = requests.get(url)
    data = response.json()

    link_data = data["url"]
    nama_tag = data["tag_name"]
    jumlah_asset = len(data["assets"])
    waktu_publish = data["published_at"]

    nama_file_mindustry_skrang = [f for f in os.listdir() if "Mindustry-BE-Desktop" in f and f.endswith(".jar")]

    if nama_tag in nama_file_mindustry_skrang[0]:
        print("file skarang paling baru, langsung gas bng")
        
    else:
        print("sabar, mo update bang")
        for i in data["assets"]:
            if "Desktop" in i["name"]:
                nama_file = i["name"]
                tipe_konten = i["content_type"]
                ukuran = round((i["size"] / (1024**2)), 2)
                link_donlod = i["browser_download_url"]

                break

        print()

        print(f"Nama tag: {nama_tag}")
        print(f"Jumlah asset: {jumlah_asset}")
        print(f"Waktu publsih: {waktu_publish}")
        print(f"Link update: {link_data}")
        print((len(link_data) + 14) * "=")
        print(f"Nama file: {nama_file}")
        print(f"Tipe konten: {tipe_konten}")
        print(f"Ukuran: {ukuran} mb")
        print(f"Link file: {link_donlod}")

        with requests.get(link_donlod, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            block_size = 1024  # 1 KB chunks

            # Setup progress bar
            with tqdm(total=total_size, unit="B", unit_scale=True, desc=nama_file) as bar:
                with open(nama_file, "wb") as f:
                    for chunk in r.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

        print(f"hasil download: {nama_file}")

        os.remove(nama_file_mindustry_skrang[0])
        print(f"file yg dihapus: {nama_file_mindustry_skrang[0]}")

file_mindustry = [f for f in os.listdir() if "Mindustry-BE-Desktop" in f and f.endswith(".jar")]
if file_mindustry:
    nama_file_updated = max(file_mindustry, key=lambda f: os.path.getmtime(f))
    print(f"Nama file yg mo dijalankan: {nama_file_updated}")

    print("Game akan dijalankan dalam 3 detik...")
    time.sleep(1)
    print("Game akan dijalankan dalam 2 detik...")
    time.sleep(1)
    print("Game akan dijalankan dalam 1 detik...")
    time.sleep(1)

    subprocess.run(["java", "-jar", nama_file_updated])
else:
    nama_file_updated = None
    print("Tidak ada file mindustry.")
