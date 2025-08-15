# Wordle Remake
# Made by Ruddra Hassan on 14th August 2025

from random import choice


class Heart:
    GREEN: str = "💚"  # Correct letter, correct position
    YELLOW: str = "💛"  # Correct letter, incorrect position
    GRAY: str = "🩶"  # Incorrect letter


class Color:
    GREEN: str = "\33[92m"  # Correct letter, correct position
    YELLOW: str = "\33[93m"  # Correct letter, incorrect position
    GRAY: str = "\33[37m"  # Incorrect letter
    RESET: str = "\33[0m"  # Reset color


NUM_GUESSES: int = 5  # <-- Change this to increase/decrease the number of allowed guesses
WORD_FILE: str = "words.txt"  # <-- Change this to word list file name
FEEDBACK_PREF: int = 1  # <-- 1. colored hearts   2. colored text


def initialize(file_path: str) -> list[str]:
    try:
        with open(file_path, "r") as file:
            word_list = [word.strip().lower() for word in file]
            word_list = [word for word in word_list if len(word) == 5]
        print(f"☑️ Successfully loaded in {len(word_list)} words")
        return word_list
    except IOError:
        print("⚠️ Critical Error: Word list not found")
        exit()


def select_word(word_list: list[str]) -> str:
    return choice(word_list)


def generate_feedback(secret: str, guess: str) -> str:
    feedback: list[str] = [""] * 5
    frequency: dict[str, int] = {}
    
    for char in secret:
        frequency[char] = frequency.get(char, 0) + 1
    
    for idx in range(5):
        if guess[idx] == secret[idx]:
            if FEEDBACK_PREF == 1:
                feedback[idx] = Heart.GREEN
            else:  # FEEDBACK_PREF == 2
                feedback[idx] = f"{Color.GREEN}{guess[idx]}{Color.RESET}"
            frequency[guess[idx]] -= 1
    
    for idx in range(5):
        if feedback[idx]:
            continue
        if guess[idx] in frequency and frequency[guess[idx]] > 0:
            if FEEDBACK_PREF == 1:
                feedback[idx] = Heart.YELLOW
            else:  # FEEDBACK_PREF == 2
                feedback[idx] = f"{Color.YELLOW}{guess[idx]}{Color.RESET}"
            frequency[guess[idx]] -= 1
        else:
            if FEEDBACK_PREF == 1:
                feedback[idx] = Heart.GRAY
            else:  # FEEDBACK_PREF == 2
                feedback[idx] = f"{Color.GRAY}{guess[idx]}{Color.RESET}"
    
    return "".join(feedback)


def play_game(word_list: list[str]) -> None:
    secret_word: str = select_word(word_list)
    feedbacks: list[str] = []
    guessed: bool = False
    
    for attempt in range(NUM_GUESSES):
        while True:
            guess: str = input(f"Guess {attempt + 1}/{NUM_GUESSES} >> ").lower()
            if len(guess) == 5:
                break
            print("⚠️ Invalid guess! Word must be 5 letters.")
        
        feedback: str = generate_feedback(secret_word, guess)
        feedbacks.append(feedback)
        print("\n".join(feedbacks))
        
        if guess == secret_word:
            print(f"\n💗 Word was: {secret_word.capitalize()}"
                  f"\nℹ️ Found in {attempt + 1} attempts\n")
            guessed = True
            break
    
    if not guessed:
        print(f"\n💔 Failed to guess word"
              f"\nℹ️ Word was {secret_word.capitalize()}\n")
    
    print("\n".join(feedbacks))


def print_instructions() -> None:
    print("\n--- Wordle ---"
          "\nGuess the 5-letter word!"
          f"\nYou have {NUM_GUESSES} attempts.")
    if FEEDBACK_PREF == 1:
        print(f"\n  - {Heart.GREEN} indicates a correct letter in the correct position."
              f"\n  - {Heart.YELLOW} indicates a correct letter in the wrong position."
              f"\n  - {Heart.GRAY} indicates a letter that is not in the word.\n")
    else:  # FEEDBACK_PREF == 2
        print(f"\n  - {Color.GREEN}Green{Color.RESET} indicates a correct letter in the correct position."
              f"\n  - {Color.YELLOW}Yellow{Color.RESET} indicates a correct letter in the wrong position."
              f"\n  - {Color.GRAY}Gray{Color.RESET} indicates a letter that is not in the word.\n")


def select_feedback_pref() -> int:
    while True:
        print("\nℹ️ Select feedback preference: "
              f"\n\t- [1] Colored Hearts {Heart.GREEN}{Heart.YELLOW}{Heart.GRAY} (DEFAULT)"
              f"\n\t- [2] Colored Text {Color.GREEN}Green{Color.RESET} {Color.YELLOW}Yellow{Color.RESET}"
              f" {Color.GRAY}Gray{Color.RESET}")
        pref: int = int(input(">> "))
        if pref in [1, 2]:
            return pref
        else:
            return 1


if __name__ == "__main__":
    words: list[str] = initialize(WORD_FILE)
    FEEDBACK_PREF = select_feedback_pref()
    print_instructions()
    while True:
        play_game(words)
        if input("\n🔃 Try again? [y/n] >> ").lower() == "n":
            break
