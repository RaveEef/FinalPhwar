from Utilities import *
from TranspositionTable import *

def node(tiles, parent_hash):
    global TT
    new_node = dict()
    new_node['name'] = str()
    new_node['tiles'] = list(tiles)
    new_node['node_hash'] = TT.get_zhash(list(tiles))
    new_node['parent_hash'] = parent_hash
    new_node['n_children'] = 0
    return new_node

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

class BoardTree:

    def __init__(self):
        self.tree = list()

    def root(self, root_tiles):
        root_node = node(root_tiles, None)
        root_node['name'] = "ROOT"
        self.tree.append(root_node)

    def add_node(self, node_tiles, node_parent):
        new_node = node(node_tiles, node_parent)

        if len(filter(lambda x: x['node_hash'] == new_node['node_hash'], self.tree)) > 0:
            print "TRANSPOSITION"

        for n in self.tree:
            if n['node_hash'] == node_parent:
                n['n_children'] += 1
                if n['name'] == "ROOT":
                    new_node['name'] = "A" + str(n['n_children'])
                else:
                    new_node['name'] = chr(ord(n['name'][0]) + 1) + str(n['n_children'])

                print n['name'], new_node['name']
                break

        #parent_name = self.find_parent_name(node_parent)

        self.tree.append(new_node)
        #parent_index = self.tree.index(node_parent)

    def find_parent_name(self, node):
        for n in self.tree:
            if n['node_hash'] == node['parent_hash']:
                return n['name']
        return False



    def write_tree(self, filename):
        file = open(filename, "w")

        write_tree = list(self.tree)

        parent = write_tree[0]
        file.write("\n{:+^65}\n".format("  " + parent['name'] + "  "))
        file.write(print_hex(parent['tiles'], False))
        file.write("\n{:+^65}\n".format(""))

        while len(write_tree) > 0:
            parent = write_tree[0]
            for n in write_tree:
                if n['parent_hash'] == parent['node_hash']:
                    file.write("\n{:+^65}\n".format("  " + n['name'] + ", child of " + parent['name'] + "  "))
                    file.write(print_hex(n['tiles'], False))
                    file.write("\n{:+^65}\n".format(""))
            write_tree.remove(parent)




        '''root = self.tree[0]
        file.write("\n{:+^65}\n".format("  ROOT NODE  "))
        file.write(print_hex(root['tiles'], False))
        file.write("\n{:+^65}\n".format(""))

        file.write("\n{:+^65}\n".format("  NODES WITH ROOT AS PARENT  "))

        for node in self.tree:
            file.write("\n{:+^65}\n".format("  " + node['name'] + "  "))
            if node['parent'] == root['hash']:
                file.write(print_hex(node['tiles'], False))
        file.write("\n{:+^65}\n".format(""))'''


        file.close()

TREE = BoardTree()