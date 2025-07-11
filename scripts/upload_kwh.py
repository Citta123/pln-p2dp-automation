import requests
import os
from scripts.logger import setup_logger
import time

base_dir = os.path.dirname(__file__)
logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))


def upload_kwh(data):
    API_URL_POST = "http://portalapp.iconpln.co.id:8000/api-v2-acmt-prod/mobile/setStanPrabayar"

    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 9 Pro MIUI/V12.0.3.0.QJZMIXM)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
    }

    with requests.Session() as session:
        session.headers.update(headers)
        for entry in data:
            payload = {
                "tglbaca": entry['tglbaca'],
                "sisakwh": entry['sisakwh'],
                "kwhkomulatif": entry['kwhkomulatif'],
                "latitude": entry['latitude'],
                "jumlah_terminal": entry['jumlah_terminal'],
                "indikatordisplay": entry['indikatordisplay'],
                "keypad": entry['keypad'],
                "cosphi": entry['cosphi'],
                "lcd": entry['lcd'],
                "kdbaca2": entry['kdbaca2'],
                "kdbaca3": entry['kdbaca3'],
                "namafoto": entry['namafoto_PN01'],  # Assuming 'namafoto_PN01' is the correct key from fill_kwh.py
                "blth": entry['blth'],
                "tegangan": entry['tegangan'],
                "tutup_meter": entry['tutup_meter'],
                "longitude": entry['longitude'],
                "arus": entry['arus'],
                "tarifindex": entry['tarifindex'],
                "kondisi_segel": entry['kondisi_segel'],
                "relay": entry['relay'],
                "indikator_temper": entry['indikator_temper'],
                "akurasi": entry['akurasi'],
                "idpel": entry['idpel'],
                "powerlimit": entry['powerlimit'],
                "transaksiby": entry['transaksiby'],
                "status_temper": entry['status_temper'],
                "kdbaca": entry['kdbaca'],
                "akses_kwh_meter": "1"  # ADDED PARAMETER
            }

            retries = 3
            backoff = 5  # detik
            for attempt in range(retries):
                try:
                    response = session.post(API_URL_POST, data=payload)
                    response.raise_for_status()
                    logger.info(f"Data kwh berhasil diupload untuk ID Pelanggan: {entry['idpel']}")
                    break  # Berhasil, keluar dari retry loop
                except requests.exceptions.HTTPError as http_err:
                    logger.error(f"HTTP error saat mengupload data untuk ID Pelanggan {entry['idpel']}: {http_err}")
                except Exception as err:
                    logger.error(f"Error saat mengupload data untuk ID Pelanggan {entry['idpel']}: {err}")

                if attempt < retries - 1:
                   logger.info(f"Mencoba kembali mengupload foto PN02 untuk ID Pelanggan {entry['idpel']} setelah {backoff} detik...")
                else:
                    logger.error(f"Gagal mengupload data untuk ID Pelanggan {entry['idpel']} setelah {retries} percobaan.")
