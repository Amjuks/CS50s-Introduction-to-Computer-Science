from cs50 import get_float


def main():

    # declarations and initializations
    dollars = get_positive_float()
    coins = round(dollars * 100)
    num_coins = 0

    # calculates number of coins
    if coins >= 25:
        num_coins = coins // 25
        coins %= 25

    if coins >= 10:
        num_coins += coins // 10
        coins %= 10

    if coins >= 5:
        num_coins += coins // 5
        coins %= 5

    if coins >= 1:
        num_coins += coins

    print(int(num_coins))


def get_positive_float():

    # initializes i to 0
    i = 0

    # gets a valid input
    while True:
        i = get_float("Change owed: ")
        if i > 0:
            break

    return i


main()