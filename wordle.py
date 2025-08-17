# Wordle Remake
# Made by Ruddra Hassan on 14th August 2025

from random import choice

import pygame

pygame.init()

WORD_FILE: str = "words.txt"  # <-- Change this to word list file name
FPS: int = 60  # <-- Doesn't really matter, only affects the animation

# Colors (R, G, B)
COLOR_BACKGROUND: tuple = (42, 42, 42)
COLOR_CORRECT: tuple = (51, 153, 60)
COLOR_PRESENT: tuple = (153, 153, 51)
COLOR_ABSENT: tuple = (102, 102, 102)
COLOR_BORDER: tuple = (255, 255, 255)
COLOR_TEXT: tuple = (255, 255, 255)
COLOR_KEY_BG: tuple = (60, 60, 60)

# Sizes
TILE_SIZE: int = 70
TILE_GAP: int = 8
KEY_WIDTH: int = 45
KEY_HEIGHT: int = 55
KEY_GAP: int = 6
FONT_SIZE_TILE: int = 36
FONT_SIZE_KEY: int = 20
FONT_SIZE_MESSAGE: int = 32
FONT_SIZE_BUTTON: int = 24
PADDING: int = 30

# Keyboard Layout
KEYBOARD_ROWS: list[str] = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

# Global Variables
screen: pygame.Surface
clock: pygame.time.Clock
font_tile: pygame.font.Font
font_key: pygame.font.Font
font_message: pygame.font.Font
font_button: pygame.font.Font
window_width: int = 0
window_height: int = 0
board_start_x: int = 0
board_start_y: int = 0
keyboard_start_x: int = 0
keyboard_start_y: int = 0

# Game State
number_guesses: int = -1
current_guess: str = ""
current_row: int = 0
secret_word: str = ""
word_list: list[str] = []
guesses: list[str] = []
feedbacks: list[list[str]] = []
key_colors: dict[str, str] = {}
game_over: bool = False
game_won: bool = False
message: str = ""
message_timer: int = 0
game_state: str = "menu"  # menu, playing, game_over
shake_timer: int = 0
shake_row: int = -1
reveal_animation: list[dict] = []
typing_animation: dict = {}


def get_words(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            words: list[str] = [word.strip().lower() for word in file if len(word.strip()) == 5]
        print(f"☑️ Successfully loaded in {len(words)} words")
        return words
    except IOError:
        print("❌ Critical Error: Word list not found or could not be loaded")
        exit()


def get_frequency(item: str) -> dict[str, int]:
    frequency_map: dict[str, int] = {}
    for char in item:
        frequency_map[char] = frequency_map.get(char, 0) + 1
    return frequency_map


def get_feedback(secret: str, guess: str) -> list[str]:
    feedback: list[str] = [""] * 5
    frequency: dict[str, int] = get_frequency(secret)
    
    for idx, char in enumerate(guess):
        if char == secret[idx]:
            feedback[idx] = "correct"
            frequency[char] -= 1
    
    for idx, char in enumerate(guess):
        if feedback[idx]:
            continue
        if frequency.get(char, 0) > 0:
            feedback[idx] = "present"
            frequency[char] -= 1
        else:
            feedback[idx] = "absent"
    
    return feedback


def setup_window():
    global screen, window_width, window_height, board_start_x, board_start_y, keyboard_start_x, keyboard_start_y
    global font_tile, font_key, font_message, font_button
    
    board_width = 5 * TILE_SIZE + 4 * TILE_GAP
    board_height = number_guesses * TILE_SIZE + (number_guesses - 1) * TILE_GAP
    
    keyboard_width = 10 * KEY_WIDTH + 9 * KEY_GAP
    keyboard_height = 4 * KEY_HEIGHT + 9 * KEY_GAP
    
    window_width = max(board_width, keyboard_width) + 2 * PADDING
    window_height = board_height + keyboard_height + 3 * PADDING + 60
    
    board_start_x = (window_width - keyboard_width) // 2
    board_start_y = PADDING
    
    keyboard_start_x = (window_width - keyboard_width) // 2
    keyboard_start_y = board_start_y + board_height + PADDING + 60
    
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Wordle")
    
    font_tile = pygame.font.Font(None, FONT_SIZE_TILE)
    font_key = pygame.font.Font(None, FONT_SIZE_KEY)
    font_message = pygame.font.Font(None, FONT_SIZE_MESSAGE)
    font_button = pygame.font.Font(None, FONT_SIZE_BUTTON)


def draw_tile(x: int, y: int, letter: str, state: str, shake_offset: int = 0, scale: float = 1.0):
    tile_x = x + shake_offset
    
    actual_size = int(TILE_SIZE * scale)
    offset = (TILE_SIZE - actual_size) // 2
    
    match state:
        case "correct":
            color = COLOR_CORRECT
        case "present":
            color = COLOR_PRESENT
        case "absent":
            color = COLOR_ABSENT
        case _:
            color = COLOR_BACKGROUND
    
    if color != COLOR_BACKGROUND:
        tile_surface = pygame.Surface((actual_size, actual_size))
        tile_surface.set_alpha(128)
        tile_surface.fill(color)
        screen.blit(tile_surface, (tile_x + offset, y + offset))
    
    border_surface = pygame.Surface((actual_size, actual_size))
    border_surface.set_alpha(128)
    pygame.draw.rect(border_surface, COLOR_BORDER, (0, 0, actual_size, actual_size), 2)
    screen.blit(border_surface, (tile_x + offset, y + offset))
    
    if letter:
        text = font_tile.render(letter, True, COLOR_TEXT)
        text_rect = text.get_rect(center=(tile_x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        screen.blit(text, text_rect)


def draw_board():
    global shake_timer, reveal_animation, typing_animation
    
    shake_offset = 0
    if shake_timer > 0:
        shake_timer -= 1
        shake_offset = int(10 * pygame.math.Vector2(1, 0).rotate(shake_timer * 30).x)
    
    for anim in reveal_animation[:]:
        anim['progress'] += 0.15
        if anim['progress'] >= 1.0:
            reveal_animation.remove(anim)
    
    if typing_animation:
        typing_animation['scale'] += (1.0 - typing_animation['scale']) * 0.3
        if abs(typing_animation['scale'] - 1.0) < 0.01:
            typing_animation.clear()
    
    for row in range(number_guesses):
        for col in range(5):
            x = board_start_x + col * (TILE_SIZE + TILE_GAP)
            y = board_start_y + row * (TILE_SIZE + TILE_GAP)
            
            letter = ""
            state = ""
            current_shake = 0
            scale = 1.0
            
            if row < len(guesses):
                letter = guesses[row][col] if col < len(guesses[row]) else ""
                if row < len(feedbacks) and feedbacks[row]:
                    state = feedbacks[row][col]
                    
                    for anim in reveal_animation:
                        if anim['row'] == row and anim['col'] == col:
                            scale = 1.0 - abs(anim['progress'] - 0.5) * 0.4
                            if anim['progress'] < 0.5:
                                state = ""
            elif row == current_row:
                if col < len(current_guess):
                    letter = current_guess[col]
                    if typing_animation and typing_animation['row'] == row and typing_animation['col'] == col:
                        scale = typing_animation['scale']
                if shake_row == row:
                    current_shake = shake_offset
            
            draw_tile(x, y, letter, state, current_shake, scale)


def draw_key(x: int, y: int, letter: str, width: int = KEY_WIDTH):
    if letter in key_colors:
        match key_colors[letter]:
            case "correct":
                color = COLOR_CORRECT
            case "present":
                color = COLOR_PRESENT
            case _:
                color = COLOR_ABSENT
    else:
        color = COLOR_KEY_BG
    
    pygame.draw.rect(screen, color, (x, y, width, KEY_HEIGHT), border_radius=4)
    pygame.draw.rect(screen, COLOR_BORDER, (x, y, width, KEY_HEIGHT), 2, border_radius=4)
    
    match letter:
        case "ENTER":
            text = font_key.render("↵", True, COLOR_TEXT)
        case "BACK":
            text = font_key.render("⌫", True, COLOR_TEXT)
        case _:
            text = font_key.render(letter, True, COLOR_TEXT)
    text_rect = text.get_rect(center=(x + width // 2, y + KEY_WIDTH // 2))
    screen.blit(text, text_rect)


def draw_keyboard():
    # First row
    row_x = keyboard_start_x
    for idx, letter in enumerate(KEYBOARD_ROWS[0]):
        x = row_x + idx * (KEY_WIDTH + KEY_GAP)
        y = keyboard_start_y
        draw_key(x, y, letter)
    
    # Second row
    row_x = keyboard_start_x + (KEY_WIDTH + KEY_GAP) // 2
    for idx, letter in enumerate(KEYBOARD_ROWS[1]):
        x = row_x + idx * (KEY_WIDTH + KEY_GAP)
        y = keyboard_start_y + KEY_HEIGHT + KEY_GAP
        draw_key(x, y, letter)
    
    enter_width = int(KEY_WIDTH * 1.5)
    back_width = int(KEY_WIDTH * 1.5)
    
    # ENTER key
    x = keyboard_start_x
    y = keyboard_start_y + 2 * (KEY_HEIGHT + KEY_GAP)
    draw_key(x, y, "ENTER", enter_width)
    
    # Third row
    row_x = x + enter_width + KEY_GAP
    for idx, letter in enumerate(KEYBOARD_ROWS[2]):
        x = row_x + idx * (KEY_WIDTH + KEY_GAP)
        draw_key(x, y, letter)
    
    # BACKSPACE key
    x = row_x + len(KEYBOARD_ROWS[2]) * (KEY_WIDTH + KEY_GAP)
    draw_key(x, y, "BACK", back_width)


def draw_message():
    global message_timer
    
    if message and message_timer > 0:
        message_timer -= 1
        
        text = font_message.render(message, True, COLOR_TEXT)
        text_rect = text.get_rect(center=(window_width // 2, board_start_y + (number_guesses * (TILE_SIZE +
                                                                                                TILE_GAP)) // 2))
        padding = 20
        bg_rect = text_rect.inflate(padding * 2, padding)
        pygame.draw.rect(screen, (20, 20, 20), bg_rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDER, bg_rect, 2, border_radius=8)
        screen.blit(text, text_rect)


def draw_menu():
    screen.fill(COLOR_BACKGROUND)
    
    # Title
    title = font_message.render("WORDLE", True, COLOR_TEXT)
    title_rect = title.get_rect(center=(window_width // 2, 100))
    screen.blit(title, title_rect)
    
    # Instructions
    inst = font_button.render("Select number of guesses (3-10)", True, COLOR_TEXT)
    inst_rect = inst.get_rect(center=(window_width // 2, 200))
    screen.blit(inst, inst_rect)
    
    button_y = 250
    button_spacing = 60
    for idx in [3, 6, 10]:
        x = window_width // 2 - 4 * button_spacing + (idx - 3) * button_spacing
        
        button_rect = pygame.Rect(x - 25, button_y - 25, 50, 50)
        pygame.draw.rect(screen, COLOR_KEY_BG, button_rect, border_radius=4)
        pygame.draw.rect(screen, COLOR_BORDER, button_rect, 2, border_radius=4)
        
        num_text = font_button.render(str(idx), True, COLOR_TEXT)
        num_rect = num_text.get_rect(center=(x, button_y))
        screen.blit(num_text, num_rect)


def draw_game_over():
    button_text = "Press SPACE to play again or ESC to menu"
    text = font_button.render(button_text, True, COLOR_TEXT)
    text_rect = text.get_rect(center=(window_width // 2, keyboard_start_y + 4 * (KEY_HEIGHT + KEY_GAP) + 30))
    screen.blit(text, text_rect)


def handle_key_input(key: str):
    global current_guess, current_row, game_over, game_won, message, message_timer, shake_timer, shake_row
    global reveal_animation, typing_animation
    
    if game_over:
        return
    
    match key:
        case "BACK":
            if current_guess:
                current_guess = current_guess[:-1]
        case "ENTER":
            if len(current_guess) == 5:
                feedback = get_feedback(secret_word, current_guess)
                guesses.append(current_guess)
                feedbacks.append(feedback)
                
                for col in range(5):
                    reveal_animation.append({
                        'row': current_row,
                        'col': col,
                        'progress': -col * 0.1
                    })
                
                for idx, letter in enumerate(current_guess):
                    if feedback[idx] == "correct":
                        key_colors[letter] = "correct"
                    elif feedback[idx] == "present" and key_colors.get(letter) != "correct":
                        key_colors[letter] = "present"
                    elif letter not in key_colors:
                        key_colors[letter] = "absent"
                
                if current_guess == secret_word:
                    game_over = True
                    game_won = True
                    message = f"Amazing! Found in {current_row + 1} attempts!"
                    message_timer = 180
                else:
                    current_row += 1
                    if current_row >= number_guesses:
                        game_over = True
                        message = f"Word was: {secret_word}"
                        message_timer = 180
                current_guess = ""
            else:
                message = "Not 5-letters"
                message_timer = 60
                shake_timer = 10
                shake_row = current_row
        case _:
            if len(key) == 1 and key.isalpha() and len(current_guess) < 5:
                current_guess += key
                typing_animation = {
                    'row': current_row,
                    'col': len(current_guess) - 1,
                    'scale': 1.2
                }


def handle_mouse_click(pos):
    global game_state, number_guesses
    
    x, y = pos
    
    if game_state == "menu":
        button_y = 250
        button_spacing = 60
        for idx in [3, 6, 10]:
            button_x = window_width // 2 - 4 * button_spacing + (idx - 3) * button_spacing
            button_rect = pygame.Rect(button_x - 25, button_y - 25, 50, 50)
            if button_rect.collidepoint(x, y):
                number_guesses = idx
                setup_window()
                start_game()
                return ()
    elif game_state == "playing":
        row_x = keyboard_start_x
        for idx, letter in enumerate(KEYBOARD_ROWS[0]):
            key_x = row_x + idx * (KEY_WIDTH + KEY_GAP)
            key_y = keyboard_start_y
            if key_x <= x <= key_x + KEY_WIDTH and key_y <= y <= key_y + KEY_HEIGHT:
                handle_key_input(letter)
                return
        
        # Second row
        row_x = keyboard_start_x + (KEY_WIDTH + KEY_GAP) // 2
        for idx, letter in enumerate(KEYBOARD_ROWS[1]):
            key_x = row_x + idx * (KEY_WIDTH + KEY_GAP)
            key_y = keyboard_start_y + KEY_HEIGHT + KEY_GAP
            if key_x <= x <= key_x + KEY_WIDTH and key_y <= y <= key_y + KEY_HEIGHT:
                handle_key_input(letter)
                return
        
        # Third row with ENTER and BACK
        enter_width = int(KEY_WIDTH * 1.5)
        back_width = int(KEY_WIDTH * 1.5)
        
        # ENTER key
        key_x = keyboard_start_x
        key_y = keyboard_start_y + 2 * (KEY_HEIGHT + KEY_GAP)
        if key_x <= x <= key_x + enter_width and key_y <= y <= key_y + KEY_HEIGHT:
            handle_key_input("ENTER")
            return
        
        # Letter keys
        row_x = key_x + enter_width + KEY_GAP
        for idx, letter in enumerate(KEYBOARD_ROWS[2]):
            key_x = row_x + idx * (KEY_WIDTH + KEY_GAP)
            if key_x <= x <= key_x + KEY_WIDTH and key_y <= y <= key_y + KEY_HEIGHT:
                handle_key_input(letter)
                return
        
        # BACK key
        key_x = row_x + len(KEYBOARD_ROWS[2]) * (KEY_WIDTH + KEY_GAP)
        if key_x <= x <= key_x + back_width and key_y <= y <= key_y + KEY_HEIGHT:
            handle_key_input("BACK")
            return


def start_game():
    global secret_word, current_guess, current_row, guesses, feedbacks, key_colors, game_over, game_won, message
    global message_timer, game_state, shake_timer, shake_row, reveal_animation, typing_animation
    
    secret_word = choice(word_list)
    current_guess = ""
    current_row = 0
    guesses = []
    feedbacks = []
    key_colors = {}
    game_over = False
    game_won = False
    message = ""
    message_timer = 0
    game_state = "playing"
    shake_timer = 0
    shake_row = -1
    reveal_animation = []
    typing_animation = {}


def main():
    global clock, word_list, game_state, window_width, window_height, screen, font_message, font_button
    
    word_list = get_words(WORD_FILE)
    
    window_width = 600
    window_height = 400
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Wordle")
    
    font_message = pygame.font.Font(None, FONT_SIZE_MESSAGE)
    font_button = pygame.font.Font(None, FONT_SIZE_BUTTON)
    
    clock = pygame.time.Clock()
    game_state = "menu"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                        window_width = 600
                        window_height = 400
                        screen = pygame.display.set_mode((window_width, window_height))
                    elif event.key == pygame.K_BACKSPACE:
                        handle_key_input("BACK")
                    elif event.key == pygame.K_RETURN:
                        handle_key_input("ENTER")
                    elif event.key == pygame.K_SPACE and game_over:
                        start_game()
                    elif event.unicode and event.unicode.isalpha():
                        handle_key_input(event.unicode.upper())
                elif game_state == "menu":
                    if event.unicode.isdigit():
                        num = int(event.unicode)
                        if 3 <= num <= 9:
                            global number_guesses
                            number_guesses = num
                            setup_window()
                            start_game()
                    elif event.key == pygame.K_0:
                        number_guesses = 10
                        setup_window()
                        start_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)
        if game_state == "menu":
            draw_menu()
        elif game_state == "playing":
            screen.fill(COLOR_BACKGROUND)
            draw_board()
            draw_keyboard()
            draw_message()
            if game_over:
                draw_game_over()
        
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
