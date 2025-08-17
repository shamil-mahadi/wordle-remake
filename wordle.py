# Wordle Remake
# Made by Ruddra Hassan on 14th August 2025

from random import choice

WORD_FILE: str = "words.txt"  # <-- Change this to word list file name

COLOR_HEART: dict = {"correct": "💚", "present": "💛", "absent": "🩶"}
COLOR_TEXT: dict = {"correct": "\33[1;92m", "present": "\33[1;93m", "absent": "\33[1;37m", "reset": "\33[0m"}

# Global Variables
feedback_preference: int = -1
number_guesses: int = -1
word_list: list[str] = []


def get_words(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            words: list[str] = [word.strip().lower() for word in file if len(word.strip()) == 5]
        print(f"☑️ Successfully loaded in {len(words)} words")
        return words
    except IOError:
        print("❌ Critical Error: Word list not found or could not be loaded")
        exit()


def colorize(char: str, color: str) -> str:
    return COLOR_HEART[color] if feedback_preference == 1 else f"{COLOR_TEXT[color]}{char}{COLOR_TEXT['reset']}"


def get_frequency(item: str) -> dict[str, int]:
    frequency_map: dict[str, int] = {}
    for char in item:
        frequency_map[char] = frequency_map.get(char, 0) + 1
    return frequency_map


def get_feedback(secret: str, guess: str) -> str:
    feedback: list[str] = [""] * 5
    frequency: dict[str, int] = get_frequency(secret)
    
    for idx, char in enumerate(guess):
        if char == secret[idx]:
            feedback[idx] = colorize(char, "correct")
            frequency[char] -= 1
    
    for idx, char in enumerate(guess):
        if feedback[idx]:
            continue
        if frequency.get(char, 0) > 0:
            feedback[idx] = colorize(char, "present")
            frequency[char] -= 1
        else:
            feedback[idx] = colorize(char, "absent")
    
    return "".join(feedback)


def play_game() -> None:
    secret_word: str = choice(word_list)
    feedbacks: list[str] = []
    
    for attempt in range(number_guesses):
        guess: str = ""
        while len(guess) != 5:
            guess = input(f"Guess {attempt + 1}/{number_guesses} >> ").lower()
            if len(guess) != 5:
                print("⚠️ Invalid guess! Word must be 5 letters.")
        
        feedback: str = get_feedback(secret_word, guess)
        feedbacks.append(feedback)
        
        print("\n".join(feedbacks))
        
        if guess == secret_word:
            print(f"\n💗 Word was: {secret_word.capitalize()}"
                  f"\nℹ️ Found in {attempt + 1} attempts\n")
            break
    else:
        print(f"\n💔 Failed to guess word"
              "\nℹ️ Word was: {secret_word.capitalize()}\n")
    
    print("\n".join(feedbacks))


def print_instructions() -> None:
    print("\n--- Wordle ---"
          "\nGuess the 5-letter word!"
          f"\nYou have {number_guesses} attempts."
          f"\n\t- {colorize('Green', 'correct')} indicates a correct letter in the correct position."
          f"\n\t- {colorize('Yellow', 'present')} indicates a correct letter in the wrong position."
          f"\n\t- {colorize('Gray', 'absent')} indicates a letter that is not in the word.\n")


def toggle_feedback_frequency() -> int:
    while True:
        print("\nℹ️ Select feedback preference:"
              f"\n\t- [1] Colored Hearts {COLOR_HEART['correct']}{COLOR_HEART['present']}{COLOR_HEART['absent']}"
              f"\n\t- [2] Colored Text {COLOR_TEXT['correct']}Green{COLOR_TEXT['reset']}"
              f" {COLOR_TEXT['present']}Yellow{COLOR_TEXT['reset']} {COLOR_TEXT['absent']}Gray{COLOR_TEXT['reset']}")
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
                return num
            print("❌ Invalid number! Pick a valid positive integer")
        except ValueError:
            print("❌ Invalid number! Pick a valid positive integer")


def main() -> None:
    global feedback_preference
    global number_guesses
    global word_list
    
    word_list = get_words(WORD_FILE)
    feedback_preference = toggle_feedback_frequency()
    number_guesses = select_num_attempts()
    print_instructions()
    while True:
        play_game()
        if input("\n🔃 Try again? [y/n] >> ").lower().strip() == "n":
            break


if __name__ == "__main__":
    main()
