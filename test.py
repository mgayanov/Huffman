import huffman
from random import randint
import hashlib
import os


def create_sample(bytes_count, file):
	content = bytearray()

	for _ in range(bytes_count+1):
		random_byte = randint(0, 255)
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

	original = "original"
	compressed = "compressed"
	uncompressed = "uncompressed"

	bytes_count = randint(10**7, 10**7)

	create_sample(bytes_count, original)

	encoder = huffman.Encoder(original)
	encoder.save(compressed)

	decoder = huffman.Decoder(compressed)
	decoder.save(uncompressed)

	if not assert_equals_hash(original, uncompressed):
		raise Exception

	delete_sample(original)
	delete_sample(compressed)
	delete_sample(uncompressed)

print("correct")