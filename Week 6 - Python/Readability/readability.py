import math


def main():

    # takes input from user
    text = input("Text: ")

    # declarations
    word_count = 0
    letters = 0
    sentences = 0

    # determines number of words, letters and sentences
    for char in range(len(text)):
        if text[char].isalpha():
            letters += 1

            if text[char + 1] in ['.', '?', '!', ' ', ',']:
                word_count += 1

        if text[char] in ['.', '?', '!']:
            sentences += 1

    # using Coleman-Liau's index algorithm
    index = round(0.0588 * ((letters / word_count) * 100) - 0.296 * ((sentences/word_count) * 100) - 15.8)

    # prints the grade
    if index < 1:
        print("Before Grade 1")

    elif index > 15:
        print("Grade 16+")

    else:
        print(f"Grade {index}")


main()