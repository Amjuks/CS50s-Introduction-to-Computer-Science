#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BUFFER_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *img_inpt = fopen(argv[1], "r");

    if (img_inpt == NULL)
    {
        printf("Could not open file");
        return 1;
    }

    BYTE buffer[BUFFER_SIZE];
    FILE *img_otpt = NULL;
    int counter = 0;
    int jpgfound = 0;
    char filename[8];

    while (fread(buffer, BUFFER_SIZE, 1, img_inpt) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpgfound == 1)
            {
                fclose(img_otpt);
            }
            else
            {
                jpgfound = 1;
            }

            sprintf(filename, "%03i.jpg", counter++);
            img_otpt = fopen(filename, "w");
            fwrite(buffer, BUFFER_SIZE, 1, img_otpt);
        }
        else
        {
            if (jpgfound == 1)
            {
                fwrite(buffer, BUFFER_SIZE, 1, img_otpt);
            }
        }
    }

    fclose(img_inpt);
    return 0;
}