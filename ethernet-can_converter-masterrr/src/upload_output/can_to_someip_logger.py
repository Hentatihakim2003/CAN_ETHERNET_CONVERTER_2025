"""
Module pour la journalisation des événements CAN vers un format SOME/IP JSON.

Permet de:
- Convertir les messages CAN en événements SOME/IP
- Maintenir un fichier JSON à jour avec les derniers états
- Valider les données par rapport au fichier DBC
"""

import can
import json
from pathlib import Path
import logging

# Configuration du chemin du fichier JSON
JSON_PATH = Path("/home/pi1/ethernet-can_converter-masterrr/src/someip_config.json")
logger = logging.getLogger('can_to_someip_logger')
logger.setLevel(logging.INFO)

def add_event_to_someip_json(can_id, data_bytes, can_decoder):
    """
    Ajoute ou met à jour un événement dans le fichier SOME/IP JSON.
    
    Args:
        can_id: Identifiant CAN du message
        data_bytes: Données brutes du message CAN
        can_decoder: Instance de CanDecoder pour la validation
    """
    hex_value = f"0x{data_bytes.hex()}"
    
    # Vérifier si le message existe dans le DBC
    if not can_decoder.db or can_id not in [msg.frame_id for msg in can_decoder.db.messages]:
        logger.warning(f"CAN ID non trouvé dans le DBC: {hex(can_id)}")
        return

    decoded = can_decoder.decode(can_id, data_bytes)
    if not decoded or ("signal" in decoded and decoded["signal"] == "inconnu"):
        logger.warning(f"Décodage inconnu pour CAN ID: {hex(can_id)} avec data: {data_bytes.hex()}")
        return

    # Vérifier si la valeur décodée est valide selon le DBC
    try:
        msg = can_decoder.db.get_message_by_frame_id(can_id)
        signal = list(msg.signals)[0]  # On prend le premier signal
        if hasattr(signal, 'choices'):  # Si le signal a des valeurs définies
            decoded_value = decoded[signal.name]
            if decoded_value not in signal.choices.values():
                logger.warning(f"Valeur {decoded_value} non valide pour {signal.name}. Valeurs autorisées: {list(signal.choices.values())}")
                return
    except Exception as e:
        logger.error(f"Erreur lors de la validation des valeurs: {e}")
        return

    # Récupère le premier élément du dictionnaire décodé
    event_name, new_status = list(decoded.items())[0]
    new_status = str(new_status)
    print(new_status)

    event_id = can_id

    if not JSON_PATH.exists():
        logger.info(f"Le fichier {JSON_PATH} n'existe pas.")
        return

    try:
        with open(JSON_PATH, "r") as f:
            someip_config = json.load(f)

        service = someip_config["services"][0]
        events = service["events"]
        event_group = service["event_groups"][0]

        # Cherche si l'event existe déjà
        for event in events:
            if event["event_id"] == event_id:
                old_status = str(event["event_value"]["status"])
                
                # Vérifier si le statut a changé
                if old_status == new_status:
                    logger.info(f"Aucun changement: event_id={event_id}, status={new_status} (identique)")
                    return
                
                event["event_value"]["status"] = new_status
                logger.info(f"Mise à jour : event_id={event_id}, {old_status} → {new_status}")
                break
        else:
            # Ajoute un nouvel événement
            new_event = {
                "event_name": f"Event_{event_id}",
                "event_id": event_id,
                "event_name": event_name,
                "is_field": False,
                "is_reliable": False,
                "update_cycle": 0,
                "event_type": "event",
                "event_value": {
                    "status": new_status
                },
                "event_direction": "requestservice",
                "communication_type": "asynchronous"
            }
            events.append(new_event)
            event_group["event_ids"].append(event_id)
            logger.info(f"Ajout : event_id={event_id}, status={new_status}")

        # Écrire seulement si nécessaire (le return dans le cas identique empêche d'arriver ici si pas de changement)
        with open(JSON_PATH, "w") as f:
            json.dump(someip_config, f, indent=4)

    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage JSON: {e}")
    except Exception as e:
        logger.error(f"Erreur lors de l'écriture du fichier JSON: {e}")
