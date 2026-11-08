"""
Module pour le décodage des messages CAN à l'aide d'un fichier DBC.

Fournit des fonctionnalités pour:
- Charger un fichier de description DBC
- Décoder les messages CAN bruts en données structurées
"""

import cantools

class CanDecoder:
    """Classe pour décoder les messages CAN à partir d'un fichier DBC."""
    
    def __init__(self, dbc_path=None):
        """
        Initialise le décodeur CAN.
        
        Args:
            dbc_path (str, optional): Chemin vers le fichier DBC. Defaults to None.
        """
        self.db = None
        if dbc_path:
            self.load_dbc(dbc_path)

    def load_dbc(self, path):
        """
        Charge un fichier DBC pour le décodage.
        
        Args:
            path (str): Chemin vers le fichier DBC
            
        Returns:
            str: Message de confirmation ou d'erreur
        """
        try:
            self.db = cantools.database.load_file(path)
            message = f"Fichier DBC chargé avec succès : {len(self.db.messages)} messages"
            return message
        except Exception as e:
            error_message = f"Erreur de chargement du DBC : {e}"
            print(error_message)
            self.db = None
            return error_message

    def decode(self, can_id, data):
        """
        Décode un message CAN.
        
        Args:
            can_id: Identifiant CAN (peut être str ou int)
            data: Données CAN brutes (peut être str hex ou bytes)
            
        Returns:
            dict: Données décodées ou {"signal": "inconnu"} si échec
        """
        if not self.db:
            return {"signal": "inconnu"}

        try:
            if isinstance(can_id, str):
                can_id = int(can_id, 16) if can_id.startswith('0x') else int(can_id)

            data = bytes.fromhex(data.replace(' ', '')) if isinstance(data, str) else data

            msg = self.db.get_message_by_frame_id(can_id)

            if len(data) < msg.length:
                data += b'\x00' * (msg.length - len(data))

            decoded = self.db.decode_message(can_id, data)

            if not decoded:
                return {"signal": "inconnu"}
            else:
                return decoded

        except (KeyError, AttributeError):
            return {"signal": "inconnu"}
        except Exception as e:
            print(f"Erreur lors du décodage : {e}")
            return {"signal": "inconnu"}
