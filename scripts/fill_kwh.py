import random
from datetime import datetime, timedelta
from scripts.logger import setup_logger
import os

base_dir = os.path.dirname(__file__)
logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))

# Mapping daya ke tarifindex dan powerlimit
DAYA_MAPPING = {
    450: {"tarifindex": "01", "powerlimit": 0.75},
    900: {"tarifindex": "02", "powerlimit": 1.53},
    1300: {"tarifindex": "03", "powerlimit": 2.31},
    1800: {"tarifindex": "04", "powerlimit": 3.09},
    2250: {"tarifindex": "05", "powerlimit": 3.87},
    2700: {"tarifindex": "06", "powerlimit": 4.65},
    3150: {"tarifindex": "07", "powerlimit": 5.43},
    4400: {"tarifindex": "08", "powerlimit": 7.58},
    5500: {"tarifindex": "09", "powerlimit": 9.48},
    6600: {"tarifindex": "10", "powerlimit": 11.37},
    7700: {"tarifindex": "11", "powerlimit": 13.27},
    12000: {"tarifindex": "12", "powerlimit": 20.67},
    14000: {"tarifindex": "13", "powerlimit": 24.11},
    22000: {"tarifindex": "14", "powerlimit": 37.85},
}


def find_closest_daya(daya, mapping):
    keys = sorted(mapping.keys())
    closest = min(keys, key=lambda x: (abs(x - daya), x))  # Jika jarak sama, pilih yang paling rendah
    return mapping[closest]


def fill_kwh(data, username):
    logger = setup_logger(os.path.join(os.path.dirname(__file__), '..', 'log', 'project.log'))
    filled_kwh = []
    try:
        for entry in data:
            idpel = entry['idpel']
            blth = entry['blth']
            kdrbm = entry['kdrbm']
            daya = int(entry['daya']) if entry['daya'].isdigit() else 0

            logger.debug(f"Processing ID Pelanggan: {idpel}, BLTH: {blth}, KDRBM: {kdrbm}, Daya: {daya}")

            # 1. tglbaca: MM/DD/YYYY dengan waktu acak antara 07:00:00 hingga 16:00:00
            tglbaca = generate_tglbaca()

            # 2. sisakwh: random float antara 5.00 - 100.00
            sisakwh = round(random.uniform(5.00, 100.00), 2)

            # 3. kwhkomulatif: random int antara 1000 - 9000
            kwhkomulatif = random.randint(1000, 9000)

            # 4. latitude: acak dengan variasi sekitar 3-4 meter (~0.000027 - 0.000036 derajat)
            latitude = generate_latitude()

            # 5. jumlah_terminal: 5
            jumlah_terminal = 5

            # 6. indikatordisplay: 0
            indikatordisplay = 0

            # 7. keypad: "Normal"
            keypad = "Normal"

            # 8. cosphi: random float antara 3 - 40
            cosphi = round(random.uniform(3, 40), 2)

            # 9. lcd: "Normal"
            lcd = "Normal"

            # 10. kdbaca2 dan kdbaca3: kosong
            kdbaca2 = ""
            kdbaca3 = ""

            # 11. namafoto: {blth}_{idpel}_{YYYYMMDD}_{random_jam}_52260_PN0X.jpg
            namafoto_PN01 = generate_namafoto(blth, idpel, "PN01")

            # 12. blth: dari CSV (sudah ada)

            # 13. tegangan: random int antara 170 - 210
            tegangan = random.randint(170, 210)

            # 14. tutup_meter: 0
            tutup_meter = 0

            # 15. longitude: acak dengan variasi sekitar 3-4 meter (~0.000027 - 0.000036 derajat)
            longitude = generate_longitude()

            # 16. arus: random int antara 0 - 4
            arus = random.randint(0, 4)

            # 17. tarifindex: berdasarkan daya
            tarifindex = find_closest_daya(daya, DAYA_MAPPING)['tarifindex']

            # 18. kondisi_segel: "Ada"
            kondisi_segel = "Ada"

            # 19. relay: "Tutup"
            relay = "Tutup"

            # 20. indikator_temper: "Tidak Nyala"
            indikator_temper = "Tidak Nyala"

            # 21. akurasi: random int antara 3 - 19
            akurasi = random.randint(3, 19)

            # 22. idpel: dari CSV (sudah ada)

            # 23. powerlimit: berdasarkan daya
            powerlimit = find_closest_daya(daya, DAYA_MAPPING)['powerlimit']

            # 24. transaksiby: mengambil dari input username
            transaksiby = username

            # 25. status_temper: 0
            status_temper = 0

            # 26. kdbaca: "NORMAL"
            kdbaca = "NORMAL"

            # Menyusun payload
            payload = {
                "tglbaca": tglbaca,
                "sisakwh": sisakwh,
                "kwhkomulatif": kwhkomulatif,
                "latitude": latitude,
                "jumlah_terminal": jumlah_terminal,
                "indikatordisplay": indikatordisplay,
                "keypad": keypad,
                "cosphi": cosphi,
                "lcd": lcd,
                "kdbaca2": kdbaca2,
                "kdbaca3": kdbaca3,
                "namafoto": namafoto_PN01,
                "blth": blth,
                "tegangan": tegangan,
                "tutup_meter": tutup_meter,
                "longitude": longitude,
                "arus": arus,
                "tarifindex": tarifindex,
                "kondisi_segel": kondisi_segel,
                "relay": relay,
                "indikator_temper": indikator_temper,
                "akurasi": akurasi,
                "idpel": idpel,
                "powerlimit": powerlimit,
                "transaksiby": transaksiby,
                "status_temper": status_temper,
                "kdbaca": kdbaca
            }

            filled_kwh.append(payload)
            logger.debug(f"Filled KWH entry: {payload}")

        logger.info(f"Data kwh berhasil diisi untuk {len(filled_kwh)} pelanggan.")

    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")

    return filled_kwh


def generate_tglbaca():
    today = datetime.now()
    random_seconds = random.randint(7 * 3600, 16 * 3600 - 1)  # Detik dari 07:00:00 hingga 15:59:59
    tglbaca_datetime = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=random_seconds)
    return tglbaca_datetime.strftime('%m/%d/%Y %H:%M:%S')


def generate_latitude():
    # Menghasilkan variasi sekitar 3-4 meter (~0.000027 - 0.000036 derajat)
    variation = random.uniform(-0.000036, 0.000036)
    return round(-7.147495 + variation, 6)


def generate_longitude():
    # Menghasilkan variasi sekitar 3-4 meter (~0.000027 - 0.000036 derajat)
    variation = random.uniform(-0.000036, 0.000036)
    return round(109.2239833 + variation, 7)


def generate_namafoto(blth, idpel, jenis_pn):
    from datetime import datetime, timedelta
    import random
    start_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
    random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
    random_time = (start_time + timedelta(seconds=random_seconds)).strftime('%H%M%S')
    YYYYMMDD = datetime.now().strftime('%Y%m%d')
    return f"{blth}_{idpel}_{YYYYMMDD}_{random_time}_52260_{jenis_pn}.jpg"
