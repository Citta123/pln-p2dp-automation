import requests
import csv
import os
from scripts.logger import setup_logger

base_dir = os.path.dirname(__file__)
logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))


def fetch_and_save_data(username, tgllogin, unitup, csv_filename):
    API_URL_GET = "http://API"

    payload = {
        'username': username,
        'tgllogin': tgllogin,  # Format: MM/DD/YYYY
        'unitup': unitup
    }

    headers = {
        'User-Agent': "Apache-HttpClient/UNAVAILABLE (java 1.4)",
        'Connection': "Keep-Alive",
        'Content-Type': "application/x-www-form-urlencoded"
    }

    logger.debug(f"Payload: {payload}")
    logger.debug(f"Headers: {headers}")

    try:
        response = requests.post(API_URL_GET, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info("Data berhasil diambil dari server.")
        logger.debug(f"Response data: {data}")

        # Menyimpan data ke CSV
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        fieldnames = ['idpel', 'blth', 'kdrbm', 'daya']
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for pelanggan in data.get('stan', []):
                writer.writerow({
                    'idpel': pelanggan.get('idpel', ''),
                    'blth': pelanggan.get('blth', ''),
                    'kdrbm': pelanggan.get('kdrbm', ''),
                    'daya': pelanggan.get('daya', '')
                })
        logger.debug(f"Data berhasil disimpan ke {csv_filename}")

        return data.get('stan', [])  # Tambahkan ini untuk mengembalikan data

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error saat mengambil data: {http_err}")
    except Exception as err:
        logger.error(f"Error saat mengambil data: {err}")
