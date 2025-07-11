import os
import base64
from scripts.logger import setup_logger


def generate_namafoto(blth, idpel, prefix):
    from datetime import datetime, timedelta
    import random
    start_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
    random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
    random_time = (start_time + timedelta(seconds=random_seconds)).strftime('%H%M%S')
    return f"{blth}_{idpel}_{datetime.now().strftime('%Y%m%d')}_{random_time}_52260_{prefix}.jpg"


def fill_photo_PN02(data):
    base_dir = os.path.dirname(__file__)
    logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))
    photo_path = os.path.join(base_dir, '..', 'photos', 'PN02', '2.jpg')

    if not os.path.exists(photo_path):
        logger.error(f"Foto PN02 tidak ditemukan di {photo_path}")
        return data  # Kembali tanpa mengubah data

    try:
        with open(photo_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        for entry in data:
            try:
                blth = entry['blth']
                idpel = entry['idpel']
            except KeyError as e:
                logger.error(f"Entry data kurang kunci yang diperlukan: {e}")
                continue  # Lewati entri ini dan lanjutkan ke entri berikutnya

            namafoto_PN02 = generate_namafoto(blth, idpel, "PN02")
            entry['namafoto_PN02'] = namafoto_PN02
            entry['filefoto_PN02'] = encoded_string
            entry['transaksiby'] = entry.get('transaksiby', '52260.d08')  # Pastikan 'transaksiby' ada

        logger.info("Foto PN02 berhasil diisi ke data.")
    except Exception as e:
        logger.error(f"Error saat mengonversi foto PN02: {e}")

    return data
