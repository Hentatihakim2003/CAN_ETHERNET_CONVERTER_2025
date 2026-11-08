import unittest
from unittest.mock import patch, MagicMock
import socket
import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from sending_bus_output.udp_send import UdpSend
class TestUdpSend(unittest.TestCase):
    @patch('socket.socket')
    @patch('logging.getLogger')  
    def test_send(self, mock_logger, mock_socket):
        logger = MagicMock()
        
        mock_udp_socket = MagicMock()
        mock_socket.return_value = mock_udp_socket
        
        udp_sender = UdpSend("192.168.1.1", 12345, logger)
        udp_payload = b'\x01#\x04\x11"3D\x00\x00\x00\x00'
        can_id = 0x123
        dlc = 8
        data = b'\x11\x22\x33\x44\x55\x66\x77\x88'
        udp_sender.send(udp_payload, can_id, dlc, data)
        mock_udp_socket.sendto.assert_called_once_with(udp_payload, ("192.168.1.1", 12345))
        logger.info.assert_called_once_with(f"Envoyé en UDP: ID={hex(can_id)}, DLC={dlc}, Data={data.hex()}")

    @patch('socket.socket')
    def test_close(self, mock_socket):
        udp_sender = UdpSend("192.168.1.1", 12345, MagicMock())
        udp_sender.close()
        mock_socket.return_value.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
