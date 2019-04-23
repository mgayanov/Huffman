import huffman
from random import randint
import hashlib
import os
from time import time


def create_sample(bytes_count, file):
	content = bytearray()

	for _ in range(int(bytes_count*0.8)):
		random_byte = randint(0, 100)
		content.append(random_byte)

	for _ in range(int(bytes_count*0.2)):
		random_byte = randint(200, 255)
		content.append(random_byte)

	with open(file, 'wb') as f:
		f.write(content)


def assert_equals_hash(file1, file2):
	file1_md5 = hashlib.md5()
	file2_md5 = hashlib.md5()

	with open(file1, "rb") as f1, open(file2, "rb") as f2:
		file1_md5.update(f1.read())
		file2_md5.update(f2.read())

	return file1_md5.hexdigest() == file2_md5.hexdigest()


def delete_sample(file):
	os.remove(file)


for _ in range(1):

	t1 = time()

	original = "enwik8.txt"
	compressed = "compressed"
	uncompressed = "uncompressed"

	#bytes_count = randint(20**6, 20**6)

	#create_sample(bytes_count, original)
	#print("create_sample", time()-t1)

	encoder = huffman.Encoder(original)
	encoder.save(compressed)

	decoder = huffman.Decoder(compressed)
	#decoder.save(uncompressed)

	#if not assert_equals_hash(original, uncompressed):
	#	raise Exception

	#delete_sample(original)
	#delete_sample(compressed)
	#delete_sample(uncompressed)

print("correct")