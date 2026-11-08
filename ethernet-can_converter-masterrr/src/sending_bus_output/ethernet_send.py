"""
Module pour l'envoi de trames Ethernet.

Permet de:
- Envoyer des trames Ethernet brutes
- Journaliser les trames envoyées
- Gérer proprement la socket
"""

import socket
import struct
import logging

class EthernetSend:
    """Classe pour l'envoi de trames Ethernet."""
    
    def __init__(self, eth_interface, logger):
        """
        Initialise l'émetteur Ethernet.
        
        Args:
            eth_interface (str): Interface Ethernet à utiliser
            logger: Instance de logger pour la journalisation
        """
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x88B5))
        self.sock.bind((eth_interface, 0))
        self.logger = logger

    def close(self):
        """Ferme proprement la socket Ethernet."""
        self.sock.close()

    def send(self, eth_frame, can_id, dlc, data):
        """
        Envoie une trame Ethernet et journalise l'action.
        
        Args:
            eth_frame: Trame Ethernet brute à envoyer
            can_id: Identifiant CAN original (pour le logging)
            dlc: Longueur des données CAN (pour le logging)
            data: Données CAN originales (pour le logging)
        """
        self.sock.send(eth_frame)
        self.logger.info(f"Envoyé en Ethernet: ID={hex(can_id)}, DLC={dlc}, Data={data.hex()}")
