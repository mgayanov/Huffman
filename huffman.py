import collections
from time import time
import binascii
import os
from bitstring import BitArray

#https://www.researchgate.net/publication/220114874_A_Memory-Efficient_and_Fast_Huffman_Decoding_Algorithm

class utils():
	@staticmethod
	def bin_to_hex(string):
		r = ["{}".format(hex(int(string[i:i+8],2))).replace("0x", "").zfill(2) for i in range(0, len(string), 8)]
		r = "".join(r)
		return r

	@staticmethod
	def hex_to_bin(string):
		r = ["{}".format(bin(int(string[i:i + 2], 16))).replace("0b", "").zfill(8) for i in range(0, len(string), 2)]
		r = "".join(r)
		return r

	@staticmethod
	def str_to_bytes(string):

		s = bytes.fromhex(string)



		return [string[i:i + 2] for i in range(0, len(string), 2)]

class encoder():

	def __init__(self, in_file):
		t1 = time()
		with open(in_file, 'rb') as f:
			#string = f.read().hex()
			string = f.read()

		print("encoder.__init__ read data t:", time() - t1)

		#string = utils.str_to_bytes(string)
		print("encoder.__init__ prepare data t:", time() - t1)

		self.__string = string

		self.__freq = self.__get_freq_tupple(string)
		#print("encoder freq part t:", time()-t1)

		#for e in self.__freq:
		#	print(e)

		#t2 = time()

		nodes = [Node(char=item[0], freq=item[1]) for item in self.__freq]

		self.__HTree = HuffmanTree(nodes)
		#print("encoder HTree part t:", time()-t2)

		#print(self.__HTree.get_leafs())

		#t3 = time()

		self.__encoded = self.__encode()
		#print("encoder encode part t:", time()-t3)

		#self.__fill_w_c()

		self.__encoded_length = len(self.__encoded)

		self.__encoded = self.__zpad(self.__encoded)

		print("encoder.__init__ t:", time()-t1)



	def get_encoded(self):
		return self.__encoded

	def get_freq(self):
		return self.__freq

	def get_table(self):
		return self.__table

	def get_length(self):
		return self.__encoded_length

	@staticmethod
	def __get_freq_tupple(s):
		return list(collections.Counter(s).items())
		#return [(c, s.count(c)) for c in set(s)]

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
		tmp = []
		table = {}

		for c in self.__string:

			if c not in table.keys():
				code = tree.get_target_bits(c)
				table[c] = {"code": code}

			result.append(table[c]["code"])

		self.__table = table

		return "".join(result)

	def get_max_bit_len(self):

		v = [e["code"] for e in list(self.__table.values())]

		# self.min_bit_code = len(min(v, key=len))
		self.max_bit_code = len(max(v, key=len))

		return self.max_bit_code

	def __fill_w_c(self):

		v = [e["code"] for e in list(self.__table.values())]

		max_bit_code = len(max(v, key=len))

		height = max_bit_code

		for c in self.__table.keys():
			l = len(self.__table[c]["code"])
			self.__table[c]["w"] = 2 ** (height - l)

		chars = self.__HTree.get_leafs()

		count_0 = self.__table[chars[0]]["w"]
		self.__table[chars[0]]["count"] = count_0

		for i in range(1, len(chars)):
			count = self.__table[chars[i-1]]["count"] + self.__table[chars[i]]["w"]
			self.__table[chars[i]]["count"] = count


	def save(self, out_file):
		content = utils.bin_to_hex(self.__encoded)
		with open(out_file, 'wb') as f:
			f.write(binascii.unhexlify(content))



class decoder():

	def __init__(self, freq, in_file, origin_length, table, max_bit_len):
		t1 = time()
		with open(in_file, 'rb') as f:
			string = f.read().hex()

		print("decoder.__init__ read data t:", time() - t1)

		#v = [e["code"] for e in list(table.values())]

		#self.min_bit_code = len(min(v, key=len))
		#self.max_bit_code = len(max(v, key=len))
		#self.max_bit = max(v, key=len)

		self.max_bit_code = max_bit_len

		self.table = table

		#print("min_bit_code: {0}, max_bit_code: {1}".format(self.min_bit_code, self.max_bit_code))
		#print("origin_length", origin_length)

		#bits = utils.hex_to_bin(string)[:origin_length]
		bits = BitArray(hex=string).bin[:origin_length]
		print("decoder.__init__ prepare data t:", time() - t1)
		#print('bits L', len(bits))

		self.__origin_length = origin_length
		#t2 = time()
		nodes = [Node(char=item[0], freq=item[1]) for item in freq]
		#print("decoder.__init__ nodes t: {0}", time()-t2)

		#t3 = time()
		self.__HTree = HuffmanTree(nodes)
		#print("decoder.__init__ HTree t: {0}", time() - t3)
		#t4 = time()

		self.__decoded = self.__decode4(bits)

		#print("decoder.__init__ decode t: ", time() - t4)

		#self.__decoded = self.__decoded[:origin_length]

		print("decoder.__init__ t:", time()-t1)

	def __decode(self, bits):

		result = bytearray()
		start = 0
		N = len(bits)

		while start < N-1:
			#t1 = time()

			char, init_index, counter = self.__HTree.path2(bits, start)

			start = init_index + counter

			result.append(char)

			#print("decoder.__decode char: {0}, bit: {1}, t: {2}".format(char, bits[a:a+b], time()-t1))

		return result

	def __decode2(self, bits):

		start = 0
		result = ""

		while start < len(bits):

			for bit_length in range(self.min_bit_code, self.max_bit_code+1, 1):

				curr_bit = bits[start:start+bit_length]

				char = self.__HTree.path3(curr_bit)

				if char:
					result += char
					start += bit_length
					break

		return result

	def __decode3(self, bits):

		start = 0
		result = ""
		N = self.min_bit_code
		M = self.max_bit_code

		c_w = [[k, self.table[k]["code"], self.table[k]["count"], self.table[k]["w"]] for k in self.table.keys()]

		lengths = []

		for e in c_w:
			l = len(e[1])
			if l not in lengths:
				lengths.append(l)

		counts_w = {}

		for e in c_w:
			counts_w[e[2]] = [e[3], e[0]]

		print(counts_w)
		counts = list(counts_w.keys())

		cached = {}

		while start < len(bits):

			old_start = start

			for bit_length in lengths:

				curr_bit = bits[start:start+bit_length]

				if curr_bit in cached.keys():
					result += cached[curr_bit]
					start += bit_length
					break

				t = (int(curr_bit, 2) + 1) * 2**(M-bit_length)
				w = 2**(M-bit_length)

				if t in counts and counts_w[t][0] == w:
					result += counts_w[t][1]
					start += bit_length

					cached[curr_bit] = counts_w[t][1]

					break

		return result

	def __decode4(self, bits):

		#t1 = time()
		self.__make_masked_table()
		#print("__decode4 make mtable t: {0}".format(time()-t1))
		table = self.mtable
		#print("__decode4 mtable len: {0}".format(len(table)))

		result = ""
		bits_len = len(bits)
		max_bit_len = self.max_bit_code

		#for k in table.keys():
		#	print(k, table[k])

		start = 0

		bandwidth = bits_len - max_bit_len + 1

		#print("bandwidth: {0}".format(bandwidth))
		#t1 = time()

		#print(bits)

		result = bytearray()

		while start < bandwidth:

			#t1 = time()
			bit = bits[start:start+max_bit_len]
			t = table[int(bit,2)]
			char = t[0]
			rest = t[1]

			#result += char
			result.append(char)
			start += max_bit_len - rest
			#print("__decode4 t per op: {0}".format(time()-t1))

			#print("bit: {0}, char: {1}, rest: {2}, new_start: {3}, if: {4}".format(bit, char, rest, start, start < bandwidth))

		#print("__decode4 main loop t:", time()-t1)

		#t1 = time()
		additional = self.__decode(bits[start:])

		for e in additional:
			result.append(e)

		#print("__decode4 second loop t:", time() - t1)
		print("res len ", len(result))

		return result

	def __make_masked_table(self):

		table = self.table

		self.max_bit_code += 0

		max_bit_len = self.max_bit_code
		#max_bit = self.max_bit

		#print("max_bit_len", max_bit_len)

		codes = {}
		#t1 = time()
		for sym in list(table.keys()):

			code = int(table[sym]["code"], 2)
			mask = int('1'*len(table[sym]["code"]), 2) << (max_bit_len - len(table[sym]["code"]))
			rest = max_bit_len - len(table[sym]["code"])
			#print("code: {0}, delta: {1}, mask: {2}, l: {3}".format(table[sym]["code"], max_bit_len - len(table[sym]["code"]), mask, len(table[sym]["code"])))
			codes[table[sym]["code"]] = [mask, bin(mask), sym, rest]
			#print(table[sym]["code"], codes[table[sym]["code"]])
		#print("codes table t: {0}".format(time()-t1))
		M = int('1'*max_bit_len, 2)

		mtable = {}
		#mtable = [0]*(M+1)

		#t1 = time()
		codes_keys = list(codes.keys())
		#print("M: {0}, codes_len: {1}".format(M, len(codes)))

		for code in codes_keys:
			mask = codes[code][0]
			sym = codes[code][2]
			rest = codes[code][3]

			n1 = int(code + '0'*rest, 2)
			n2 = int(code + '1' * rest, 2)

			for d in range(n1, n2+1):
				mtable[d] = [sym, rest, bin(mask), code]

		'''
		for d in range(M+1):

			for code in codes_keys:
				mask = codes[code][0]
				sym = codes[code][2]
				rest = codes[code][3]



				if (d & mask) >> rest == int(code, 2):
					print("d: {0}, mask: {1}, code: {2}, sym: {3}".format(bin(d), mask, d & mask, sym))
					#mtable[bin(d).replace("0b", "").rjust(max_bit_len, "0")] = [sym, rest]
					mtable[d] = [sym, rest, bin(mask), code]
					break
					#print(bin(d), sym)
		'''
		#print("mtable t: {0}".format(time() - t1))
		#for k in mtable.keys():
		#	print(k, mtable[k])

		#print(mtable)

		self.mtable = mtable


	def get_decoded(self):
		return self.__decoded

	def save(self, out_file):
		content = self.__decoded
		#print(content)
		with open(out_file, 'wb') as f:
			f.write(content)
			#f.write(binascii.unhexlify(content))


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