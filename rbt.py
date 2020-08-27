class RBTNode:
    def __init__(self, value, color, left=None, right=None):
        self.left = left
        self.right = right
        self.value = value
        self.color = color
    
    def get_value(self):
        return self.value
    
    def get_color(self):
        return self.color

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_color(self, color):
        self.color = color
    
    def insert_child(self, child):
        if child.get_value() < self.get_value():
            self.set_left(child)
        else:
            self.set_right(child)

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def __repr__(self):
        return f'<RBTNode value={self.value} color={self.color}>'

class RBT:
    BLACK = 0
    RED = 1
    def __init__(self):
        self.root = None

    def search(self, value):
        current_node = self.root
        while current_node is not None:
            if current_node.get_value() == value:
                return True
            elif current_node.get_value() > value:
                current_node = current_node.get_left()
            else:
                current_node = current_node.get_right()
        return False
    
    def insert(self, value):
        # Prevent duplicates
        if self.search(value):
            return

        # Create the new node and insert it
        new_node = RBTNode(value, RBT.RED)
        if self.root is None:
            self.root = new_node
            self.root.set_color(RBT.BLACK)
        else:
            parent = self.get_future_parent(new_node)
            parent.insert_child(new_node)
            if parent.get_color() == RBT.RED:
                self.fix_tree(new_node)
        self.check_invariants()

    def get_future_parent(self, new_node):
        current_node = self.root
        while True:
            if new_node.get_value() < current_node.get_value():
                if current_node.get_left() is None:
                    return current_node
                else:
                    current_node = current_node.get_left()
            else:
                if current_node.get_right() is None:
                    return current_node
                else:
                    current_node = current_node.get_right()
    
    def get_parent(self, node):
        current_node = self.root
        while current_node is not None:
            if node == current_node.get_left() or node == current_node.get_right():
                return current_node
            elif node.get_value() < current_node.get_value():
                current_node = current_node.get_left()
            else:
                current_node = current_node.get_right()
        return None
    
    def fix_tree(self, new_node):
        parent = self.get_parent(new_node)
        gparent = self.get_parent(parent)
        uncle = gparent.get_left() if gparent.get_left() != parent else gparent.get_right()

        # Case 3.1
        if uncle and uncle.get_color() == RBT.RED:
            parent.set_color(RBT.BLACK)
            uncle.set_color(RBT.BLACK)
            if gparent != self.root:
                assert self.get_parent(gparent) is not None
                gparent.set_color(RBT.RED)
                if self.get_parent(gparent).get_color() == RBT.RED:
                    # Fix grandparent in the same way
                    self.fix_tree(gparent)
        else:
            self.insert_with_rotation(new_node, parent, gparent)

    def insert_with_rotation(self, child, parent, gparent):
        # First, get child to outer part of the tree
        if parent == gparent.get_right() and child == parent.get_left():
            # Right rotation
            gparent.set_right(child)
            parent.set_left(child.get_right())
            child.set_right(parent)
            child, parent = parent, child
        elif parent == gparent.get_left() and child == parent.get_right():
            # Left rotation
            gparent.set_left(child)
            parent.set_right(child.get_left())
            child.set_left(parent)
            child, parent = parent, child
        
        # Second, promote parent and recolor
        if parent == gparent.get_left():
            gparent.set_left(parent.get_right())
            parent.set_right(gparent)
            if self.get_parent(gparent):
                if gparent == self.get_parent(gparent).get_left():
                    self.get_parent(gparent).set_left(parent)
                else:
                    self.get_parent(gparent).set_right(parent)
            else:
                self.root = parent
            parent.set_color(RBT.BLACK)
            gparent.set_color(RBT.RED)
        else:
            gparent.set_right(parent.get_left())
            parent.set_left(gparent)
            if self.get_parent(gparent):
                if gparent == self.get_parent(gparent).get_left():
                    self.get_parent(gparent).set_left(parent)
                else:
                    self.get_parent(gparent).set_right(parent)
            else:
                self.root = parent
            parent.set_color(RBT.BLACK)
            gparent.set_color(RBT.RED)

    def check_invariants(self):
        assert self.child_parent_invariant()
        assert self.root.get_color() == RBT.BLACK
        assert self.bst_invariant()
        assert self.both_children_of_red_are_black()
        assert self.all_paths_have_the_same_black()

    def child_parent_invariant(self):
        def recur_helper(tree):
            if tree is None:
                return True
            return (tree.get_left() is None or self.get_parent(tree.get_left()) == tree) and \
                   (tree.get_right() is None or self.get_parent(tree.get_right()) == tree) and \
                   recur_helper(tree.get_left()) and recur_helper(tree.get_right())
        return recur_helper(self.root)

    def bst_invariant(self):
        '''
        Checks the invariant of normal BSTs:
        "All elements in the left branch of an element
            are smaller than that element and all elements in
            the right branch of an element are greater than (or equal)
            that element"
        '''
        def bst_invariant_recur(tree):
            if tree is None:
                return True
            return (tree.get_left() is None or tree.get_left().get_value() <= tree.get_value()) and \
                   (tree.get_right() is None or tree.get_right().get_value() >= tree.get_value()) and \
                   bst_invariant_recur(tree.get_left()) and bst_invariant_recur(tree.get_right())
        return bst_invariant_recur(self.root)

    def both_children_of_red_are_black(self):
        '''
        Checks the fourth invariant of RB trees:
        "If a node is red, then both its children are black."
        '''
        def both_red(parent, child):
            return parent.get_color() == RBT.RED and child.get_color() == RBT.RED

        def recur_helper(tree):
            if tree is None:
                return True
            return not (tree.get_left() is not None and both_red(tree, tree.get_left())) and \
                   not (tree.get_right() is not None and both_red(tree, tree.get_right())) and \
                   recur_helper(tree.get_left()) and recur_helper(tree.get_right())

        return recur_helper(self.root)

    def all_paths_have_the_same_black(self):
        '''
        Checks the fifth invariant of RB trees:
        "Every path from a given node to any of its descendant
            None nodes goes through the same number of black nodes."
        '''
        def recur_helper(tree):
            if tree is None:
                return 0, False

            left, violation = recur_helper(tree.get_left())
            if violation:
                return 0, True

            right, violation = recur_helper(tree.get_right())
            if violation:
                return 0, True
            
            current = 1 if tree.get_color() == RBT.BLACK else 0
            return left + current, left != right

        violation = recur_helper(self.root)[1] 
        return not violation

