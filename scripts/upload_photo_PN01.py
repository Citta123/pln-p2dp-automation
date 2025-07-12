import requests
from scripts.logger import setup_logger
import time
import os
from concurrent.futures import ThreadPoolExecutor

base_dir = os.path.dirname(__file__)
logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))


def upload_entry(entry):
    API_URL_POST = "http://API"

    headers = {
        'User-Agent': "Apache-HttpClient/UNAVAILABLE (java 1.4)",
        'Connection': "Keep-Alive",
        'Content-Type': "application/x-www-form-urlencoded"
    }

    if 'filefoto_PN01' not in entry:
        logger.error(f"Foto PN01 untuk ID Pelanggan {entry['idpel']} tidak tersedia.")
        return  # Lewati entri ini

    payload = {
        "idpel": entry['idpel'],
        "blth": entry['blth'],
        "unitup": "52260",
        "namafile": entry['namafoto_PN01'],
        "filefoto": entry['filefoto_PN01'],
        "transaksiby": entry['transaksiby']  # Diubah dari "52260.d08" menjadi entry['transaksiby']
    }

    logger.debug(f"Filled Photo PN01 entry: {payload}")

    retries = 3
    backoff = 5  # detik
    for attempt in range(retries):
        try:
            response = requests.post(API_URL_POST, data=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Foto PN01 berhasil diupload untuk ID Pelanggan: {entry['idpel']}")
            break  # Berhasil, keluar dari retry loop
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error saat mengupload foto PN01 untuk ID Pelanggan {entry['idpel']}: {http_err}")
        except Exception as err:
            logger.error(f"Error saat mengupload foto PN01 untuk ID Pelanggan {entry['idpel']}: {err}")

        if attempt < retries - 1:
            logger.info(f"Mencoba kembali mengupload foto PN01 untuk ID Pelanggan {entry['idpel']} setelah {backoff} detik...")
        else:
            logger.error(f"Gagal mengupload foto PN01 untuk ID Pelanggan {entry['idpel']} setelah {retries} percobaan.")


def upload_photo_PN01(data):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(upload_entry, data)
