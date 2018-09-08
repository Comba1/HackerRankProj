import Queue as q
# from array import array

class TrieNodeT:
    def __init__(self):
        # self.healths = {}
        self.indexes = []  # array('L')
        self.healths = []
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

    def __init__(self, genes, healths):
        self.cnt = 0
        self.root = TrieNodeT()  # root has health 0
        self.queue = q.Queue()
        self.queue.put(self.root)

        self.build_trie(genes, healths)
        self.build_failures()

    def build_trie(self, genes, healths):

        cur = self.root
        for i, (gene, health) in enumerate(zip(genes, healths)):
            for char in gene:
                if char not in cur.children:
                    cur.children[char] = TrieNodeT()
                cur = cur.children[char]
            cur.healths.append(health)  # assigning a health for the specific gene when we reach the end of a word
            cur.indexes.append(i)
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
                    child_node.healths += child_node.failure_node.healths
                    child_node.indexes += child_node.failure_node.indexes
                self.queue.put(child_node)

    def calc_health(self, strand, first, last):

        i = 0
        s = strand[i]

        cur = self.root
        health = 0
        end = False
        while not end:
            if s in cur.children:
                cur = cur.children[s]
                #  collecting all the relevant healths
                for j, health_index in enumerate(cur.indexes):
                    if first <= health_index <= last:
                        health += cur.healths[j]
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

        return health


if __name__ == '__main__':
    # input_dict = {'a': 4, 'aa': 5, 'bd': 6, 'ab': 7, 'dc': 8, 'abd': 9}
    # genes = input_dict.keys()
    # healths = input_dict.values()

    # last = 5
    file = open("C:\\Users\\agantz\Documents\\private\\Development\\Python\HackerRank\\DNA_input02.txt")

    n = int(file.readline())

    genes = file.readline().rstrip().split()

    health = list(map(int, file.readline().rstrip().split()))

    s = int(file.readline())
    min = max = None
    trie = TrieT(genes, health)
    my_trie = TrieT(genes, health)
    # my_trie.calc_health(input_str, first, last)

    for line in file:
        firstLastd = line.split()

        first = int(firstLastd[0])

        last = int(firstLastd[1])

        d = firstLastd[2]
        h_total = 0
        # for j in range(first, last + 1):
        #     gene = genes[j]
        #     health = healths[j]
        #     for i in range(len(input_str) - len(gene) + 1):
        #         if gene == input_str[i: i + len(gene)]:
        #             h_total += health
        # print (h_total)
        health_total = 0
        health_total = my_trie.calc_health(d, first, last)
        if max == None:  # initialize
            max = health_total
            min = health_total
        elif health_total > max:
            max = health_total
        elif health_total < min:
            min = health_total
    print (str(min) + ' ' + str(max))
    file.close()

    # right answer: 15806635 20688978289
        # print (my_trie.cnt)
        # print (sum(input_dict.values()))

