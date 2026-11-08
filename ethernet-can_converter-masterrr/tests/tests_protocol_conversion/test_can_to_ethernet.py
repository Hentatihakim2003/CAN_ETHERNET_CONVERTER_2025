import unittest
import sys
import os
import struct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from protocol_conversion.can_to_ethernet import CantoEthernet  

class TestCantoEthernet(unittest.TestCase):
    def setUp(self):
        self.pc_mac = bytes.fromhex('001122334455')
        self.raspberry_mac = bytes.fromhex('66778899AABB')
        self.eth_type_can = bytes.fromhex('88B5')
        self.eth_interface = 'lo'  

        self.eth_handler = CantoEthernet(self.eth_interface, self.pc_mac, self.raspberry_mac, self.eth_type_can)

        self.fake_packet = bytes([
            0x00,             
            0x01, 0x23,       
            0x00,             
            0x04,             
            0x00, 0x00, 0x00, 
            0x11, 0x22, 0x33, 0x44  
        ])

    def test_extraction_can(self):
        eth_frame, can_id, dlc, data = self.eth_handler.extraction_can(self.fake_packet)

        self.assertEqual(can_id, 0x0123)
        self.assertEqual(dlc, 4)
        self.assertEqual(data, bytes([0x11, 0x22, 0x33, 0x44]))

        expected_payload = (
            self.pc_mac +
            self.raspberry_mac +
            self.eth_type_can +
            struct.pack("!IB", 0x0123, 4) +
            data.ljust(8, b'\x00')
        )

        self.assertEqual(eth_frame, expected_payload)

if __name__ == '__main__':
    unittest.main()
