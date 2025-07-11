from scripts.fetch_data import fetch_and_save_data
from scripts.fill_kwh import fill_kwh
from scripts.fill_photo_PN01 import fill_photo_PN01
from scripts.fill_photo_PN02 import fill_photo_PN02
from scripts.fill_photo_PN03 import fill_photo_PN03
from scripts.upload_kwh import upload_kwh
from scripts.upload_photo_PN01 import upload_photo_PN01
from scripts.upload_photo_PN02 import upload_photo_PN02
from scripts.upload_photo_PN03 import upload_photo_PN03
from scripts.logger import setup_logger
from scripts.clean_cache import clean_python_cache
from datetime import datetime
import os


def display_rbm_options(data):
    """
    Menampilkan opsi kategori kdrbm yang tersedia
    """
    rbm_categories = set(entry['kdrbm'] for entry in data)  # Mengambil semua kategori kdrbm unik
    print("Pilih kategori rbm yang akan diproses:")
    for idx, category in enumerate(sorted(rbm_categories), 1):
        print(f"{idx}. {category}")
    return sorted(rbm_categories)


def get_rbm_and_count(rbm_categories):
    """
    Meminta pengguna untuk memilih kategori rbm dan jumlah ID yang ingin diproses
    """
    try:
        # Meminta pilihan kategori
        rbm_choice = int(input("Masukkan nomor kategori KDRBM yang akan diproses: "))
        if rbm_choice < 1 or rbm_choice > len(rbm_categories):
            print("Pilihan tidak valid!")
            return None, None
        selected_rbm = rbm_categories[rbm_choice - 1]

        # Meminta jumlah ID pelanggan yang ingin diproses
        count = int(input(f"Masukkan jumlah ID pelanggan yang akan diproses untuk kategori {selected_rbm}: "))
        if count <= 0:
            print("Jumlah harus lebih dari 0!")
            return None, None

        return selected_rbm, count
    except ValueError:
        print("Input tidak valid!")
        return None, None


def main():
    # Inisialisasi Logger
    logger = setup_logger(os.path.join(os.path.dirname(__file__), 'log', 'project.log'))

    try:
        # 0. Input Username
        username = input("Masukkan username: ")
        if not username:
            username = "52260"  # Nilai default jika tidak diisi

        # 1. Tetapkan nilai default
        tgllogin = datetime.now().strftime('%m/%d/%Y')  # Nilai default tgllogin
        unitup = "52260"  # Nilai default unitup
        csv_filename = os.path.join(os.path.dirname(__file__), 'data', 'dpm_prabayar.csv')  # Nilai default csv_filename

        # 2. Ambil dan simpan data dari server
        data = fetch_and_save_data(
            username=username,
            tgllogin=tgllogin,
            unitup=unitup,
            csv_filename=csv_filename
        )
        logger.info("Data berhasil diambil dari server.")
        logger.debug(f"Data fetched: {data}")

        # 3. Ambil opsi kategori rbm
        rbm_categories = display_rbm_options(data)
        selected_rbm, count = get_rbm_and_count(rbm_categories)
        logger.debug(f"Selected RBM: {selected_rbm}, Count: {count}")

        if selected_rbm and count:
            # 4. Filter data berdasarkan kategori kdrbm yang dipilih
            filtered_data = [entry for entry in data if entry['kdrbm'] == selected_rbm][:count]
            logger.info(f"Data berhasil difilter untuk {selected_rbm} dengan {count} ID pelanggan.")
            logger.debug(f"Filtered data: {filtered_data}")

            # 5. Lanjutkan dengan pengisian KWH
            filled_kwh = fill_kwh(filtered_data, username)
            logger.debug(f"Filled KWH data: {filled_kwh}")

            # 6. Lanjutkan dengan pengisian foto
            filled_kwh = fill_photo_PN01(filled_kwh)
            filled_kwh = fill_photo_PN02(filled_kwh)
            filled_kwh = fill_photo_PN03(filled_kwh)

            # 7. Upload KWH dan foto
            upload_kwh(filled_kwh)
            upload_photo_PN01(filled_kwh)
            upload_photo_PN02(filled_kwh)
            upload_photo_PN03(filled_kwh)

            logger.info("Data berhasil diproses dan diupload.")

    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
        print(f"Terjadi kesalahan: {e}")

    finally:
        # Hapus cache python
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        clean_python_cache(project_path)
        logger.info("Cache Python telah dihapus.")


if __name__ == "__main__":
    main()
