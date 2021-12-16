from __future__ import annotations

from abc import ABC, abstractmethod
from functools import reduce
from operator import mul
from typing import Optional

from pipe import reverse


Bits = list[int]

REAL_FILE = 'input-16.txt'


def hex_to_bits(hex: str) -> Bits:
    n = int(hex, 16)
    return [(n >> position) & 1 for position in range((4 * len(hex)) - 1, -1, -1)]


def bits_to_int(bits: Bits) -> int:
    return sum([bit * 2**position for position, bit in enumerate(bits | reverse)])


class Packet(ABC):
    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = type_id

    @abstractmethod
    def value(self) -> int:
        pass

    @abstractmethod
    def sub_packets(self) -> list[Packet]:
        pass

    @abstractmethod
    def version_sum(self) -> int:
        pass

    @staticmethod
    def bits_to_literal(bits: Bits) -> tuple[int, Bits]:
        digits = []
        index = 0
        while (bits[index]) == 1:
            digits.extend(bits[index + 1:index + 5])
            index += 5
        digits.extend(bits[index + 1:index + 5])
        index += 5
        return bits_to_int(digits), bits[index:]

    @staticmethod
    def make_packet_from_bin(bits: Bits) -> tuple[Optional[Packet], Bits]:
        version = bits_to_int(bits[0:3])
        type_value = bits_to_int(bits[3:6])
        remaining = bits[6:]
        if type_value == 4:
            literal, remaining = Packet.bits_to_literal(remaining)
            p = LiteralPacket(version, type_value, literal)
        else:
            p = OperatorPacket(version, type_value)
            _, remaining = p.parse_sub_packets(remaining)
        return p, remaining

    @staticmethod
    def make_packet_from_hex(hex: str) -> tuple[Packet, Bits]:
        bits = hex_to_bits(hex)
        return Packet.make_packet_from_bin(bits)


class LiteralPacket(Packet):
    def __init__(self, version: int, type_id: int, literal: int):
        super().__init__(version, type_id)
        self.literal = literal

    def value(self) -> int:
        return self.literal

    def sub_packets(self) -> list[Packet]:
        return []

    def version_sum(self) -> int:
        return self.version

    def __repr__(self):
        return f"Literal(v{self.version} = {self.value()})"


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int):
        super().__init__(version, type_id)
        self.packets = []

    def parse_sub_packets(self, remaining_bits: Bits) -> tuple[Packet, Bits]:
        length_id = remaining_bits[0]
        remaining_bits = remaining_bits[1:]
        if length_id == 0:
            length = bits_to_int(remaining_bits[:15])
            remaining_bits = remaining_bits[15:]
            sub_packet_bits = remaining_bits[:length]
            remaining_bits = remaining_bits[length:]
            while sub_packet_bits:
                p, sub_packet_bits = Packet.make_packet_from_bin(sub_packet_bits)
                self.packets.append(p)
        else:
            length = bits_to_int(remaining_bits[:11])
            remaining_bits = remaining_bits[11:]
            while len(self.packets) < length:
                p, remaining_bits = Packet.make_packet_from_bin(remaining_bits)
                self.packets.append(p)
        return self, remaining_bits

    def value(self) -> int:
        values = [p.value() for p in self.packets]
        match self.type_id:
            case 0:
                return sum(values)
            case 1:
                return reduce(mul, values)
            case 2:
                return min(values)
            case 3:
                return max(values)
            case 5:
                return 1 if values[0] > values[1] else 0
            case 6:
                return 1 if values[0] < values[1] else 0
            case 7:
                return 1 if values[0] == values[1] else 0
            case _:
                print("undefined type!")
                return 0

    def sub_packets(self) -> list[Packet]:
        return self.packets

    def version_sum(self) -> int:
        return self.version + sum([p.version_sum() for p in self.sub_packets()])

    def __repr__(self):
        return f"Operator(v{self.version} = {self.sub_packets()})"


def load_from_file(file_name: str) -> tuple[Packet, list[int]]:
    with open('data/' + file_name, 'r') as f:
        return Packet.make_packet_from_hex(f.readline().strip())


def part_one(packet: Packet):
    print(f"part one version sum: {packet.version_sum()}")


def part_two(packet: Packet):
    print(f"part two value: {packet.value()}")


if __name__ == "__main__":
    packet, _ = load_from_file(REAL_FILE)
    part_one(packet)
    part_two(packet)
