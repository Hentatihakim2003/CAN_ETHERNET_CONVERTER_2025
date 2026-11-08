import unittest
from unittest.mock import MagicMock, patch
import can
import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from sending_bus_output.can_send import CanSend

class TestCanSend(unittest.TestCase):
    @patch('can.interface.Bus')  # On "patch" le bus CAN
    def test_process_ethernet_frame(self, mock_bus_class):
        # Création d’un logger factice
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())  # pour afficher dans la console

        # On crée un mock de bus
        mock_bus = MagicMock()
        mock_bus_class.return_value = mock_bus

        # Instanciation de CanSend avec le mock
        can_sender = CanSend("can0", logger)

        # Création de messages CAN simulés
        msg1 = can.Message(arbitration_id=0x123, data=[0x11, 0x22], is_extended_id=False)
        msg2 = can.Message(arbitration_id=0x456, data=[0xAA, 0xBB, 0xCC], is_extended_id=False)

        messages = [msg1, msg2]

        # Appel de la méthode à tester
        can_sender.process_ethernet_frame(messages)

        # Vérifie que `send` a été appelé deux fois avec les bons messages
        self.assertEqual(mock_bus.send.call_count, 2)
        mock_bus.send.assert_any_call(msg1)
        mock_bus.send.assert_any_call(msg2)

if __name__ == '__main__':
    unittest.main()

