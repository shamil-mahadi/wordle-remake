# Wordle Remake
# Made by Ruddra Hassan on 14th August 2025

from random import randint

WORD_LIST: list[str] = []

GREEN_HEART: str = "💚"      # Letter part of word, in that exact position
YELLOW_HEART: str = "💛"     # Letter part of word, not in that exact position
GRAY_HEART: str = "🩶"       # Letter not part of word

NUM_GUESSES: int = 5         # <-- Change this to increase/decrease the number of allowed guesses
WORD_FILE: str = "words.txt" # <-- Change this to word list file name


def initialize() -> None:
    try:
        with open(WORD_FILE, "r") as file:
            WORD_LIST.extend(word.strip() for word in file)
        print(f"☑️ Successfully loaded {len(WORD_LIST)} words.")
    except IOError:
        print("⚠️ Critical Error: Word list not found")
        exit()


def select_word(word_list: list[str]) -> str:
    return word_list[randint(0, len(word_list))]


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


def main() -> None:
    secret_word: str = select_word(WORD_LIST)
    feedbacks: list[str] = []
    guessed: bool = False
    
    for attempt in range(NUM_GUESSES):
        while True:
            guess: str = input(f"Guess {attempt + 1} >> ").lower()
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


if __name__ == "__main__":
    initialize()
    while True:
        main()
        if input("\n🔃 Try again? [y/n] >> ").lower() == "n":
            break
