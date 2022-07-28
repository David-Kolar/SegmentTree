from math import log2, ceil

class Node:
    def __init__(self, value):
        self.min = None
        self.max = None
        self.val = value
        self.left = None
        self.right = None
        self.parent = None

def soucet(a, b):
    return a + b

class SegmentTree:
    def __init__(self, posloupnost, funkce):
        posloupnost += [0]*(2**ceil(log2(len(posloupnost))) - len(posloupnost))
        self.delka = len(posloupnost)
        self.funkce = funkce
        pole = []
        for i, prvek in enumerate(posloupnost):
            n = Node(prvek)
            n.min = i
            n.max = i
            pole.append(n)

        while(len(pole)!=1):
            nove_pole = []
            for i in range(0, len(pole), 2):
                prvni = pole[i]
                druhe = pole[i+1]
                new_node = Node(funkce(prvni.val, druhe.val))
                new_node.left = prvni
                new_node.right = druhe
                new_node.min = prvni.min
                new_node.max = druhe.max
                prvni.parent = new_node
                druhe.parent = new_node
                nove_pole.append(new_node)
            pole = nove_pole
            self.root = pole[0]

    def find_val(self, index):
        aktualni = self.root
        while(True):
            if (aktualni.min == aktualni.max):
                return aktualni
            elif (aktualni.left.max >= index):
                aktualni = aktualni.left
            else:
                aktualni = aktualni.right

    def update_value(self, index, val):
        node = self.find_val(index)
        node.val = val
        while(True):
            node = node.parent
            node.val = self.funkce(node.left.val, node.right.val)
            if (node == self.root):
                return
    def interval(self, a, b):
        pointer1 = self.find_val(a)
        pointer2 = self.find_val(b)
        val1 = pointer1.val
        val2 = pointer2.val
        while(True):
            if (pointer1.parent==pointer2.parent):
                return self.funkce(val1, val2)
            parent1 = pointer1.parent
            parent2 = pointer2.parent
            if (parent1.left == pointer1):
                val1 = self.funkce(val1, parent1.right.val)
            if (parent2.right == pointer2):
                val2 = self.funkce(val2, parent2.left.val)
            pointer1 = parent1
            pointer2 = parent2

def NRP(pole):
    nove_pole = []
    tabulka = dict()
    index = 0
    for prvek in pole:
        if (index == 0) or (nove_pole[-1]!=prvek):
            nove_pole.append(prvek)
            index += 1
    nove_pole.sort()
    for i, prvek in enumerate(nove_pole):
        tabulka[prvek] = i
    nove_pole = [0]*len(nove_pole)
    strom = SegmentTree(nove_pole, max)
    for prvek in pole:
        index = tabulka[prvek]
        maximum = strom.interval(0, index) + 1
        strom.update_value(index, maximum)
    return strom.interval(0, len(nove_pole)-1)

pole = [1, 2, 100, 3, 2, 1, 2, 3, 4, 4, 5, 6, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.71, 1.72, 1.73, 1.74]
print(NRP(pole))
