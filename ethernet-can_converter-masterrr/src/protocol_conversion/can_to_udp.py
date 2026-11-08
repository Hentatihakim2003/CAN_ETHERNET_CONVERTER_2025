"""
Module de conversion CAN vers UDP.

Permet de:
- Parser les trames CAN
- Convertir les messages CAN en paquets UDP
- Gérer les flags CAN (étendu, remote, erreur)
"""

import socket
import struct
import logging

# Définition des flags CAN
CAN_EFF_FLAG = 0x80000000  # Trame étendue
CAN_RTR_FLAG = 0x40000000
CAN_ERR_FLAG = 0x20000000

class CantoUdp:
    """Classe pour la conversion de messages CAN vers UDP."""
    
    def extraction_udp(self, packet):
        """
        Extrait les données CAN et construit un payload UDP.
        
        Args:
            packet: Paquet CAN à convertir
            
        Returns:
            tuple: (udp_payload, can_id, dlc, data)
        """
        raw_data = bytes(packet)
        can_id_raw = struct.unpack("<I", raw_data[0:4])[0]
        is_extended = bool(can_id_raw & CAN_EFF_FLAG)
        is_remote = bool(can_id_raw & CAN_RTR_FLAG)
        is_error = bool(can_id_raw & CAN_ERR_FLAG)
        
        if is_extended:
            can_id = can_id_raw & 0x1FFFFFFF
        else:
            can_id = can_id_raw & 0x7FF
            
        dlc = raw_data[4]
        data = raw_data[8:8+dlc]
        udp_payload = struct.pack("!IB", can_id_raw, dlc) + data.ljust(8, b'\x00')
        return (udp_payload, can_id, dlc, data)
