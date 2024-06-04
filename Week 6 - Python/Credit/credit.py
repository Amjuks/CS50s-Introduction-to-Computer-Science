from cs50 import get_int
from math import floor


def main():

    # initializations and declarations
    card_num = get_valid_int()
    card_num_copy = card_num
    c_len = 0
    every_two_digits = 0
    other_digits = 0

    # prerequisites for Luhn's algorithm
    while card_num > 0:

        if c_len % 2 == 0:
            other_digits += card_num % 10
        else:
            last_digit = 2 * (card_num % 10)
            every_two_digits += (last_digit // 10) + (last_digit % 10)

        c_len += 1
        card_num //= 10

    # uses Luhn's algorithm
    two_digits = card_num_copy // (10 ** (c_len - 2))
    sum_digits = every_two_digits + other_digits

    # determines which card it is
    if sum_digits % 10 != 0:
        print("INVALID")

    else:
        if two_digits > 50 and two_digits < 56:
            print("MASTERCARD")

        elif two_digits == 34 or two_digits == 37:
            print("AMEX")

        elif floor(two_digits // 10) == 4:
            print("VISA")

        else:
            print("INVALID")


def get_valid_int():

    # initializes i to 0
    i = 0

    # gets a valid input
    while True:
        i = get_int("Number: ")
        if i > 0 and isinstance(i, int):
            break

    return i


main()