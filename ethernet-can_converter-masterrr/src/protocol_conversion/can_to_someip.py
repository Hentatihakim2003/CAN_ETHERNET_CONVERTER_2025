"""
Module de conversion CAN vers SOME/IP.

Permet de:
- Parser les trames CAN
- Extraire les informations pour SOME/IP
- Préparer les données pour la journalisation SOME/IP
"""

import socket
import socket
import struct
import logging
from scapy.all import *

# Définition des flags CAN
CAN_EFF_FLAG = 0x80000000  # Trame étendue
CAN_RTR_FLAG = 0x40000000
CAN_ERR_FLAG = 0x20000000

class CantoSomeip:
    """Classe pour la conversion de messages CAN vers SOME/IP."""
    
    def __init__(self):
        """Initialise le convertisseur CAN vers SOME/IP."""
        pass

    def parse_can_frame(self, packet):
        """
        Parse une trame CAN brute.
        
        Args:
            packet: Paquet CAN brut
            
        Returns:
            dict: Dictionnaire contenant les informations parsées ou None si invalide
        """
        raw = bytes(packet)

        if len(raw) < 8:
            return None  # Trop court pour être une trame CAN complète

        # Extraire le champ ID brut
        can_id_raw = struct.unpack("<I", raw[0:4])[0]

        is_extended = bool(can_id_raw & CAN_EFF_FLAG)
        is_remote = bool(can_id_raw & CAN_RTR_FLAG)
        is_error = bool(can_id_raw & CAN_ERR_FLAG)

        # Extraire l'ID pur
        if is_extended:
            can_id = can_id_raw & 0x1FFFFFFF
        else:
            can_id = can_id_raw & 0x7FF

        dlc = raw[4]
        data = raw[8:8 + dlc]

        return {
            "id": can_id,
            "is_extended": is_extended,
            "dlc": dlc,
            "data": data,
            "is_remote": is_remote,
            "is_error": is_error,
        }

    def extraction_can(self, packet):
        """
        Extrait les données CAN pour SOME/IP.
        
        Args:
            packet: Paquet CAN à convertir
            
        Returns:
            tuple: (can_id, dlc, data) ou (None, None, None) si invalide
        """
        parsed = self.parse_can_frame(packet)
        if not parsed:
            return None, None, None  # Trame invalide

        can_id = parsed["id"]
        dlc = parsed["dlc"]
        data = parsed["data"]

        return can_id, dlc, data
