# trivial_compression.py
# From Classic Computer Science Problems in Python Chapter 1
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


nucleotide_to_bits = {"A": 0b00, "C": 0b01, "G": 0b10, "T": 0b11}
bits_to_nucleotide = {v: k for k, v in nucleotide_to_bits.items()}


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1  # start with sentinel
        for nucleotide in gene.upper():
            self.bit_string <<= 2  # shift left two bits
            if nucleotide not in nucleotide_to_bits:
                raise ValueError("Invalid Nucleotide:{}".format(nucleotide))
            # change last two bits to xx
            self.bit_string |= nucleotide_to_bits[nucleotide]

    def decompress(self) -> str:
        gene: str = ""
        for i in range(
            0, self.bit_string.bit_length() - 1, 2
        ):  # - 1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11  # get just 2 relevant bits
            if bits not in bits_to_nucleotide:
                raise ValueError("Invalid bits:{}".format(bits))
            gene += bits_to_nucleotide[bits]
        return gene[::-1]  # [::-1] reverses string by slicing backwards

    def __str__(self) -> str:  # string representation for pretty printing
        return self.decompress()


if __name__ == "__main__":
    from sys import getsizeof

    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("original is {} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)  # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bit_string)))
    print(compressed)  # decompress
    print(
        "original and decompressed are the same: {}".format(
            original == compressed.decompress()
        )
    )
