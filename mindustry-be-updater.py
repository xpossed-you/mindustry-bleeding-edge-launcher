"""import os buat explore file, clear layar cmd"""
import os
# import sys # buat debugging sys.exit()

import subprocess
import time
import requests
from tqdm import tqdm


os.system("cls" if os.name == "nt" else "clear")

### intro ###
print("   __   __           ___                    __        ")
print("  / /  / /__ ___ ___/ (_)__  ___ _  ___ ___/ /__ ____")
print(" / _ \/ / -_) -_) _  / / _ \/ _ `/ / -_) _  / _ `/ -_)")
print("/_.__/_/\__/\__/\_,_/_/_//_/\_, /  \__/\_,_/\_, /\__/ ")
print("                           /___/           /___/      ")
print("mindustry launcher & updater, xpossed-you @ github")
print()


waktu_skarang = time.time()

### FUNCTION ###

def cek_internet():
    """buat cek koneksi internet lah, apalagi"""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

### EO FUNCTION ###

if not cek_internet():
    print("Koneksi internet bermasalah, update batal...")

else:
    LINK_API_BUILDMINDUSTRY = "https://api.github.com/repos/anuken/mindustrybuilds/releases/latest"
    response = requests.get(LINK_API_BUILDMINDUSTRY, timeout=5)

    data = response.json()

    link_data = data["url"]
    nama_tag = data["tag_name"]
    jumlah_asset = len(data["assets"])
    waktu_publish = data["published_at"]

    file_mindustry = [f for f in os.listdir()
                                  if "Mindustry-BE-Desktop"
                                  in f and f.endswith(".jar")]


    if nama_tag in file_mindustry[0]:
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

        with requests.get(link_donlod, stream=True, timeout=5) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            BLOCK_SIZE = 1024  # 1 KB

            with tqdm(total=total_size, unit="B", unit_scale=True, desc=nama_file) as bar:
                with open(nama_file, "wb") as f:
                    for chunk in r.iter_content(chunk_size=BLOCK_SIZE):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

        print(f"hasil download: {nama_file}")

        os.remove(file_mindustry[0])
        print(f"file yg dihapus: {file_mindustry[0]}")

file_mindustry = [f for f in os.listdir() if "Mindustry-BE-Desktop" in f and f.endswith(".jar")]
if file_mindustry:
    nama_file_updated = max(file_mindustry, key=os.path.getmtime)

    terakhir_update = os.path.getmtime(nama_file_updated)
    days_ago = int((waktu_skarang - terakhir_update) // (60 * 60 * 24))
    print("tanggal update terakhir:", time.strftime('%d-%m-%Y', time.localtime(terakhir_update)))
    print(f"update terakhir: {days_ago} hari yang lalu")

    print(f"Nama file yg mo dijalankan: {nama_file_updated}")

    print("Game akan dijalankan dalam 3 detik...")
    time.sleep(1)
    print("Game akan dijalankan dalam 2 detik...")
    time.sleep(1)
    print("Game akan dijalankan dalam 1 detik...")
    time.sleep(1)

    subprocess.run(["java", "-jar", nama_file_updated], check=False)
else:
    print("Tidak ada file mindustry.")
