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
            pass
        elif c.startswith('t'):
            pass
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

if __name__ == "__main__":
    main()