import unittest
from unittest.mock import patch, MagicMock
import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from sending_bus_output.ethernet_send import EthernetSend
class TestEthernetSend(unittest.TestCase):
    @patch('socket.socket')  # on remplace socket.socket par un mock
    def test_send(self, mock_socket_class):
        # Création d'un faux logger
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

        # On prépare le mock de socket
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        # Instanciation de la classe avec interface fictive
        eth_sender = EthernetSend("eth0", logger)

        # Préparation des données de test
        eth_frame = b'\xaa\xbb\xcc\xdd\xee\xff' * 2 + b'\x88\xb5' + b'\x01#\x08' + b'\x11\x22\x33\x44\x55\x66\x77\x88'
        can_id = 0x123
        dlc = 8
        data = b'\x11\x22\x33\x44\x55\x66\x77\x88'

        # Appel de la méthode à tester
        eth_sender.send(eth_frame, can_id, dlc, data)

        # Vérifie que send a bien été appelé avec eth_frame
        mock_socket.send.assert_called_once_with(eth_frame)

    @patch('socket.socket')
    def test_close(self, mock_socket_class):
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        eth_sender = EthernetSend("eth0", MagicMock())
        eth_sender.close()
        mock_socket.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()


