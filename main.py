from calculator import add, subtract, multiply, divide


def main():
    print("Workflow Tester Calculator")
    print(f"  3 + 4 = {add(3, 4)}")
    print(f"  10 - 6 = {subtract(10, 6)}")
    print(f"  5 * 7 = {multiply(5, 7)}")
    print(f"  9 / 2 = {divide(9, 2)}")


if __name__ == "__main__":
    main()