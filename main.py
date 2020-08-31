from rbt import RBT
import sys

PROMPT = '''
Enter i to insert a number
      d to delete a number
      s to search for a number
      v to view the tree
      t to enter iteration mode
      x to exit
Command: '''

ITER_PROMPT = '''
Enter l to go left
      r to right
      p to go back to the parent
      x to exit iteration mode
Input: '''

def main():
    tree = RBT()
    while True:
        c = input(PROMPT)
        c = c.lower()
        if c.startswith('i'):
            if tree.insert(get_a_number()):
                print("The number was inserted in the tree.")
            else:
                print("The number is already in the tree.")
        elif c.startswith('d'):
            if tree.delete(get_a_number()):
                print("The number was deleted from the tree.")
            else:
                print("This number is not in the tree.")
        elif c.startswith('s'):
            if tree.search(get_a_number()):
                print("The number was found in the tree!")
            else:
                print("The number wasn't found :(")
        elif c.startswith('v'):
            tree.render()
        elif c.startswith('t'):
            if tree.root:
                print("You have entered the iteration mode!")
                iteration_mode(tree.root, tree)
            else:
                print("The tree is empty, add some values to iterate on.")
        elif c.startswith('x'):
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Wrong Input!")
        input("Press Enter to continue...")

def get_a_number():
    while True:
        try:
            num = int(input("Enter the number: "))
        except:
            print("Wrong input, you should enter a number!")
            continue
        break
    return num

def iteration_mode(current, tree):
    parent = tree.get_parent(current)
    print("Current node:")
    print(f"\tvalue = {current.get_value()}")
    print(f"\tleft child  = {current.get_left().get_value() if current.get_left() else 'null'}")
    print(f"\tright child  = {current.get_right().get_value() if current.get_right() else 'null'}")
    print(f"\tparnet  = {parent.get_value() if parent else 'null'}")
    c = input(ITER_PROMPT).lower()
    if c.startswith('l'):
        if current.get_left():
            iteration_mode(current.get_left(), tree)
        else:
            print("Can't go there, the node is null!")
            iteration_mode(current, tree)
    elif c.startswith('r'):
        if current.get_right():
            iteration_mode(current.get_right(), tree)
        else:
            print("Can't go there, the node is null!")
            iteration_mode(current, tree)
    elif c.startswith('p'):
        if parent:
            iteration_mode(parent, tree)
        else:
            print("Can't go there, the node is null!")
            iteration_mode(current, tree)
    elif c.startswith('x'):
        return
    else:
        print("Wrong Input!")
        iteration_mode(current, tree)

if __name__ == "__main__":
    main()