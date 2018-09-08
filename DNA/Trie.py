import Queue as q


class TrieNodeT:
    def __init__(self):
        self.health = 0
        self.children = {}
        self.failure_node = None

    def set_failure_node(self, node, char):

        if char in node.children:
            self.failure_node = node.children[char]
        elif node.failure_node is None:  # root node!
            self.failure_node = node
        else:
            self.set_failure_node(node.failure, char)


class TrieT:

    def __init__(self, input_dict):
        self.cnt = 0
        self.root = TrieNodeT()  # root has health 0
        self.queue = q.Queue()
        self.queue.put(self.root)

        self.build_trie(input_dict)
        self.build_failures()

    def calc_health_dbg(self, node):
        self.cnt += node.health
        for key in node.dict:
            self.calc_health (node.dict[key])

    def build_trie(self, input_dict):

        cur = self.root
        # cur.failure = cur
        for word in input_dict:
            for char in word:
                if char not in cur.children:
                    cur.children[char] = TrieNodeT()
                cur = cur.children[char]
            cur.health = input_dict[word]  # assigning a health when we reach the end of the word
            cur = self.root

    def build_failures(self):

        while not self.queue.empty():
            node = self.queue.get()
            for char, child_node in node.children.items():
                if node == self.root:
                    child_node.failure_node = node
            # child.failure = node for child in node.dict.values
                else:
                    child_node.set_failure_node(node.failure_node, char)
                    child_node.health += child_node.failure_node.health
                self.queue.put(child_node)

    def calc_health(self, strand):

        i = 0
        s = strand[i]

        cur = self.root
        health = 0
        end = False
        hit = False
        while not end:
            if s in cur.children:
                cur = cur.children[s]
                hit = True
                if i == len(strand) - 1:
                    end = True
                else:
                    i += 1
                    s = strand[i]
            else:
                if cur.failure_node:  # if has failure- continue to search the same char in the failure node
                    cur = cur.failure_node
                else:  # cur is root- increment
                    if i == len(strand) - 1:
                        end = True
                    else:
                        i += 1
                        s = strand[i]
            if hit:
                health += cur.health
                hit = False
        print (health)


if __name__ == '__main__':
    input_dict = {'a': 4, 'aa': 5, 'bd': 6, 'ab': 7, 'dc': 8, 'abd': 9}
    input_str = 'acaabdcabd'

    my_trie = TrieT(input_dict)
    my_trie.calc_health(input_str)

    h_total = 0
    for gene, health in input_dict.items():
        for i in range(len(input_str) - len(gene) + 1):
            if gene == input_str[i: i + len(gene)]:
                h_total += health
    print (h_total)
    # my_trie.calc_health(my_trie.root)
    # print (my_trie.cnt)
    # print (sum(input_dict.values()))

