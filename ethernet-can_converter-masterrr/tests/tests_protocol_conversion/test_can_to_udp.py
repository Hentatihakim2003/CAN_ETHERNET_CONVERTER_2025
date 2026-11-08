import unittest
import sys
import os
import struct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))


from protocol_conversion.can_to_udp import CantoUdp

class TestCantoUdp(unittest.TestCase):
    def setUp(self):
        self.udp_handler = CantoUdp("192.168.1.100", 5000)
        self.fake_packet = bytes([
            0x00,             # préfixe
            0x01, 0x23,       # CAN ID = 0x123
            0x00,             # padding
            0x04,             # DLC = 4
            0x00, 0x00, 0x00, # padding
            0x11, 0x22, 0x33, 0x44  # Data
        ])
    
    def test_extraction_udp(self):
        udp_payload, can_id, dlc, data = self.udp_handler.extraction_udp(self.fake_packet)
        self.assertEqual(can_id, 0x123)
        self.assertEqual(dlc, 4)
        self.assertEqual(data, bytes([0x11, 0x22, 0x33, 0x44]))
        expected_payload = struct.pack("!IB", 0x123, 4) + bytes([0x11, 0x22, 0x33, 0x44]).ljust(8, b'\x00')
        self.assertEqual(udp_payload, expected_payload)

if __name__ == '__main__':
    unittest.main()

