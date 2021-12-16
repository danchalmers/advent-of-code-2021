import unittest

from day_sixteen import hex_to_bits, bits_to_int, Packet


class DaySixteenTestCase(unittest.TestCase):
    def test_hexbin(self):
        self.assertEqual([0,0,0,0], hex_to_bits('0'))
        self.assertEqual([1,0,1,0], hex_to_bits('A'))
        self.assertEqual([1,1,1,0,0,0,0,1], hex_to_bits('E1'))

    def test_binint(self):
        self.assertEqual(0, bits_to_int([0,0,0,0]))
        self.assertEqual(10, bits_to_int([1,0,1,0]))
        self.assertEqual(2, bits_to_int([0,1,0]))
        self.assertEqual(225, bits_to_int([1,1,1,0,0,0,0,1]))

    def test_number_packet_example(self):
        packet, remainder = Packet.make_packet_from_hex('D2FE28')
        self.assertEqual(6, packet.version)
        self.assertEqual(4, packet.type_id)
        self.assertEqual(2021, packet.value())#

    def test_operator_length_type_0(self):
        packet, _ = Packet.make_packet_from_hex('38006F45291200')
        self.assertEqual(1, packet.version)
        self.assertEqual(6, packet.type_id)
        self.assertEqual(2, len(packet.sub_packets()))

    def test_operator_length_type_1(self):
        packet, _ = Packet.make_packet_from_hex('EE00D40C823060')
        self.assertEqual(7, packet.version)
        self.assertEqual(3, packet.type_id)
        self.assertEqual(3, len(packet.sub_packets()))

    def test_version_sum_eg0(self):
        packet, _ = Packet.make_packet_from_hex('D2FE28')
        version_sum = packet.version_sum()
        self.assertEqual(6, version_sum)

    def test_version_sum_eg1(self):
        packet, _ = Packet.make_packet_from_hex('8A004A801A8002F478')
        version_sum = packet.version_sum()
        self.assertEqual(16, version_sum)

    def test_version_sum_eg2(self):
        packet, _ = Packet.make_packet_from_hex('620080001611562C8802118E34')
        version_sum = packet.version_sum()
        self.assertEqual(12, version_sum)

    def test_version_sum_eg3(self):
        packet, _ = Packet.make_packet_from_hex('C0015000016115A2E0802F182340')
        version_sum = packet.version_sum()
        self.assertEqual(23, version_sum)

    def test_version_sum_eg4(self):
        packet, _ = Packet.make_packet_from_hex('A0016C880162017C3686B18A3D4780')
        version_sum = packet.version_sum()
        self.assertEqual(31, version_sum)


if __name__ == '__main__':
    unittest.main()
