#logger_init
from file_handling.udp_log_handler import UDPLogHandler
import logging
  # <== Ajoute cette ligne

def initialize_logger(file_path: str, udp_ip: str = None, udp_port: int = None) -> logging.Logger:
    general_logger = logging.getLogger()
    general_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')

    file_handler = logging.FileHandler(file_path, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    general_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    general_logger.addHandler(stream_handler)

    # 🔥 Ajoute le handler UDP si nécessaire
    if udp_ip and udp_port:
        udp_handler = UDPLogHandler(udp_ip, udp_port)
        udp_handler.setLevel(logging.DEBUG)
        udp_handler.setFormatter(formatter)
        general_logger.addHandler(udp_handler)

    return general_logger
