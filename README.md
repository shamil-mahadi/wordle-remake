# Wordle Remake

This is a remake of the popular game [Wordle](https://www.nytimes.com/games/wordle/index.html) which I made using Python because I was bored as hell. The game is purely based on the CLI and does not have a GUI ~~yet~~.

#### What is wordle? 
If you have never played Wordle, what are you doing here?

#### How does it work?
~~IDK, read the code.~~ The program reads the 2000+ 5-letter words stored in a little file called `words.txt` (you can change the file path in the code) and stores it in an array and then randomly selects one of the word from the 2000+ 5-letter words so that the player can then struggle to find the word. How exciting! :3

Anyway, here are some pictures of the game:

<img width="790" height="444" alt="image" src="https://github.com/user-attachments/assets/3a86a9a6-9677-4a66-8bf7-4b7f1d4b2547" />

<img width="456" height="1533" alt="image" src="https://github.com/user-attachments/assets/91eef3f1-8628-428c-8b53-8ff1bbf5bb54" />

# How to play?
You can get a local copy of this project up and running by "cloning" the repository. Follow the steps below for your respective operating system:

### Prerequisites
Before you begin, make sure you have **Git** and **Python** installed on your computer. If you don't, you can download it from here:
- [git-scm](https://git-scm.com/downloads)
- [python](https://www.python.org/downloads/)

## Windows
#### 1. Open Command Prompt
You can do this by pressing `Win` + `R` and typing in `cmd`.
#### 2. Navigate to desired folder
Pick a place where you want to save this project (locally ofc). For example, to save it on your desktop, type:

`cd Desktop`

##### Proceed to **Step 3** below the macOS instructions.

## macOS
#### 1. Open Terminal
You can find it in `Applications/Utilities`, or by searching for "Terminal" in Spotlight.
#### 2. Navigate to desired folder
Pick a place where you want to save this project (locally ofc). For example, to save it on your desktop, type:

`cd ~/Desktop`

---

#### 3. Clone the repository
Copy and paste the following command. This will create a new folder with all the project files.

`git clone https://github.com/ruddra-hassan/wordle-remake`

#### 4. Enter the project directory
`cd wordle-remake`

#### 5. Run the main file
`python wordle.py`

If this command doesn't work, try using `py` instead

`py wordle.py`

