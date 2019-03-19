import huffman
import binascii

class Test():

    def __init__(self, desc):
        self.desc = desc

    def readfile(self, filename):
        with open(filename, "rb") as f:
            hexstring = f.read().hex()
            return hexstring

    def writefile(self, filename, hexstring):
        with open(filename, "wb") as f:
            f.write(binascii.unhexlify(hexstring))

    def str_to_bytes(self, string):
        return [string[i:i + 2] for i in range(0, len(string), 2)]

    def bin_to_hex(self, string):
        r = ["{}".format(hex(int(string[i:i+8],2))[2:]).zfill(2) for i in range(0, len(string), 8)]
        r = "".join(r)
        return r

    def hex_to_bin(self, string):
        r = ["{}".format(bin(int(string[i:i + 2], 16))).replace("0b", "").zfill(8) for i in range(0, len(string), 2)]
        print(r)
        r = "".join(r)
        return r



test = Test("simple-test")

hexunencoded = test.readfile("LICENSE")

print(hexunencoded)

chunks = test.str_to_bytes(hexunencoded)

print("chunks", chunks)

encoder = huffman.encoder(chunks)

encoded = encoder.get_encoded()
freq = encoder.get_freq()

print("encoded", encoded)

hexencoded1 = test.bin_to_hex(encoded)
print("hexencoded1", hexencoded1)

test.writefile("tmp", hexencoded1)

hexencoded2 = test.readfile("tmp")

print("hexencoded2", hexencoded2)

bits = test.hex_to_bin(hexencoded2)

decoder = huffman.decoder(freq, bits)

decoded = decoder.get_decoded()

print("decoded", decoded)

test.writefile("tmp2", decoded)