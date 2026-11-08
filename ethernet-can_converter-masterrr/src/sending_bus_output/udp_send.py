"""
Module pour l'envoi de paquets UDP.

Permet de:
- Envoyer des données via UDP
- Journaliser les paquets envoyés
- Gérer proprement la socket
"""

import socket
import struct
import logging

class UdpSend:
    """Classe pour l'envoi de paquets UDP."""
    
    def __init__(self, ip_dest, port, logger):
        """
        Initialise l'émetteur UDP.
        
        Args:
            ip_dest (str): Adresse IP de destination
            port (int): Port de destination
            logger: Instance de logger pour la journalisation
        """
        self.ip_dest = ip_dest
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logger = logger

    def close(self):
        """Ferme proprement la socket UDP."""
        self.sock.close()
        
    def send(self, udp_payload, can_id, dlc, data):
        """
        Envoie un paquet UDP et journalise l'action.
        
        Args:
            udp_payload: Données UDP à envoyer
            can_id: Identifiant CAN original (pour le logging)
            dlc: Longueur des données CAN (pour le logging)
            data: Données CAN originales (pour le logging)
        """
        self.sock.sendto(udp_payload, (self.ip_dest, self.port))
        self.logger.info(f"Envoyé en UDP: ID={hex(can_id)}, DLC={dlc}, Data={data.hex()}")
