import unittest
import struct
import can
import sys
import os
import struct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from protocol_conversion.ethernet_to_can import EthernetToCan
from scapy.all import Ether, IP, UDP, Raw

class TestEthernetToCan(unittest.TestCase):
    def setUp(self):
        self.mac_pc = "00:11:22:33:44:55"
        self.mac_rsp = "66:77:88:99:AA:BB"
        self.ip_pc = "192.168.1.10"
        self.ip_rsp = "192.168.1.20"
        self.interface = "eth0"

        self.eth_to_can = EthernetToCan(
            interface=self.interface,
            handler=None,
            mac_pc=self.mac_pc,
            mac_rsp=self.mac_rsp,
            ip_pc=self.ip_pc,
            ip_rsp=self.ip_rsp,
            logger=None
        )

        self.can_id = 0x100
        self.dlc = 8
        self.data = bytes([0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7])
        payload = struct.pack("!IB", self.can_id, self.dlc) + self.data
        print (payload)
        payload = payload + b'\x00' * (12 - len(payload))
        self.packet = Ether(src=self.mac_pc, dst=self.mac_rsp) / IP(src=self.ip_pc, dst=self.ip_rsp) / UDP(dport=5005) / Raw(load=payload)

    def test_extraction_ethernet_to_can(self):
        messages = self.eth_to_can.extraction_ethernet_to_can(self.packet)

        self.assertEqual(len(messages), 1)
        msg = messages[0]
        self.assertIsInstance(msg, can.Message)
        self.assertEqual(msg.arbitration_id, self.can_id)
        self.assertEqual(msg.dlc, self.dlc)
        self.assertEqual(msg.data, self.data)
        self.assertFalse(msg.is_extended_id)

if __name__ == '__main__':
    unittest.main()
