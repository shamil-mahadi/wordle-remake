# Wordle Remake
# Made by Ruddra Hassan on 14th August 2025

from random import choice

GREEN_HEART: str = "💚"      # Correct letter, correct position
YELLOW_HEART: str = "💛"     # Correct letter, incorrect position
GRAY_HEART: str = "🩶"       # Incorrect letter

NUM_GUESSES: int = 5         # <-- Change this to increase/decrease the number of allowed guesses
WORD_FILE: str = "words.txt" # <-- Change this to word list file name


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
            feedback[idx] = GREEN_HEART
            frequency[guess[idx]] -= 1
    
    for idx in range(5):
        if feedback[idx]:
            continue
        if guess[idx] in frequency and frequency[guess[idx]] > 0:
            feedback[idx] = YELLOW_HEART
            frequency[guess[idx]] -= 1
        else:
            feedback[idx] = GRAY_HEART
    
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
        print(feedback)
        
        if feedback == GREEN_HEART * 5:
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
          f"\nYou have {NUM_GUESSES} attempts."
          f"\n  - {GREEN_HEART} indicates a correct letter in the correct position."
          f"\n  - {YELLOW_HEART} indicates a correct letter in the wrong position."
          f"\n  - {GRAY_HEART} indicates a letter that is not in the word.\n")

if __name__ == "__main__":
    words: list[str] = initialize(WORD_FILE)
    print_instructions()
    while True:
        play_game(words)
        if input("\n🔃 Try again? [y/n] >> ").lower() == "n":
            break
