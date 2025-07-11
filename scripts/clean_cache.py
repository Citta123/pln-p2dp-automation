import os
import shutil
import sys
from scripts.logger import setup_logger


def clean_python_cache(project_root):
    base_dir = os.path.dirname(__file__)
    logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))
    logger.debug(f"Memulai proses pembersihan cache pada path: {project_root}")

    # Menghapus direktori __pycache__
    for root, dirs, _ in os.walk(project_root, topdown=True):
        if '__pycache__' in dirs:
            dir_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(dir_path)
                logger.info(f"Deleted cache directory: {dir_path}")
            except Exception as e:
                logger.error(f"Error saat menghapus cache directory {dir_path}: {e}")

    # Menghapus file dpm_prabayar.csv
    csv_file_path = os.path.join(base_dir, '..', 'data', 'dpm_prabayar.csv')
    logger.debug(f"Path file CSV: {csv_file_path}")
    if os.path.isfile(csv_file_path):
        try:
            os.remove(csv_file_path)
            logger.info(f"Deleted file: {csv_file_path}")
        except Exception as e:
            logger.error(f"Error saat menghapus file {csv_file_path}: {e}")
    else:
        logger.warning(f"File tidak ditemukan: {csv_file_path}")

    logger.debug("Proses pembersihan cache selesai.")


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    logger = setup_logger(os.path.join(base_dir, '..', 'log', 'project.log'))

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
        if not os.path.isdir(project_path):
            logger.error(f"Path yang diberikan tidak valid: {project_path}")
            sys.exit(1)
    else:
        # Default ke direktori induk dari skrip saat ini (project_root)
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    clean_python_cache(project_path)
