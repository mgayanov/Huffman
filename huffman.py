import collections
from time import time
import binascii
import os
from bitstring import BitArray

#https://www.researchgate.net/publication/220114874_A_Memory-Efficient_and_Fast_Huffman_Decoding_Algorithm

BYTE_1 = 1
BYTE_4 = 4


class encoder():

	def __init__(self, in_file):

		t1 = time()

		with open(in_file, 'rb') as f:
			string = f.read()

		self.__string = string

		self.__freq = self.__make_freq_tupple(string)

		nodes = self.__make_nodes()

		self.__HTree = HuffmanTree(nodes)

		self.__encoded = self.__encode()

		self.__encoded_len_original = len(self.__encoded)

		self.__encoded = self.__zpad(self.__encoded)

		print("encoder.__init__ t:", time()-t1)

	@staticmethod
	def __make_freq_tupple(s):
		return list(collections.Counter(s).items())

	def __make_nodes(self):
		return [Node(char=item[0], freq=item[1]) for item in self.__freq]

	@staticmethod
	def __zpad(string):
		result = string
		l = len(string)
		if l % 8 != 0:
			n = (l // 8 + 1) * 8
			result = string.ljust(n, "0")
		return result

	def __encode(self):

		tree = self.__HTree

		result = []
		table = {}

		for c in self.__string:

			if c not in table.keys():
				code = tree.get_target_bits(c)
				table[c] = {"code": code}

			result.append(table[c]["code"])

		return "".join(result)

	def __freqs_to_bytes(self):

		freqs_b = b""

		for e in self.__freq:
			freqs_b += e[0].to_bytes(length=BYTE_1, byteorder="big")
			freqs_b += e[1].to_bytes(length=BYTE_4, byteorder="big")

		freqs_bytes_count_b = len(freqs_b).to_bytes(length=BYTE_4, byteorder="big")

		return freqs_b, freqs_bytes_count_b

	def __original_len_to_byte(self):
		return self.__encoded_len_original.to_bytes(length=BYTE_4, byteorder="big")

	def __encoded_to_bytes(self):
		return BitArray(bin=self.__encoded).bytes

	def save(self, file):

		freqs_b, freqs_bytes_count_b = self.__freqs_to_bytes()

		original_len_b = self.__original_len_to_byte()

		encoded_b = self.__encoded_to_bytes()

		content = freqs_bytes_count_b + freqs_b + original_len_b + encoded_b

		with open(file, 'wb') as f:
			f.write(content)

class decoder():

	def __init__(self, in_file):
		t1 = time()

		self.__freq, self.__encoded_len_original, self.__encoded = self.__extract(in_file)

		nodes = self.__make_nodes()

		self.__HTree = HuffmanTree(nodes)

		self.__table = self.__make_table()

		self.__max_bit_len = self.__get_max_bit_len()

		self.__mtable = self.__make_masked_table()

		bits = BitArray(hex=self.__encoded).bin[:self.__encoded_len_original]

		self.__decoded = self.__decode4(bits)

		print("decoder.__init__ t:", time()-t1)

	def __extract(self, file):

		with open(file, "rb") as f:
			content = f.read()

		freqs_bytes_count = int.from_bytes(content[0:0+BYTE_4], byteorder="big")

		freqs_bytes = content[0+BYTE_4:0+BYTE_4+freqs_bytes_count]

		freqs = []

		for pos in range(0, freqs_bytes_count, 5):
			char = int.from_bytes(freqs_bytes[pos:pos+BYTE_1], byteorder="big")
			freq = int.from_bytes(freqs_bytes[pos+BYTE_1:pos+BYTE_1+BYTE_4], byteorder="big")
			freqs.append((char, freq))

		encoded_len_original = int.from_bytes(content[BYTE_4+freqs_bytes_count:BYTE_4+freqs_bytes_count+BYTE_4], byteorder="big")

		encoded = content[BYTE_4+freqs_bytes_count+BYTE_4:].hex()

		return freqs, encoded_len_original, encoded

	def __make_nodes(self):
		return [Node(char=item[0], freq=item[1]) for item in self.__freq]

	def __make_table(self):
		table = {}
		tree = self.__HTree

		chars = [e[0] for e in self.__freq]

		for char in chars:
			code = tree.get_target_bits(char)
			table[char] = {"code": code}

		return table

	def __get_max_bit_len(self):
		v = [e["code"] for e in list(self.__table.values())]
		max_bit_len = len(max(v, key=len))
		return max_bit_len

	def __decode(self, bits):

		result = bytearray()
		start = 0
		N = len(bits)

		while start < N:

			char, init_index, counter = self.__HTree.path2(bits, start)

			start = init_index + counter

			result.append(char)

		return result

	def __decode4(self, bits):

		mtable = self.__mtable
		bits_len = len(bits)
		max_bit_len = self.__max_bit_len

		start = 0

		bandwidth = bits_len - max_bit_len + 1

		result = bytearray()

		while start < bandwidth:
			bit = bits[start:start+max_bit_len]
			t = mtable[int(bit,2)]
			char = t[0]
			rest = t[1]

			result.append(char)
			start += max_bit_len - rest

		additional = self.__decode(bits[start:])

		for e in additional:
			result.append(e)

		return result

	def __make_masked_table(self):

		table = self.__table

		max_bit_len = self.__max_bit_len

		codes = {}
		for sym in list(table.keys()):

			sym_len = len(table[sym]["code"])

			rest = max_bit_len - sym_len

			mask = (1 << sym_len) << rest

			code = table[sym]["code"]

			codes[code] = [mask, bin(mask), sym, rest]

		mtable = {}
		codes_keys = list(codes.keys())

		for code in codes_keys:
			mask = codes[code][0]
			sym = codes[code][2]
			rest = codes[code][3]

			n1 = int(code,2) << rest#int(code + ("0"*rest), 2)
			n2 = (int(code,2) << rest) | ((1<<rest)-1)#int(code + ("1"*rest), 2)

			for d in range(n1, n2+1):
				mtable[d] = [sym, rest, bin(mask), code]

		return mtable

	def save(self, out_file):
		content = self.__decoded
		with open(out_file, 'wb') as f:
			f.write(content)


class Node():

	def __init__(self, char, freq, left=None, right=None):
		self.char  = char
		self.freq  = freq
		self.left  = left
		self.right = right

class HuffmanTree():

	def __init__(self, nodes_list):

		if len(nodes_list) == 2:
			left_node  = nodes_list[0]
			right_node = nodes_list[1]

			self.root = Node(char=None, freq=None, left=left_node, right=right_node)
			return

		nodes_list = sorted(nodes_list, key=lambda node: node.freq, reverse=True)

		min_freq_node1, min_freq_node2 = nodes_list.pop(), nodes_list.pop()

		new_node = Node(char=None, freq=min_freq_node1.freq + min_freq_node2.freq, left=min_freq_node2,
						right=min_freq_node1)

		nodes_list.append(new_node)

		self.__init__(nodes_list)

	#bits is str
	def get_target_bits(self, target, node=None, bits=""):

		node = node or self.root

		# leaf found
		if not node.left and not node.right:
			return bits if node.char == target else None

		if node.left:
			a = self.get_target_bits(target, node.left, bits + "0")

			if a: return a

		if node.right:
			a = self.get_target_bits(target, node.right, bits + "1")

			if a: return a

		return None

	#bits is int list
	def path(self, bits, node=None, start=0, counter=0):

		node = node or self.root

		# leaf found
		if not node.left and not node.right:
			return node.char, start, counter

		#next_step = bits.pop(0)
		next_step = bits[start + counter]
		counter += 1

		if next_step == '0':
			return self.path(bits, node.left, start, counter)

		if next_step == '1':
			return self.path(bits, node.right, start, counter)

	def path2(self, bits, start):

		curr_node = self.root
		counter = 0

		while curr_node.left or curr_node.right:
			next_step = bits[start + counter]

			if next_step == '0':
				curr_node = curr_node.left

			if next_step == '1':
				curr_node = curr_node.right

			counter += 1

		return curr_node.char, start, counter

	def path3(self, bit):

		curr_node = self.root
		counter = 0
		result = None

		while counter < len(bit):
			next_step = bit[counter]

			if next_step == '0':
				curr_node = curr_node.left

			if next_step == '1':
				curr_node = curr_node.right

			counter += 1

		if not curr_node.left and not curr_node.right:
			result = curr_node.char

		return result

	def get_leafs(self, node=None):

		curr_node = node or self.root

		leafs = []

		if not curr_node.left and not curr_node.right:
			return [curr_node.char]

		if curr_node.left:
			left_childs = self.get_leafs(curr_node.left)
			for child in left_childs:
				leafs.append(child)

		if curr_node.right:
			right_childs = self.get_leafs(curr_node.right)
			for child in right_childs:
				leafs.append(child)

		return leafs