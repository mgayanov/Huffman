import huffman
import binascii
from random import randint
from time import time
import itertools
import collections
import hashlib

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




def f_encode_only(n):
	origin = 'target{}'.format(n)
	compressed = '{}-c'.format(origin)

	encoder = huffman.encoder(origin)

	encoder.save(compressed)

def f_decode_only(n):
	origin = 'target{}'.format(n)
	compressed = '{}-c'.format(origin)
	uncompressed = '{}-u'.format(origin)

	decoder = huffman.decoder(compressed)
	decoder.save(uncompressed)

def f_encode_decode(n):

	origin = 'target{}'.format(n)
	compressed = '{}-c'.format(origin)
	uncompressed = '{}-u'.format(origin)

	origin_md5 = hashlib.md5()

	with open(origin, "rb") as f:
		origin_md5.update(f.read())

	encoder = huffman.encoder(origin)

	encoder.save(compressed)

	decoder = huffman.decoder(compressed)
	decoder.save(uncompressed)

	uncompressed_md5 = hashlib.md5()

	with open(uncompressed, "rb") as f:
		uncompressed_md5.update(f.read())

	print(uncompressed_md5.hexdigest() == origin_md5.hexdigest())

n = 11

#f_encode_only(n)
f_decode_only(n)
#f_encode_decode(n)