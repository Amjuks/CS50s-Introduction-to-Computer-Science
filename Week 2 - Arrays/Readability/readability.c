#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string sentence = get_string("Text : ");

    int c = 0, letters = 0, wordcount = 0, s = 0, length = strlen(sentence);

    for (c = 0; c < length; c++)
    {
        if (isalpha(sentence[c]))
        {
            letters++;
        }

        if (isalpha(sentence[c]) && (isspace(sentence[c + 1]) || sentence[c + 1] == 46 || sentence[c + 1] == 33 || sentence[c + 1] == 63
                                     || sentence[c + 1] == 44))
        {
            wordcount++;
        }

        if (sentence[c] == 46 || sentence[c] == 33 || sentence[c] == 63)
        {
            s++;
        }
    }

    float index = 0.0588 * (100 * (float) letters / (float) wordcount) - 0.296 * (100 * (float) s / (float) wordcount) - 15.8;

    if (index < 16 && index >= 0)
    {
        printf("Grade %i\n", (int) round(index));
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }

}
