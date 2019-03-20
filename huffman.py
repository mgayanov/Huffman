

import binascii

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
        return [string[i:i + 2] for i in range(0, len(string), 2)]

class encoder():

    def __init__(self, in_file):

        with open(in_file, 'rb') as f:
            string = f.read().hex()

        string = utils.str_to_bytes(string)

        self.__string = string

        self.__freq = self.__get_freq_tupple(string)

        nodes = [Node(char=item[0], freq=item[1]) for item in self.__freq]

        self.__HTree = HuffmanTree(nodes)

        self.__encoded = self.__encode()

        self.__encoded_length = len(self.__encoded)

        l1 = len(self.__encoded)
        self.__encoded = self.__zpad(self.__encoded)
        l2 = len(self.__encoded)

        print('L1', l1, 'L2', l2)



    def get_encoded(self):
        return self.__encoded

    def get_freq(self):
        return self.__freq

    def get_length(self):
        return self.__encoded_length

    @staticmethod
    def __get_freq_tupple(s):
        return sorted([(c, s.count(c)) for c in set(s)], key=lambda x: x[1], reverse=True)

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

        for c in self.__string:
            code = tree.get_target_bits(c)
            result.append(code)
            t = [c, chr(int(c, 16)), self.__string.count(c), code]
            if t not in tmp:
                tmp.append(t)
            #print("c: {0}, freq: {1}, code: {2}".format(c, self.__string.count(c), code))

        tmp = sorted(tmp, key=lambda x: x[2])
        for e in tmp:
            print(e)

        #result = [tree.get_target_bits(c) for c in self.__string]

        return "".join(result)

    def save(self, out_file):
        content = utils.bin_to_hex(self.__encoded)
        with open(out_file, 'wb') as f:
            f.write(binascii.unhexlify(content))



class decoder():

    def __init__(self, freq, in_file, origin_length):

        with open(in_file, 'rb') as f:
            string = f.read().hex()

        print("origin_length", origin_length)

        bits = utils.hex_to_bin(string)[:origin_length]
        print('bits L', len(bits))

        self.__origin_length = origin_length

        nodes = [Node(char=item[0], freq=item[1]) for item in freq]

        self.__HTree = HuffmanTree(nodes)

        self.__decoded = self.__decode(bits)

        self.__decoded = self.__decoded[:origin_length]

    def __decode(self, bits):

        bits = [int(bit) for bit in bits]

        result = ""

        while bits:
            result += self.__HTree.path(bits)

        return result

    def get_decoded(self):
        return self.__decoded

    def save(self, out_file):
        content = self.__decoded
        with open(out_file, 'wb') as f:
            f.write(binascii.unhexlify(content))


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
    def path(self, bits, node=None):

        node = node or self.root

        # leaf found
        if not node.left and not node.right:
            return node.char

        next_step = bits.pop(0)

        if next_step == 0 and node.left:
            return self.path(bits, node.left)

        if next_step == 1 and node.right:
            return self.path(bits, node.right)