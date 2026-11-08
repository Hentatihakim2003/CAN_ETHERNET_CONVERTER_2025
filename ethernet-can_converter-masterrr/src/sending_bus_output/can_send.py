"""
Module pour l'envoi de messages CAN.

Permet de:
- Envoyer des messages sur le bus CAN
- Journaliser les messages envoyés
- Mettre à jour les événements SOME/IP
"""

import struct
import logging
import can
from upload_output.can_to_someip_logger import add_event_to_someip_json 

class CanSend:
    """Classe pour l'envoi de messages CAN."""
    
    def __init__(self, can_interface, logger, can_decoder):
        """
        Initialise l'émetteur CAN.
        
        Args:
            can_interface (str): Interface CAN à utiliser
            logger: Instance de logger pour la journalisation
            can_decoder: Instance de CanDecoder pour la conversion SOME/IP
        """
        self.bus = can.interface.Bus(channel=can_interface, bustype="socketcan")
        self.logger = logger
        self.can_decoder = can_decoder

    def send(self, message, i):
        """
        Envoie un message CAN et journalise l'action.
        
        Args:
            message: Message CAN à envoyer
            i: Numéro de message pour le logging
        """
        self.bus.send(message)
        add_event_to_someip_json(message.arbitration_id, message.data, self.can_decoder)
        self.logger.info(f"[{i}] Envoyé en CAN: ID={hex(message.arbitration_id)}, DLC={message.dlc}, Data={message.data.hex()}")

    def process_ethernet_frame(self, message_can):
        """
        Traite une trame Ethernet convertie en messages CAN.
        
        Args:
            message_can: Liste de messages CAN à envoyer
        """
        i = 0
        for message in message_can:
            i = i + 1
            self.send(message, i)
