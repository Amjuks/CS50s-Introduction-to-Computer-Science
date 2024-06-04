#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{

    if (argv[2])
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    if (argc == 2) //Check conditions
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++) //Check each character in the string
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }

    int key = atoi(argv[1]);
    string ptext = get_string("plaintext: ");
    int l = strlen(ptext);

    printf("ciphertext: ");


    for (int i = 0; i < l; i++)
    {
        char c = ptext[i];

        if (isalpha(c))
        {
            if (isupper(c))
            {
                printf("%c", 'A' + (ptext[i] - 'A' + key) % 26);
            }
            else
            {
                printf("%c", 'a' + (ptext[i] - 'a' + key) % 26);
            }

        }
        else
        {
            printf("%c", c);
        }
    }

    printf("\n");
    return 0;

}
