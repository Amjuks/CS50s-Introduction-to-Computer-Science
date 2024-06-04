#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int nr, s, h, i, j; //nr - number of rows; s - space; h - hashtags; i and j are counters

    do
    {
        nr = get_int("Height: ");
    }
    while (nr < 1 || nr > 8);
    s = nr - 1;

    for (i = 1; i <= nr; i++)
    {
        for (j = 1; j <= s; j++)
        {
            printf(" ");
        }
        s--;
        for (h = 0; h < i; h++)
        {
            printf("#");
        }
        printf("\n");
    }
}
