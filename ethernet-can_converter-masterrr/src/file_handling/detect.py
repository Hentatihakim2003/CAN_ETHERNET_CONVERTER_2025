"""
Module de détection des interfaces et configuration.

Permet de:
- Détecter les interfaces CAN et Ethernet disponibles
- Récupérer les adresses MAC et IP
- Construire et sauvegarder une configuration par défaut
"""

import os
import json
import netifaces
import subprocess

def get_mac(interface):
    """
    Récupère l'adresse MAC d'une interface.
    
    Args:
        interface (str): Nom de l'interface
        
    Returns:
        str: Adresse MAC ou None si erreur
    """
    try:
        with open(f"/sys/class/net/{interface}/address", "r") as f:
            return f.read().strip()
    except:
        return None

def get_ip(interface):
    """
    Récupère l'adresse IP d'une interface.
    
    Args:
        interface (str): Nom de l'interface
        
    Returns:
        str: Adresse IP ou None si erreur
    """
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except:
        return None

def detect_interfaces():
    """
    Détecte les interfaces CAN et Ethernet disponibles.
    
    Returns:
        tuple: (can_interface, eth_interface) ou (None, None) si non trouvées
    """
    interfaces = os.listdir('/sys/class/net/')
    can_interface = next((i for i in interfaces if i.startswith("can")), None)
    eth_interface = next((i for i in interfaces if i.startswith("eth") or i.startswith("en")), None)
    return can_interface, eth_interface

def build_config():
    """
    Construit une configuration par défaut basée sur les interfaces détectées.
    
    Returns:
        dict: Configuration par défaut
    """
    can_interface, eth_interface = detect_interfaces()
    raspberry_mac = get_mac(eth_interface)
    adr_ip_raspberry = get_ip(eth_interface)

    config = {
        "can_interface": can_
