import os
import json
import netifaces
import subprocess

def get_mac(interface):
    try:
        with open(f"/sys/class/net/{interface}/address", "r") as f:
            return f.read().strip()
    except:
        return None

def get_ip(interface):
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except:
        return None

def detect_interfaces():
    interfaces = os.listdir('/sys/class/net/')
    can_interface = next((i for i in interfaces if i.startswith("can")), None)
    eth_interface = next((i for i in interfaces if i.startswith("eth") or i.startswith("en")), None)
    return can_interface, eth_interface

def get_pc_mac_ip_from_arp():
    try:
        result = subprocess.check_output("arp -n", shell=True).decode()
        lines = result.split('\n')
        for line in lines:
            if "ether" in line or ":" in line:
                parts = line.split()
                if len(parts) >= 3:
                    return parts[0], parts[2]  # IP, MAC
    except:
        pass
    return None, None

def build_config():
    can_interface, eth_interface = detect_interfaces()
    raspberry_mac = get_mac(eth_interface)
    adr_ip_raspberry = get_ip(eth_interface)
    adr_ip_pc, pc_mac = get_pc_mac_ip_from_arp()

    config = {
        "can_interface": can_interface,
        "eth_interface": eth_interface,
        "broadcast_mac": "ff:ff:ff:ff:ff:ff",
        "raspberry_mac": raspberry_mac,
        "pc_mac": pc_mac,
        "adr_ip_pc": adr_ip_pc,
        "adr_ip_raspberry": adr_ip_raspberry,
        "port": 5005,
        "raspberry_mac_bytes": raspberry_mac.replace(":", "").upper() if raspberry_mac else "",
        "pc_mac_bytes": pc_mac.replace(":", "").upper() if pc_mac else "",
        "eth_type_can": "88B5"
    }

    return config

def save_config(config):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # /projet
    config_path = os.path.join(base_dir, 'resources', 'default_configuration.json')

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

config=build_config
print("config creer avec succes")
save_config(config)
