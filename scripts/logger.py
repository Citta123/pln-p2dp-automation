import logging
import os


def setup_logger(log_file):
    log_file = os.path.join(os.path.dirname(__file__), '..', log_file)
    logger = logging.getLogger('project_logger')
    logger.setLevel(logging.DEBUG)  # Set level to DEBUG to capture all messages

    # Buat handler untuk file log
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Buat handler untuk terminal (stdout)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # Set level to INFO to capture INFO and higher level messages

    # Buat formatter dan tambahkan ke handler
    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Tambahkan handler ke logger
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
