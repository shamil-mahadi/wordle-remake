# Wordle Remake
# Made by Ruddra Hassan on 14th August 2025

from random import choice

WORD_FILE: str = "words.txt"  # <-- Change this to word list file name

color_heart: dict = {"green": "💚", "yellow": "💛", "gray": "🩶"}
color_text: dict = {"green": "\33[1;92m", "yellow": "\33[1;93m", "gray": "\33[1;37m", "reset": "\33[0m"}
feedback_pref: int = 1


def initialize(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            word_list = [word.strip().lower() for word in file if len(word.strip()) == 5]
        print(f"☑️ Successfully loaded in {len(word_list)} words")
        return word_list
    except IOError:
        print("❌ Critical Error: Word list not found or could not be loaded")
        exit()


def select_word(word_list: list[str]) -> str:
    return choice(word_list)


def colorize(char: str, color: str, pref: int) -> str:
    return color_heart[color] if pref == 1 else f"{color_text[color]}{char}{color_text['reset']}"


def generate_feedback(secret: str, guess: str, pref: int) -> str:
    feedback: list[str] = [""] * 5
    frequency: dict[str, int] = {char: secret.count(char) for char in secret}
    
    for idx, char in enumerate(guess):
        if guess[idx] == secret[idx]:
            feedback[idx] = colorize(char, "green", pref)
            frequency[char] -= 1
    
    for idx, char in enumerate(guess):
        if feedback[idx]:
            continue
        if frequency.get(char, 0) > 0:
            feedback[idx] = colorize(char, "yellow", pref)
            frequency[char] -= 1
        else:
            feedback[idx] = colorize(char, "gray", pref)
    
    return "".join(feedback)


def play_game(word_list: list[str], num_guesses: int, pref: int) -> None:
    secret_word: str = select_word(word_list)
    feedbacks: list[str] = []
    
    for attempt in range(num_guesses):
        guess: str = ""
        while len(guess) != 5:
            guess = input(f"Guess {attempt + 1}/{num_guesses} >> ").lower()
            if len(guess) != 5:
                print("⚠️ Invalid guess! Word must be 5 letters.")
        
        feedback: str = generate_feedback(secret_word, guess, pref)
        feedbacks.append(feedback)
        print("\n".join(feedbacks))
        
        if guess == secret_word:
            print(f"\n💗 Word was: {secret_word.capitalize()}"
                  f"\nℹ️ Found in {attempt + 1} attempts\n")
            break
    else:
        print(f"\n💔 Failed to guess word"
              f"\nℹ️ Word was: {secret_word.capitalize()}\n")
    print("\n".join(feedbacks))


def print_instructions(num_guesses: int, pref: int) -> None:
    print("\n--- Wordle ---"
          "\nGuess the 5-letter word!"
          f"\nYou have {num_guesses} attempts."
          f"\n  - {colorize('Green', 'green', pref)} indicates a correct letter in the correct position."
          f"\n  - {colorize('Yellow', 'yellow', pref)} indicates a correct letter in the wrong position."
          f"\n  - {colorize('Gray', 'gray', pref)} indicates a letter that is not in the word.\n")


def select_feedback_pref() -> int:
    while True:
        print("\nℹ️ Select feedback preference: "
              f"\n\t- [1] Colored Hearts {color_heart['green']}{color_heart['yellow']}{color_heart['gray']} (DEFAULT)"
              f"\n\t- [2] Colored Text {color_text['green']}Green{color_text['reset']} "
              f"{color_text['yellow']}yellow{color_text['reset']} {color_text['gray']}Gray{color_text['reset']}")
        try:
            pref: int = int(input(">> "))
            if pref in [1, 2]:
                return pref
            print("❌ Invalid option! Pick a valid option [1/2]")
        except ValueError:
            print("❌ Invalid option! Pick a valid option [1/2]")


def select_num_attempts() -> int:
    while True:
        print("\nℹ️ Select number of attempts (DEFAULT: 6)")
        try:
            num: int = int(input(">> "))
            if num > 0:
                if 5 < num > 10 and input("⚠️ Are you sure? [y/n] >> ").lower().strip() != "n":
                    return num
                return num
            print("❌ Invalid number! Pick a valid positive integer")
        except ValueError:
            print("❌ Invalid number! Pick a valid positive integer")


def main() -> None:
    words: list[str] = initialize(WORD_FILE)
    pref = select_feedback_pref()
    num_guesses = select_num_attempts()
    print_instructions(num_guesses, pref)
    while True:
        play_game(words, num_guesses, pref)
        if input("\n🔃 Try again? [y/n] >> ").lower().strip() == "n":
            break


if __name__ == "__main__":
    main()
