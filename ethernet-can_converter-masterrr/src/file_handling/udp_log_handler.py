#udploghandler
import logging
import socket

class UDPLogHandler(logging.Handler):
    def __init__(self, ip: str, port: int):
        super().__init__()
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        try:
            # Utilise le formatter attaché au handler
            if self.formatter:
                msg = self.format(record)
            else:
                msg = self.default_format(record)
            self.sock.sendto(msg.encode('utf-8'), (self.ip, self.port))
        except Exception as e:
            print(f"[Erreur UDPLogHandler] {e}")

    def default_format(self, record):
        return f"{record.levelname}: {record.getMessage()}"
