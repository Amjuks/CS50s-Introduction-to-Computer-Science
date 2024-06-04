#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int nr, s, j, i, h; //nr - number of rows; s - space; h - hashtags; i and j are counters

    do
    {
        nr = get_int("Height: ");
    }
    while (nr > 8 || nr < 1);
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

        printf("  ");

        for (h = 0; h < i; h++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}

