#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars;

    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

    int coins = round(dollars * 100), numOfCoins = 0;

    if (coins >= 25)
    {
        numOfCoins = (coins / 25);
        coins = coins % 25;
    }

    if (coins >= 10)
    {
        numOfCoins = numOfCoins + (coins / 10);
        coins = coins % 10;
    }

    if (coins >= 5)
    {
        numOfCoins = numOfCoins + (coins / 5);
        coins = coins % 5;
    }

    if (coins >= 1)
    {
        numOfCoins = numOfCoins + coins;
    }

    printf("%i\n", numOfCoins);
}
