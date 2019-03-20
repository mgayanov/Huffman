import huffman
import binascii
import time

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
        r = ["{}".format(hex(int(string[i:i+8],2))).replace("0x", "").zfill(2) for i in range(0, len(string), 8)]
        r = "".join(r)
        return r

    def hex_to_bin(self, string):
        r = ["{}".format(bin(int(string[i:i + 2], 16))).replace("0b", "").zfill(8) for i in range(0, len(string), 2)]
        r = "".join(r)
        return r

origin = 'target.txt'
compressed = '{}-c'.format(origin)
uncompressed = '{}-u'.format(origin)

encoder = huffman.encoder(origin)
freq = encoder.get_freq()
length = encoder.get_length()

encoder.save(compressed)

decoder = huffman.decoder(freq, compressed, length)
decoder.save(uncompressed)

'''
test = Test("simple-test")

hexunencoded = test.readfile("target")

#print(hexunencoded)

chunks = test.str_to_bytes(hexunencoded)

#print("chunks", chunks)

t1 = time.time()

encoder = huffman.encoder(chunks)

print("encoder time", time.time()-t1)

encoded = encoder.get_encoded()
freq = encoder.get_freq()

for e in freq:
    print(e)

l1 = len(encoded)
print("l1", l1)

if l1 % 8 != 0:
    n = (l1 // 8 + 1) * 8
    print("n", n)
    encoded = encoded.ljust(n, "0")
    l2 = len(encoded)
print("l2", l2)

hexencoded1 = test.bin_to_hex(encoded)

#print("encoded2", test.hex_to_bin(hexencoded1))
#print("encoded == test.hex_to_bin(hexencoded1)", encoded == test.hex_to_bin(hexencoded1))

test.writefile("tmp", hexencoded1)

#####################



hexencoded2 = test.readfile("tmp")

print("hexencoded1 == hexencoded2", hexencoded1 == hexencoded2)

#print("hexencoded2", hexencoded2)

bits = test.hex_to_bin(hexencoded2)[:l1]

#print("bits    ", bits)

#print(encoded == bits)

t1 = time.time()

decoder = huffman.decoder(freq, bits)

print("decoder time", time.time()-t1)

decoded = decoder.get_decoded()

#print("decoded", decoded)

test.writefile("tmp2", decoded)
'''