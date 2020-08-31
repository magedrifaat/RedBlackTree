from rbt import RBT, RBTNode
import random
import traceback

def test():
    tree = RBT()
    count = 0
    history = []
    numbers = [random.randint(0, 1000000) for i in range(500)]
    print("started")
    for number in numbers:
        try:
            history.append(f"tree.insert({number})")
            tree.insert(number)
            count += 1
        except Exception as e:
            traceback.print_exc()
            print("\n".join(history))
            print(count)
            break

    print("deleting")
    numbers = list(set(numbers))
    for i in range(len(numbers)):
        try:
            deleted = random.choice(numbers)
            history.append(f"tree.delete({deleted})")
            numbers.remove(deleted)
            tree.delete(deleted)
        except:
            traceback.print_exc()
            print("\n".join(history))
            break
    assert tree.root is None


if __name__ == "__main__":
    test()