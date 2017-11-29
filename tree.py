class Node:
    """ Represents a tree node with unique key and list of values. """

    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.key = key
        self.values = [value]


class Tree:
    """ Represents a BST tree of Node values. """

    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.add_node(key, value, self.root)

    def add_node(self, key, value, node):
        if key < node.key:
            if node.left is not None:
                self.add_node(key, value, node.left)
            else:
                node.left = Node(key, value)
        elif key == node.key:
            node.values.append(value)
        else:
            if node.right is not None:
                self.add_node(key, value, node.right)
            else:
                node.right = Node(key, value)

    def find(self, key):
        if self.root is not None:
            node = self.find_node(key, self.root)
            if node:
                return node.values

    def find_node(self, key, node):
        if key == node.key:
            return node
        elif key < node.key and node.left is not None:
            return self.find_node(key, node.left)
        elif key > node.key and node.right is not None:
            return self.find_node(key, node.right)
