"""
Module principal du projet de conversion CAN/Ethernet/UDP/SOMEIP pour Raspberry Pi.

Ce module orchestre tous les composants du système :
- Sniffing des bus CAN et Ethernet
- Conversion entre protocoles
- Envoi des données sur les différents bus
- Gestion de la configuration et des logs
"""

from pathlib import Path
from sniffing.can_sniffer import SniffCAN
from sniffing.ethernet_sniffer import SniffEthernet
from protocol_conversion.can_to_ethernet import CantoEthernet
from protocol_conversion.can_to_udp import CantoUdp
from protocol_conversion.ethernet_to_can import EthernetToCan
from protocol_conversion.can_to_someip import CantoSomeip
from sending_bus_output.can_send import CanSend
from sending_bus_output.ethernet_send import EthernetSend
from sending_bus_output.udp_send import UdpSend
from file_handling.Load_config import LoadConfig
from file_handling.sendipmac import RaspberryPiServer
from upload_output.can_to_someip_logger import add_event_to_someip_json 
import threading
import time
import json
import os
from file_handling.logger_init import initialize_logger
from file_handling.detect import build_config, save_config, add_config_fields
from converterdecoder import CanDecoder

# Chemin du fichier de logs
log_file_path = "logs/program_logs.log"  
#logger = initialize_logger(log_file_path)
can_sniffer = None  # Variable globale pour le sniffer CAN

def pause_can_sniffer(duration_sec=0.05):
    """
    Met temporairement en pause le sniffer CAN.
    
    Args:
        duration_sec (float): Durée de la pause en secondes
    """
    global can_sniffer
    can_sniffer.stop()
    time.sleep(duration_sec)
    can_sniffer.start()
    

def handle_can_packet(packet, mode):
    """
    Gère les paquets CAN reçus en fonction du mode de conversion.
    
    Args:
        packet: Paquet CAN reçu
        mode (str): Mode de conversion ("ETHERNET", "UDP" ou "SOMEIP")
    """
    if mode == "ETHERNET":
        eth_frame, can_id, dlc, data = eth_converter.extraction_can(packet)
        eth_sender.send(eth_frame, can_id, dlc, data)
    elif mode == "UDP":
        udp_frame, can_id, dlc, data = udp_converter.extraction_udp(packet)
        udp_sender.send(udp_frame, can_id, dlc, data)
    elif mode == "SOMEIP":
        udp_frame, can_id, dlc, data = udp_converter.extraction_udp(packet)
        udp_sender.send(udp_frame, can_id, dlc, data)
        can_id, dlc, data = someip_cnverter.extraction_can(packet)
        add_event_to_someip_json(can_id, data, can_decoder)
    

def handle_ethernet_packet(packet):
    """
    Gère les paquets Ethernet reçus et les convertit en messages CAN.
    
    Args:
        packet: Paquet Ethernet reçu
    """
    pause_can_sniffer(0.05)
    messages_can = can_converter.extraction_ethernet_to_can(packet)
    can_sender.process_ethernet_frame(messages_can)
    

if __name__ == "__main__":
    try:
        # Initialisation de la configuration
        config = build_config()
        save_config(config)
        
        # Démarrage du serveur pour récupérer les infos du PC
        server = RaspberryPiServer()
        result = server.start()
        adrippc, macpc, mode = result
        
        # Initialisation du logger
        logger = initialize_logger(log_file_path, adrippc, 5006)
        macpcbytes = macpc.replace(":", "").upper() if macpc else ""
        
        # Mise à jour de la configuration
        add_config_fields({
            "pc_mac": macpc,
            "pc_mac_bytes": macpcbytes,
            "adr_ip_pc": adrippc
        })
        
        print(mode)
        if mode not in ["ETHERNET", "UDP", "SOMEIP"]:
            logger.warning("Mode invalide. Par défaut, Ethernet est utilisé.")
            mode = "ETHERNET"
        
        # Chargement de la configuration
        load = LoadConfig()
        BASE_DIR = Path(__file__).resolve().parent.parent
        CONFIG_FILE = BASE_DIR / "resources" / "default_configuration.json"
        config = load.load_config(CONFIG_FILE)
        
        # Initialisation du décodeur CAN
        dbc_path = "/home/pi1/ethernet-can_converter-masterrr/src/wapper.dbc"
        can_decoder = CanDecoder(dbc_path=dbc_path)
        
        # Récupération des paramètres de configuration
        can_interface = config["can_interface"]
        eth_interface = config["eth_interface"]
        broadcast_mac = config["broadcast_mac"]
        raspberry_mac = config["raspberry_mac"]
        pc_mac = config["pc_mac"]
        adr_ip_pc = config["adr_ip_pc"]
        adr_ip_raspberry = config["adr_ip_raspberry"]
        port = config["port"]
        pc_mac_bytes = config["pc_mac_bytes"]
        raspberry_mac_bytes = config["raspberry_mac_bytes"]
        eth_type_can = config["eth_type_can"]
        
        # Initialisation des composants
        can_sniffer = SniffCAN(can_interface, lambda pkt: handle_can_packet(pkt, mode), logger)
        eth_sniffer = SniffEthernet(eth_interface, handle_ethernet_packet, pc_mac, broadcast_mac, 
                                  adr_ip_pc, adr_ip_raspberry, logger)
        
        can_converter = EthernetToCan()
        eth_converter = CantoEthernet(eth_interface, pc_mac_bytes, raspberry_mac_bytes, eth_type_can)
        udp_converter = CantoUdp()
        someip_cnverter = CantoSomeip()
        
        can_sender = CanSend(can_interface, logger, can_decoder)
        eth_sender = EthernetSend(eth_interface, logger)
        udp_sender = UdpSend(adr_ip_pc, port, logger)

        # Démarrage des threads de sniffing
        can_thread = threading.Thread(target=can_sniffer.start, daemon=True)
        eth_thread = threading.Thread(target=eth_sniffer.start, daemon=True)

        can_thread.start()
        eth_thread.start()
        
        # Boucle principale
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Arrêt du programme...")

    finally:
        logger.info("Fermeture des sockets et sniffers...")
        try:
            eth_sender.close()
            udp_sender.close()
        except AttributeError:
            pass

        logger.info("Programme arrêté proprement.")
