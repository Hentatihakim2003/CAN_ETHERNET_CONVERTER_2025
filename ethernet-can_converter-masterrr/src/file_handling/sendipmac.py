#sendipmac
import socket
import json
import os
import netifaces

class RaspberryPiServer:
    def __init__(self, port=5000, filename="received_info.json"):
        self.port = port
        self.filename = filename
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.port))  # Écoute sur toutes les interfaces

    def detect_interfaces(self):
        interfaces = os.listdir('/sys/class/net/')
        eth_interface = next((i for i in interfaces if i.startswith("eth") or i.startswith("en")), None)
        return eth_interface

    def get_ip(self, interface):
        try:
            return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        except Exception:
            return None

    def get_mac(self, interface):
        try:
            with open(f"/sys/class/net/{interface}/address", "r") as f:
                return f.read().strip()
        except Exception:
            return None

    def start(self):
        print("En attente d'une demande de découverte...")
        try:
            while True:
                data, address = self.sock.recvfrom(1024)
                request = json.loads(data.decode())

                eth_interface = self.detect_interfaces()
                if eth_interface is None:
                    print("Erreur : aucune interface Ethernet détectée.")
                    return None  # On ne ferme pas ici encore car le finally va gérer

                if request.get("request") == "discovery":
                    # Récupérer l'IP et la MAC de la Raspberry Pi
                    raspberry_info = {
                        "ip": self.get_ip(eth_interface),
                        "mac": self.get_mac(eth_interface)
                    }

                    ip_pc = request.get("pc_ip")
                    mac_pc = request.get("pc_mac")
                    mode = request.get("mode")

                    self.sock.sendto(json.dumps(raspberry_info).encode(), address)
                    print("Réponse envoyée à l'adresse", address)
                    return (ip_pc, mac_pc, mode)

                else:
                    print("Reçu un message inconnu. Attente d'un message 'discovery'...")

        finally:
            self.sock.close()  # Toujours fermer proprement à la fin

if __name__ == "__main__":
    server = RaspberryPiServer()
    result = server.start()
    if result:
        ip_pc, mac_pc, mode = result
        print(f"PC IP: {ip_pc}")
        print(f"PC MAC: {mac_pc}")
        print(f"Mode: {mode}")


