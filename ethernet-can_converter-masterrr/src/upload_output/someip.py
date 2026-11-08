import time
import json

class SomeipLogger:
    def __init__(self, can_id, dlc, data_bytes):
        self.can_id = can_id
        self.data1 = []
        self.dlc = dlc
        self.data_bytes = data_bytes  # données CAN brutes
        self.service_id = 0x1234
        self.method_id = 0x5678
        self.client_id = 0x1
        self.session_id = 0x01

    def log_someip_frame(self):
        data_hex = self.data_bytes.hex()
        is_button_pressed = data_hex == "0001020304050607"

        someip_frame = {
            "services": [
                {
                    "service_name": "ControlLeds",
                    "service_id": self.service_id,
                    "instance_id": self.method_id,
                    "port": 30509,
                    "communication_protocol": "SOME/IP",
                    "service_version": "1.0",
                    "events": [
                        {
                            "event_name": "ButtonStatus",
                            "event_id": self.can_id,
                            "is_field": False,
                            "is_reliable": False,
                            "update_cycle": 0,
                            "event_type": "event",
                            "data_type": str(is_button_pressed),
                            "event_direction": "sendservice",
                            "communication_type": "asynchronous"
                        }
                    ],
                    "event_groups": [
                        {
                            "group_name": "ButtonEvents",
                            "event_group_id": 8017,
                            "event_ids": [2915, 2917],
                            "event_group_description": "Group for LED status change events"
                        }
                    ]
                }
            ],
            "timestamp": time.time()
        }
        self.data1.append(someip_frame)

        with open("someip_log.json", "a") as f:
            json.dump(self.data1, f, indent=4)

