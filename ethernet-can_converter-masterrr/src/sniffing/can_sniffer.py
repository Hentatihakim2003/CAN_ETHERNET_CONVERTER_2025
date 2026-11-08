"""
Module pour le sniffing des messages CAN.

Permet de:
- Capturer les messages CAN en temps réel
- Démarrer/arrêter le sniffing
- Transmettre les messages capturés à un callback
"""

import logging
from scapy.all import sniff
import threading

class SniffCAN:
    """Classe pour le sniffing des messages CAN."""
    
    def __init__(self, interface, callback, logger):
        """
        Initialise le sniffer CAN.
        
        Args:
            interface (str): Interface CAN à surveiller
            callback (function): Fonction à appeler pour chaque message capturé
            logger: Instance de logger pour la journalisation
        """
        self.interface = interface
        self.callback = callback
        self.logger = logger
        self.running = False
        self.sniffer_thread = None

    def start(self):
        """Démarre le thread de sniffing."""
        self.running = True
        self.sniffer_thread = threading.Thread(target=self.sniff_loop)
        self.sniffer_thread.start()

    def sniff_loop(self):
        """Boucle principale de sniffing."""
        from scapy.all import sniff
        while self.running:
            sniff(iface=self.interface, prn=self.callback, store=False, timeout=1)

    def stop(self):
        """Arrête le sniffing et attend la fin du thread."""
        self.running = False
        if self.sniffer_thread:
            self.sniffer_thread.join()
