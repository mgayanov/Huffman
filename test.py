import huffman
import binascii

with open("LICENSE", "rb") as f:
    s = f.read().hex()

#s = binascii.hexlify(s.encode()).decode()

print(s)

chunks = [s[i:i+2] for i in range(0, len(s), 2)]

print(chunks)

encoded = huffman.encoder(chunks).get_encoded()

print(encoded)

with open("tmp", "w") as f:
    f.write(binascii.unhexlify(encoded).decode())
