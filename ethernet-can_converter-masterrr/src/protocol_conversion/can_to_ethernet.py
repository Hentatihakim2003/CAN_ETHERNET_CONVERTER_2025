"""
Module de conversion CAN vers Ethernet.

Permet de:
- Parser les trames CAN
- Convertir les messages CAN en trames Ethernet
- Gérer les flags CAN (étendu, remote, erreur)
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

class CantoEthernet:
    """Classe pour la conversion de messages CAN vers Ethernet."""
    
    def __init__(self, eth_interface, pc_mac, raspberry_mac, eth_type_can):
        """
        Initialise le convertisseur.
        
        Args:
            eth_interface (str): Interface Ethernet à utiliser
            pc_mac: Adresse MAC du PC en bytes
            raspberry_mac: Adresse MAC de la Raspberry Pi en bytes
            eth_type_can: Type Ethernet pour les trames CAN
        """
        self.pc_mac = pc_mac
        self.raspberry_mac = raspberry_mac
        self.eth_type_can = eth_type_can

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
            "id": can_id_raw,
            "id_can": can_id, 
            "is_extended": is_extended,
            "dlc": dlc,
            "data": data,
            "is_remote": is_remote,
            "is_error": is_error,
        }

    def extraction_can(self, packet):
        """
        Extrait les données CAN et construit une trame Ethernet.
        
        Args:
            packet: Paquet CAN à convertir
            
        Returns:
            tuple: (trame_ethernet, can_id, dlc, data) ou (None, None, None, None) si invalide
        """
        parsed = self.parse_can_frame(packet)
        if not parsed:
            return None, None, None, None  # Trame invalide

        can_id = parsed["id"]
        dlc = parsed["dlc"]
        data = parsed["data"]
        
        id_c = parsed["id_can"]
        # Construction de la trame Ethernet avec padding si besoin
        eth_frame = (
            self.pc_mac +
            self.raspberry_mac +
            self.eth_type_can +
            struct.pack("!IB", can_id, dlc) +
            data.ljust(8, b'\x00')  # Remplissage à 8 octets si nécessaire
        )

        return eth_frame, id_c, dlc, data
