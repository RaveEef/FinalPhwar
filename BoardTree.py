from Utilities import *


def node(tiles, parent):
    new_node = {}
    new_node['tiles'] = list(tiles)
    new_node['parent'] = parent
    return new_node


class BoardTree:

    def __init__(self):
        self.tree = list()

    def root(self, root_tiles):
        root_node = node(root_tiles, None)
        self.tree.append(root_node)

    def add_node(self, node_tiles, node_parent):
        new_node = node(node_tiles, node_parent)


        if new_node in self.tree:
            print "NODE ALREADY IN TREE"
            return

        self.tree.append(new_node)
        parent_index = self.tree.index(node_parent)

    def find_node(self, tiles):
        for node in self.tree:
            if node['tiles'] == tiles:
                if node['parent'] is None:
                    print ""
                return node

        return False

    def write_tree(self, filename):
        file = open(filename, "w")

        root = self.tree[0]
        file.write("\n{:+^65}\n".format("  ROOT NODE  "))
        file.write(print_hex(root['tiles'], False))
        file.write("\n{:+^65}\n".format(""))

        file.write("\n{:+^65}\n".format("  NODES WITH ROOT AS PARENT  "))
        for node in self.tree:
            if node['parent'] == root:
                file.write(print_hex(node['tiles'], False))
        file.write("\n{:+^65}\n".format(""))


        file.close()

TREE = BoardTree()

# region BoardStack
class BoardStack:

    def __init__(self):
        self.stack = list()

    def push(self, data):
        # Checking to avoid duplicate entries
        if data not in self.stack:
            self.stack.append(data)
            return True
        return False

    def pop(self):
        if len(self.stack) <= 0:
            return ("Stack Empty!")
        # print  "POPPING FROM STACK, SIZE: ", len(self.stack)
        return self.stack.pop()

    def size(self):
        return len(self.stack)

    def peek(self, i=-1):
        return self.stack[i]

    def print_stack(self):
        if self.size() > 1:
            print print_hex(self.peek(-2))
        print print_hex(self.peek())

# endregion