class RBTNode:
    def __init__(self, value, color, left=None, right=None, parent=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.value = value
        self.color = color
    
    def set_color(self, color):
        self.color = color
    
    def set_parent(self, parent):
        self.parent = parent

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def __repr__(self):
        return f'<RBTNode value={self.value} color={self.color}>'

class RBT:
    def __init__(self):
        self.root = None

    def search(self, value):
        current_node = self.root
        while current_node is not None:
            if current_node.value == value:
                return True
            elif current_node.value > value:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return False
    
    def insert(self, value):
        pass