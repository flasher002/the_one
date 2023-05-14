import random
import string


def bot_move():
    if pencils % 4 == 0:
        print(3)
        return 3
    elif (pencils - 3) % 4 == 0 or pencils == 3:
        print(2)
        return 2
    elif (pencils - 2) % 4 == 0 or pencils == 2:
        print(1)
        return 1

    if pencils == 1:
        print(1)
        return 1
    else:
        random_turn = random.randint(1, 3)
        print(random_turn)
        return random_turn


def find_fault_message(object_to_map, purpose):
    if purpose == "starting_pencils":
        if object_to_map not in string.digits:
            return "The number of pencils should be numeric \n"
        elif object_to_map == "0":
            return "The number of pencils should be positive \n"
    elif purpose == "starting_player":
        if object_to_map not in players:
            return f"Choose between '{players[0]}' and '{players[1]}' \n"
    elif purpose == "taking_pencils":
        if object_to_map not in ["1", "2", "3"]:
            return "Possible values: '1', '2' or '3' \n"
    if purpose == "too_many_pencils":
        return "Too many pencils were taken \n"


def force_correct_answer_format(possible_answer, input_message, compoundable, no_alone_zero, purpose):
    initial_answer = input(input_message)
    if compoundable:
        answer = initial_answer
        while True:
            is_correct_form = 1
            for i in answer:
                if i in possible_answer:
                    is_correct_form *= 1
                else:
                    is_correct_form *= 0
            if bool(is_correct_form) and answer != "" and not (no_alone_zero and answer == "0"):
                return answer
            else:
                answer = input(find_fault_message(answer, purpose))
    else:
        answer = initial_answer
        while True:
            if answer == "" or (no_alone_zero and answer == "0"):
                answer = input(find_fault_message(answer, purpose))
                continue
            if answer in possible_answer:
                return answer
            if answer in string.digits:
                if int(answer) in possible_answer:
                    return answer
            answer = input(find_fault_message(answer, purpose))


pencils = int(force_correct_answer_format(string.digits, "How many pencils would you like to use: \n", True, True,
                                          "starting_pencils"))
players = ["Joni", "Josi"]
starting_player = force_correct_answer_format(players, f"Who will be the first ({players[0]}, {players[1]}): \n",
                                              False, False, "starting_player")

next_player = players.index(starting_player)

# Main game loop
while True:
    print("|" * pencils)
    if next_player == 1:
        print(f"{players[1]}'s turn!")
        next_player -= 1
    else:
        print(f"{players[0]}'s turn!")
        next_player += 1

    if next_player == 0:
        taken_pencils = bot_move()

    else:
        taken_pencils = int(force_correct_answer_format(["1", "2", "3"], "", False, False, "taking_pencils"))
        if taken_pencils > pencils:
            left_over_pencils = list(range(1, pencils + 1))
            taken_pencils = int(force_correct_answer_format(left_over_pencils, "Too many pencils were taken \n",
                                                            False, False, "too_many_pencils"))

    if taken_pencils == pencils:
        print(f"{players[next_player]} won!")
        break

    pencils -= taken_pencils
