import huffman
import binascii
from random import randint
from time import time
import itertools
import collections

class Test():

	def __init__(self, desc):
		self.desc = desc

	def create_sample(self, bytes, samplefile):
		alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz"
		digits = "0123456789"
		l = len(alphabet)
		k = len(digits)
		content = [alphabet[randint(0, l-1)] for _ in range(round(bytes*0.99))]
		content += [digits[randint(0, k - 1)] for _ in range(round(bytes * 0.01))]
		content = "".join(content)

		with open(samplefile, 'w') as f:
			f.write(content)

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


def f4():
	t = Test("sample-test")

	#t.create_sample(15000000, "target11")

	origin = 'target4'
	compressed = '{}-c'.format(origin)
	uncompressed = '{}-u'.format(origin)

	encoder = huffman.encoder(origin)
	freq = encoder.get_freq()
	length = encoder.get_length()
	table = encoder.get_table()
	max_bit_len = encoder.get_max_bit_len()

	#for k in table.keys():
	#	print("k: {0}, v: {1}".format(k, table[k]))

	encoder.save(compressed)

	#decoder = huffman.decoder(freq, compressed, length, table, max_bit_len)
	#decoder.save(uncompressed)

def f_encode_only(n):
	origin = 'target{}'.format(n)
	compressed = '{}-c'.format(origin)

	encoder = huffman.encoder(origin)

	encoder.save(compressed)

def f_encode_decode(n):

	origin = 'target{}'.format(n)
	compressed = '{}-c'.format(origin)
	uncompressed = '{}-u'.format(origin)

	encoder = huffman.encoder(origin)
	freq = encoder.get_freq()
	length = encoder.get_length()
	table = encoder.get_table()
	max_bit_len = encoder.get_max_bit_len()

	encoder.save(compressed)

	decoder = huffman.decoder(freq, compressed, length, table, max_bit_len)
	decoder.save(uncompressed)

n = 11

#f_encode_only(n)
f_encode_decode(n)
'''
from bitstring import BitArray

with open("target0", "rb") as f:
	c = f.read().hex()

binstring = ''
t1 = time()

r = BitArray(hex=c)
print(r.bin)

with open("target0", "rb") as f:
	c = f.read()

for e in c:
	binstring += bin(e).replace("0b", "").zfill(8)

print(time()-t1)

print(binstring)

print(len(binstring))

#print(list(collections.Counter(c).items()))
'''