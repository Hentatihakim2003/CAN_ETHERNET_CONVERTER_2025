"""
Module pour le sniffing des paquets Ethernet.

Permet de:
- Capturer les paquets Ethernet spécifiques
- Filtrer les paquets selon des critères (MAC, IP, etc.)
- Transmettre les paquets valides à un handler
"""

from scapy.all import Raw
import logging
from scapy.all import sniff, Ether, IP, UDP

class SniffEthernet:
    """Classe pour le sniffing des paquets Ethernet."""
    
    def __init__(self, interface, handler, mac_pc, mac_rsp, ip_pc, ip_rsp, logger):
        """
        Initialise le sniffer Ethernet.
        
        Args:
            interface (str): Interface Ethernet à surveiller
            handler (function): Fonction de traitement des paquets
            mac_pc (str): Adresse MAC du PC à filtrer
            mac_rsp (str): Adresse MAC de la Raspberry Pi
            ip_pc (str): Adresse IP du PC
            ip_rsp (str): Adresse IP de la Raspberry Pi
            logger: Instance de logger pour la journalisation
        """
        self.interface = interface
        self.handler = handler
        self.mac_pc = mac_pc
        self.mac_rsp = mac_rsp
        self.ip_pc = ip_pc
        self.ip_rsp = ip_rsp
        self.logger = logger

    def packet_filter(self, packet):
        """
        Filtre les paquets Ethernet selon des critères spécifiques.
        
        Args:
            packet: Paquet réseau capturé
            
        Returns:
            bool: True si le paquet doit être traité, False sinon
        """
        if Ether in packet:
            if (
                (packet[Ether].src == self.mac_pc) and
                (packet[Ether].dst == self.mac_rsp) and (packet.haslayer(Raw)) and
                (packet[Ether].type == 0x88b5)
            ):
                return True
        
        if IP in packet and UDP in packet:
            if ((packet[IP].dst == self.ip_rsp) and (packet.haslayer(Raw) and (packet[UDP].dport == 5005)):
                return True

        return False

    def start(self):
        """Démarre le sniffing Ethernet."""
        self.logger.info(f"Démarrage du sniffing Ethernet sur {self.interface}")
        sniff(
            iface=self.interface, 
            prn=lambda pkt: self.handler(pkt) if self.packet_filter(pkt) else None, 
            store=False
        )
