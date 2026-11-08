#load_config
import json

class LoadConfig:
    @staticmethod
    def load_config(config_path):
        with open(config_path, "r") as file:
            config = json.load(file)
        
        config["pc_mac_bytes"] = bytes.fromhex(config["pc_mac_bytes"])
        config["raspberry_mac_bytes"] = bytes.fromhex(config["raspberry_mac_bytes"])
        config["eth_type_can"] = bytes.fromhex(config["eth_type_can"])
        
        return config
