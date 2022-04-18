import random

tries = 8
game_won = False
inputs = 0

print("H A N G M A N")
play_y_n = input('Type "play" to play the game, "exit" to quit:')
if play_y_n == "exit":
    quit()
print("")

word_list = ['python', 'java', 'kotlin', 'javascript']
chosen_word = random.choice(word_list)
word_set = set(chosen_word)
word_in_underscore = len(chosen_word) * "-"
chosen_word_list = list(chosen_word)
underscore_word_list = list(word_in_underscore)
already_tried_letter = set()
check_list = list("~" * len(chosen_word))

while tries:

    if chosen_word_list == check_list:
        game_won = True

    if game_won:
        print("")
        print(chosen_word)
        print("You guessed the word!")
        print("You survived!")
        break

    for i in underscore_word_list:
        print(i, end="")
    print("")
    input_letter = input("Input a letter: ")

    if not (input_letter.islower() and input_letter.isascii()):
        print("Please enter a lowercase English letter")
        print("", end="") if len(input_letter) != 1 else print("")
        if len(input_letter) != 1:
            print("You should input a single letter")
            print("")
        continue

    if len(input_letter) != 1:
        print("You should input a single letter")
        print("")
        continue

    if input_letter in already_tried_letter:
        print("You've already guessed this letter")
        print("")
        continue

    if (input_letter in word_set) and (input_letter not in already_tried_letter):
        for _ in range(chosen_word.count(input_letter)):
            underscore_word_list[chosen_word_list.index(input_letter)] = input_letter
            chosen_word_list[chosen_word_list.index(input_letter)] = "~"
            print("")
    elif input_letter not in word_set and input_letter not in already_tried_letter:
        already_tried_letter.add(input_letter)
        print("That letter doesn't appear in the word")
        print("") if tries > 1 and not game_won else print("", end="")
        if not game_won:
            tries -= 1

    already_tried_letter.add(input_letter)

else:
    print("You lost!")
