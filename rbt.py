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
    
    def get_successor(self):
        assert self.get_right() is not None
        current = self.get_right()
        while current.get_left() is not None:
            current = current.get_left()
        return current

    def set_value(self, value):
        self.value = value

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

    def find(self, value):
        current_node = self.root
        while current_node is not None:
            if current_node.get_value() == value:
                return current_node
            elif current_node.get_value() > value:
                current_node = current_node.get_left()
            else:
                current_node = current_node.get_right()
        return None

    def search(self, value):
        return self.find(value) is not None
    
    def insert(self, value):
        # Prevent duplicates
        if self.search(value):
            return False

        # Create the new node and insert it
        new_node = RBTNode(value, RBT.RED)
        if self.root is None:
            self.root = new_node
            self.root.set_color(RBT.BLACK)
        else:
            parent = self.get_future_parent(new_node)
            parent.insert_child(new_node)
            if parent.get_color() == RBT.RED:
                self.fix_redred(new_node)
        self.check_invariants()
        return True

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
    
    def fix_redred(self, new_node):
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
                    self.fix_redred(gparent)
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

    def delete(self, value):
        node = self.find(value)
        if node is None:
            return False
        parent = self.get_parent(node)
        
        # If the node has two children swap it with the inorder successor
        if node.get_left() is not None and node.get_right() is not None:
            successor = node.get_successor()
            # Get parent before messing up the tree
            parent = self.get_parent(successor)
            node_val = node.get_value()
            node.set_value(successor.get_value())
            successor.set_value(node_val)
            node = successor
        
        if node == self.root:
            # Set the new root and return
            self.root = node.get_left() if node.get_left() else node.get_right()
            return True

        if node.get_color() == RBT.RED:
            # If the node is red simply remove it from the tree (it can't have a single child)
            assert node.get_left() is None and node.get_right() is None
            if node == parent.get_left():
                parent.set_left(None)
            else:
                parent.set_right(None)
        else:
            child = node.get_left() if node.get_left() else node.get_right()
            if child is not None and child.get_color() == RBT.RED:
                # If the node has a red child we can swap and recolor
                child.set_color(RBT.BLACK)
                if node == parent.get_left():
                    parent.set_left(child)
                else:
                    parent.set_right(child)
            else:
                # The node is a leaf, remove it and fix the violation of black height
                assert child is None
                if node == parent.get_left():
                    parent.set_left(None)
                    sibling = parent.get_right()
                else:
                    parent.set_right(None)
                    sibling = parent.get_left()
                self.fix_black_height(parent, sibling)
        
        self.check_invariants()
        return True
    
    def fix_black_height(self, parent, sibling):
        assert sibling is not None
        if sibling.get_color() == RBT.RED:
            parent.set_color(RBT.RED)
            sibling.set_color(RBT.BLACK)
            gparent = self.get_parent(parent)
            if sibling == parent.get_left():
                new_sibling = sibling.get_right()
                parent.set_left(sibling.get_right())
                sibling.set_right(parent)
            else:
                new_sibling = sibling.get_left()
                parent.set_right(sibling.get_left())
                sibling.set_left(parent)
            if gparent:
                if parent == gparent.get_left():
                    gparent.set_left(sibling)
                else:
                    gparent.set_right(sibling)
            else:
                self.root = sibling

            sibling = new_sibling
        
        assert sibling is not None
        sl = sibling.get_left()
        sr = sibling.get_right()
        if parent.get_color() == RBT.BLACK and sibling.get_color() == RBT.BLACK and \
            (sl is None or sl.get_color() == RBT.BLACK) and (sr is None or sr.get_color() == RBT.BLACK):
            # Case 3: Recursive
            sibling.set_color(RBT.RED)
            gparent = self.get_parent(parent)
            if gparent is not None:
                if parent == gparent.get_left():
                    self.fix_black_height(gparent, gparent.get_right())
                else:
                    self.fix_black_height(gparent, gparent.get_left())
        elif parent.get_color() == RBT.RED and sibling.get_color() == RBT.BLACK and \
            (sl is None or sl.get_color() == RBT.BLACK) and (sr is None or sr.get_color() == RBT.BLACK):
            # Case 4
            sibling.set_color(RBT.RED)
            parent.set_color(RBT.BLACK)
        else:
            # Case 5
            if sibling.get_color() == RBT.BLACK:
                if sibling == parent.get_right() and \
                    (sl and sl.get_color() == RBT.RED) and (sr is None or sr.get_color() == RBT.BLACK):
                    
                    sibling.set_color(RBT.RED)
                    sl.set_color(RBT.BLACK)
                    sibling.set_left(sl.get_right())
                    sl.set_right(sibling)
                    parent.set_right(sl)
                    sibling = sl
                elif sibling == parent.get_left() and \
                    (sr and sr.get_color() == RBT.RED) and (sl is None or sl.get_color() == RBT.BLACK):

                    sibling.set_color(RBT.RED)
                    sr.set_color(RBT.BLACK)
                    sibling.set_right(sr.get_left())
                    sr.set_left(sibling)
                    parent.set_left(sr)
                    sibling = sr
            else:
                assert False
            
            # Case 6
            assert sibling.get_color() == RBT.BLACK
            gparent = self.get_parent(parent)
            sibling.set_color(parent.get_color())
            parent.set_color(RBT.BLACK)
            if sibling == parent.get_right():
                assert sibling.get_right().get_color() == RBT.RED
                sibling.get_right().set_color(RBT.BLACK)
                parent.set_right(sibling.get_left())
                sibling.set_left(parent)
            else:
                assert sibling.get_left().get_color() == RBT.RED
                sibling.get_left().set_color(RBT.BLACK)
                parent.set_left(sibling.get_right())
                sibling.set_right(parent)
            if gparent:
                if parent == gparent.get_left():
                    gparent.set_left(sibling)
                else:
                    gparent.set_right(sibling)
            else:
                self.root = sibling


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

