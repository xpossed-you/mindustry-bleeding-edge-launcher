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

### FUNCTION ###

waktu_skarang = time.time()

def cek_internet():
    """buat cek koneksi internet lah, apalagi"""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

### EO FUNCTION ###

if not cek_internet():
    print("Internet connection error...")

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
        print("You have the latest version.")
    else:
        print("Newer version available, downloading...")
        for i in data["assets"]:
            if "Desktop" in i["name"]:
                nama_file = i["name"]
                tipe_konten = i["content_type"]
                ukuran = round((i["size"] / (1024**2)), 2)
                link_donlod = i["browser_download_url"]

                break
        print()

        print(f"Tag name: {nama_tag}")
        print(f"Asset found: {jumlah_asset}")
        print(f"Published on: {waktu_publish}")
        print(f"Update URL: {link_data}")
        print((len(link_data) + 14) * "=")
        print(f"File name: {nama_file}")
        print(f"Content type: {tipe_konten}")
        print(f"Size: {ukuran} mb")
        print(f"File URL: {link_donlod}")

        with requests.get(link_donlod, stream=True, timeout=5) as mind_request:
            mind_request.raise_for_status()
            total_size = int(mind_request.headers.get("content-length", 0))
            BLOCK_SIZE = 1024  # 1 KB

            with tqdm(total=total_size, unit="B", unit_scale=True, desc=nama_file) as bar:
                with open(nama_file, "wb") as f:
                    for chunk in mind_request.iter_content(chunk_size=BLOCK_SIZE):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

        print(f"{nama_file} Downloaded successfully.")

        os.remove(file_mindustry[0])
        print(f"{file_mindustry[0]} removed.")

file_mindustry = [f for f in os.listdir() if "Mindustry-BE-Desktop" in f and f.endswith(".jar")]
if file_mindustry:
    nama_file_updated = max(file_mindustry, key=os.path.getmtime)

    terakhir_update = os.path.getmtime(nama_file_updated)
    days_ago = int((waktu_skarang - terakhir_update) // (60 * 60 * 24))
    print("Last updated date:", time.strftime('%d-%m-%Y', time.localtime(terakhir_update)))
    print(f"{days_ago} days ago")

    print(f"{nama_file_updated} will be opened")

    print("in 3 seconds...")
    time.sleep(1)
    print("in 2 seconds...")
    time.sleep(1)
    print("in 1 seconds...")
    time.sleep(1)

    subprocess.run(["java", "-jar", nama_file_updated], check=False)
else:
    print("No Mindustry file found, please re run the program if you have internet connection.")
    print("If you still see this message, please report the issue to github.")
    print("https://github.com/xpossed-you/mindustry-bleeding-edge-launcher")

print("guddddbye...")

# akhir file mindustry-be-updater.py
