// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 30000;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //declarations
    int h = hash(word);       //hashing the word to find it's index in the hashtable
    node *cursor = table[h];  //to move through the linked list

    while (cursor != NULL)
    {
        if (!(strcasecmp(cursor->word, word) == 0))
        {
            cursor = cursor->next;
        }
        else
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
//hash function posted on reddit by delipity
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c); /* hash * 33 + c */
    }

    return hash % N;
}

//variable to keep track of words
int word_count = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //declarations
    FILE *file = fopen(dictionary, "r");
    char word[LENGTH + 1];

    //returns false if the file is NULL
    if (file == NULL)
    {
        return false;
    }

    while (fscanf(file, "%s", word) != EOF)
    {
        //create a node
        node *n = malloc(sizeof(node));

        //check if the created node is NULL
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word); //copy the string into the node
        n->next = NULL;
        int h = hash(word); //hashing the string

        //inserting node to hashtable
        n->next = table[h];
        table[h] = n;
        word_count++;

    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //declarations
    node *cursor;
    node *tmp;

    //iterates true each index in the hashtable
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        tmp = cursor;

        //iterates through each node in the linked list
        while (cursor != NULL)
        {
            cursor = tmp->next;
            free(tmp);
            tmp = cursor;
        }
    }

    return true;
}
