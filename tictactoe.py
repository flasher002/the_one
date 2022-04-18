starting_state = "         "
print(starting_state)
game_state = [[x for x in starting_state[i * 3:3 * (i + 1)]] for i in range(3)]


def print_game_state():
    print("---------")
    print(f"| {game_state[0][0]} {game_state[0][1]} {game_state[0][2]} |")
    print(f"| {game_state[1][0]} {game_state[1][1]} {game_state[1][2]} |")
    print(f"| {game_state[2][0]} {game_state[2][1]} {game_state[2][2]} |")
    print("---------")
    print("")


print_game_state()

acceptable_input = False
end_game = False
player_turn = 0

while not end_game:
    input_row_column = input()

    for i in input_row_column:
        if not(i.isdigit() or i == " "):
            print("You should enter numbers!")
            continue

    input_row_column = input_row_column.split()

    input_row_column = [int(x) - 1 for x in input_row_column]

    input_row = int(input_row_column[0])
    input_column = int(input_row_column[1])

    if input_column > 2 or input_row > 2:
        print("Coordinates should be from 1 to 3")
        continue

    if game_state[input_row][input_column] != " ":
        print("This cell is occupied! Choose another one!")

    if game_state[input_row][input_column] == " ":
        game_state[input_row][input_column] = "X" if int(player_turn) == 0 else "O"
        player_turn = not(bool(player_turn))
        print_game_state()

    if game_state[0].count("X") == 3 or game_state[1].count("X") == 3 or game_state[2].count("X") == 3:
        print("X wins")
        break

    elif game_state[0].count("O") == 3 or game_state[1].count("O") == 3 or game_state[2].count("O") == 3:
        print("O wins")
        break

    elif (game_state[0][0] + game_state[1][0] + game_state[2][0]).count("X") == 3 or \
            (game_state[0][1] + game_state[1][1] + game_state[2][1]).count("X") == 3 or \
              (game_state[0][2] + game_state[1][1] + game_state[2][2]).count("X") == 3:
        print("X wins")
        break

    elif (game_state[0][0] + game_state[1][0] + game_state[2][0]).count("O") == 3 or \
            (game_state[0][1] + game_state[1][1] + game_state[2][1]).count("O") == 3 or \
            (game_state[0][2] + game_state[1][1] + game_state[2][2]).count("O") == 3:
        print("O wins")
        break

    elif (game_state[0][0] + game_state[1][1] + game_state[2][2]).count("X") == 3 or \
            (game_state[0][2] + game_state[1][1] + game_state[2][0]).count("X") == 3:
        print("X wins")
        break

    elif (game_state[0][0] + game_state[1][1] + game_state[2][2]).count("O") == 3 or \
            (game_state[0][2] + game_state[1][1] + game_state[2][0]).count("O") == 3:
        print("O wins")
        break

    elif game_state[0].count(" ") == 0 and game_state[1].count(" ") == 0 and game_state[2].count(" ") == 0:
        print("Draw")
        break
