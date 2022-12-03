from string import ascii_letters

def filter_words_func():
    all_words_file = open("wordle/words/words.txt", "r")
    five_letter_words_file = open("wordle/words/five_letter_words.txt", "w")
    all_words = all_words_file.readlines()
    for word in all_words:
        valid = True
        index = 0
        for letter in word:
            if not str(letter) in ascii_letters and index < 5:
                valid = False
            index += 1
        if len(word) == 6 and valid:
            five_letter_words_file.write(word.lower())
    all_words_file.close()
    five_letter_words_file.close()
        