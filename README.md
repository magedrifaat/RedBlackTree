# RedBlackTree
A python implementation of the red-black tree data structure.

## Usage
Run the following command to try out inserting, deleting, searching in the tree as well as viewing and iterating through it:
```
python main.py
```

The actual implementation of the data structure is the class RBT in the rbt.py module, if you intend to use it in a production environment make sure to turn off the assertions or delete them altogether.
## Example
```python
from rbt import RBT

tree = RBT()
tree.insert(1)
tree.insert(2)
tree.insert(3)

if tree.search(1):
  print("1 is in the tree")
 
tree.delete(1)
if not tree.search(1):
  print("1 is no more in the tree")
  
tree.render()
```
