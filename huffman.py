class Huffman():
    pass

class Node():

    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right



class Tree():

    def __init__(self, nodes_list):

        if len(nodes_list) == 2:
            self.root = Node(char=None, freq=None, left=nodes_list[0], right=nodes_list[1])
            return

        nodes_list = sorted(nodes_list, key=lambda node: -node.freq)

        min_freq_node1, min_freq_node2 = nodes_list.pop(), nodes_list.pop()

        new_node = Node(char=None, freq=min_freq_node1.freq + min_freq_node2.freq, left=min_freq_node2,
                        right=min_freq_node1)
        nodes_list.append(new_node)

        self.__init__(nodes_list)

    def find(self, target, start_node=None, result=""):

        start_node = start_node or self.root

        # leaf found
        if not start_node.left and not start_node.right:
            return result if start_node.char == target else None

        if start_node.left:
            a = self.find(target, start_node.left, result + "0")

            if a: return a

        if start_node.right:
            a = self.find(target, start_node.right, result + "1")

            if a: return a

        return None

    def path(self, steps, next_node=None):

        next_node = next_node or self.root

        # leaf found
        if not next_node.left and not next_node.right:
            return next_node.char

        next_step = steps.pop(0)

        if next_step == 0 and next_node.left:
            return self.path(steps, next_node.left)

        if next_step == 1 and next_node.right:
            return self.path(steps, next_node.right)



# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
def frequencies(s):
    result = sorted([(c, s.count(c)) for c in set(s)], key=lambda x: -x[1])
    return result


# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    if len(freqs) <= 1:
        return None

    nodes = [Node(char=item[0], freq=item[1]) for item in freqs]

    tree = Tree(nodes)

    encoded = [tree.find(c) for c in s]

    result = "".join(encoded)

    return result


# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs, bits):
    if len(freqs) <= 1:
        return None

    nodes = [Node(char=item[0], freq=item[1]) for item in freqs]

    tree = Tree(nodes)

    bits = [int(bit) for bit in bits]

    result = ""

    while bits:
        result += tree.path(bits)

    return result