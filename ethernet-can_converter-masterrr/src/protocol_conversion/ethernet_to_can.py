"""
Module de conversion Ethernet vers CAN.

Permet de:
- Parser les trames Ethernet contenant des messages CAN
- Convertir les données en messages CAN valides
- Gérer le padding et les trames multiples
"""

import can
import struct
from scapy.all import Raw

# Définition des flags CAN
CAN_EFF_FLAG = 0x80000000  # Trame étendue

class EthernetToCan:
    """Classe pour la conversion de trames Ethernet vers messages CAN."""
    
    def extraction_ethernet_to_can(self, packet):
        """
        Extrait les messages CAN d'une trame Ethernet.
        
        Args:
            packet: Paquet Ethernet contenant des messages CAN
            
        Returns:
            list: Liste de messages CAN extraits
        """
        payload = bytes(packet[Raw])
        messages_can = []
        offset = 0

        while offset < len(payload):
            if offset + 4 > len(payload):
                break  

            can_id_raw = struct.unpack('!I', payload[offset:offset + 4])[0]
            is_extended = bool(can_id_raw & CAN_EFF_FLAG)
            
            if is_extended:
                can_id = can_id_raw & 0x1FFFFFFF
            else:
                can_id = can_id_raw & 0x7FF
            offset += 4
            print(hex(can_id))

            if offset + 1 > len(payload):
                break  

            dlc = struct.unpack('!B', payload[offset:offset + 1])[0]
            offset += 1

            if offset + dlc > len(payload):
                break  

            data = payload[offset:offset + dlc]
            offset += dlc
            message = can.Message(arbitration_id=can_id, data=data, dlc=dlc, is_extended_id=is_extended)
            messages_can.append(message)

            if all(b == 0 for b in payload[offset:]):
                break  

        return messages_can
