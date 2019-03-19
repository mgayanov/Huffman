class encoder():

    def __init__(self, string):

        self.freq = self.__get_freq_tupple(string)

        nodes = [Node(char=item[0], freq=item[1]) for item in self.freq]

        self.__HTree = HuffmanTree(nodes)
        
        self.__string = string

        self.__encoded = self.__encode()

    def get_encoded(self):
        return self.__encoded

    def get_freq(self):
        return self.freq

    @staticmethod
    def __get_freq_tupple(s):
        return sorted([(c, s.count(c)) for c in set(s)], key=lambda x: x[1], reverse=True)

    def __encode(self):

        tree = self.__HTree

        result = [tree.get_target_bits(c) for c in self.__string]

        return "".join(result)

class decoder():

    def __init__(self, freq, bits):

        nodes = [Node(char=item[0], freq=item[1]) for item in freq]

        self.__HTree = HuffmanTree(nodes)

        self.__decoded = self.__decode(bits)

    def __decode(self, bits):

        bits = [int(bit) for bit in bits]

        result = ""

        while bits:
            result += self.__HTree.path(bits)

        return result

    def get_decoded(self):
        return self.__decoded


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

'''
string = "qwerty"
H = encoder(string)

freq = H.get_freq()
encoded = H.get_encoded()
print(encoded)

decoded = decoder(freq, encoded).get_decoded()
print(decoded)


bits = H(string)

print(bits)

decoded = H.decode(bits)

print(decoded)
'''