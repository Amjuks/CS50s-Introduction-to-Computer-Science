from cs50 import get_int


def main():
    height = get_valid_int()
    width = height
    print_pattern(height, width)


def print_pattern(h, w):

    # to terminate the recursion
    if (h == 0):
        return

    # prints the current line of the pyramid
    print(" " * (h - 1), end="")
    print("#" * (w - h + 1), end="")
    print("  ", end="")
    print("#" * (w - h + 1), end="")
    print()

    # prints the bottom half of the pyramid
    print_pattern(h - 1, w)


def get_valid_int():

    # initializes i to 0
    i = 0

    # takes a valid input
    while True:
        i = get_int("Height: ")
        if i > 0 and i < 9:
            break

    return i


main()