from rbt import RBT, RBTNode

def main():
    tree = RBT()
    node1 = RBTNode(1, 1)
    node2 = RBTNode(2, 1)
    node3 = RBTNode(3, 1)
    node2.set_left(node1)
    node2.set_right(node3)
    tree.root = node2
    print(tree.search(1))
    print(tree.search(2))
    print(tree.search(3))
    print(tree.search(4))

if __name__ == "__main__":
    main()