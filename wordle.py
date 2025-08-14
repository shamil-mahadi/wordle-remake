# WORDLE Remake
# Made by Ruddra Hassan on 14th August 2025

from random import randint
from typing import TextIO

WORD_LIST: list[str] = ["fiber", "movie", "local", "ready", "drill", "green", "occur", "smith", "drawn", "party",
                        "undue", "peace", "stuck", "those", "river", "guest", "block", "shirt", "proud", "royal"]
GREEN_BLOCK: str = "💚"
YELLOW_BLOCK: str = "💛"
GRAY_BLOCK: str = "🩶"
NUM_GUESS: int = 5


def initialize() -> None:
    try:
        file: TextIO = open("words.txt", "r")
        for word in file.readlines():
            WORD_LIST.append(word.strip())
        print("☑️ Word list successfully loaded.")
        print(f"ℹ️ There are {len(WORD_LIST)} words in list.")
        file.close()
    except IOError:
        print("⚠️ Critical Error: Word list could not be found")
        exit()


def get_word(word_list: list[str]) -> str:
    num_words: int = len(word_list)
    random_index: int = randint(0, num_words)
    return word_list[random_index]


initialize()
def main() -> None:
    secret_word: str = get_word(WORD_LIST)
    current_list: list[str] = [""] * NUM_GUESS
    guessed: bool = False
    for attempts in range(NUM_GUESS):
        current: str = ""
        while True:
            guess_word: str = input(f"Guess {attempts + 1}: ")
            if len(guess_word) == 5:
                break
            print("Invalid word, word must be 5 letters!")
        
        for this_character in range(5):
            if guess_word[this_character] == secret_word[this_character]:
                current += "💚"
            elif guess_word[this_character] in secret_word:
                current += "💛"
            else:
                current += "🩶"
        current_list[attempts] = current
        print(current)
        if current == "💚💚💚💚💚":
            print("\n")
            print(f"💗 Word was: {secret_word.capitalize()}")
            print(f"ℹ️ Guessed word in: {attempts + 1} attempts.")
            print("\n")
            for lines in current_list:
                print(lines)
            print("\n")
            guessed = True
            break
    
    if not guessed:
        print("\n")
        print("💔 Failed to guess word.")
        print(f"ℹ️ Word was: {secret_word.capitalize()}")
        print("\n")
        for lines in current_list:
            print(lines)
        print("\n")

if __name__ == '__main__':
    while True:
        main()
        if input("Try again? (y/n): ").lower() == "n":
            break