from rbt import RBT, RBTNode
import random
import traceback

def main():
    tree = RBT()
    count = 0
    history = []
    numbers = [random.randint(0,10000) for i in range(1000)]
    print("started")
    for number in numbers:
        try:
            history.append(f"tree.insert({number})")
            tree.insert(number)
            count += 1
        except Exception as e:
            traceback.print_exc()
            print("\n".join(history))
            tree.render()
            print(count)
            break

if __name__ == "__main__":
    main()