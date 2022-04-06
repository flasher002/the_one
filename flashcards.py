import logging
import argparse

card_dict = dict()
check_list = list()
order_list = list()
statistics_dict = dict()

logging.basicConfig(filename="/home/luc/test/logging_data.txt",
                    filemode="w",
                    format='%(message)s',
                    level="DEBUG")


def check_definition(definition, term_check=False):
    for j in check_list:
        if j[1] == definition and not term_check:
            return j[1]
        elif j[1] == definition and term_check:
            return j[0]
    else:
        return False


def add_to_stat_dict():
    for key in card_dict.keys():
        if key not in statistics_dict:
            statistics_dict[key] = [0, 0, False]

        if key not in card_dict and key in statistics_dict:
            statistics_dict.pop(key)


def check_term(term, found_index=False):
    if found_index:
        index = 0
        for j in check_list:
            index += 1
            if j[0] == term:
                return f"{index - 1}:{j[0]}"

    for j in check_list:
        if j[0] == term:
            return term
    else:
        return False


def try_again(to_try_again, term_check=False, definition_check=False):
    if term_check:
        right_input = False
        new_try = to_try_again
        while not right_input:
            new_try = input(f'The card "{new_try}" already exists. Try again:\n')
            logging.debug(f'The card "{new_try}" already exists. Try again:')
            logging.debug(new_try)
            if check_term(new_try):
                continue
            else:
                return new_try

    elif definition_check:
        right_input = False
        new_try = to_try_again
        while not right_input:
            new_try = input(f'The definition "{new_try}" already exists. Try again:\n')
            logging.debug(f'The definition "{new_try}" already exists. Try again:')
            logging.debug(new_try)
            if check_definition(new_try):
                continue
            else:
                return new_try


def add_cards():
    term = input("The card:\n")
    logging.debug("The card:")
    logging.debug(term)
    logging.debug(term)
    if check_term(term):
        term = try_again(term, True)
        order_list.append(term)
    else:
        order_list.append(term)

    definition = input("The definition of the card:\n")
    logging.debug("The definition of the card:")
    logging.debug(definition)
    if check_definition(definition):
        definition = try_again(definition, False, True)

    card_dict[term] = definition
    check_list.append([term, definition])
    print(f'The pair ("{term}":"{definition}") has been added.\n')
    logging.info(f'the pair ("{term}":"{definition}") has been added.')
    cards_save_file = open("/home/luc/test/existing_cards.txt", "a+")
    cards_save_file.write(f"{term}:{definition}\n")
    cards_save_file.close()
    add_to_stat_dict()


def ask_cards(num_cards):
    logging.debug(num_cards)
    add_to_stat_dict()
    if num_cards > len(order_list):
        reset_counter = 0
        num_remaining_questions = num_cards
        while num_remaining_questions != 0:
            guess = input(f'Print the definition of "{order_list[reset_counter]}":\n')
            logging.info(f'Print the definition of "{order_list[reset_counter]}":')
            logging.debug(guess)
            if guess == card_dict[order_list[reset_counter]]:
                print("Correct!")
                logging.debug("Correct!")
                statistics_dict[order_list[reset_counter]][0] = statistics_dict[order_list[reset_counter]][0] + 1
                statistics_dict[order_list[reset_counter]][1] = statistics_dict[order_list[reset_counter]][1] + 1
            elif check_definition(guess):
                print(f'Wrong. The right answer is "{card_dict[order_list[reset_counter]]}", but '
                      f'your definition is correct for "{check_definition(guess, True)}".')
                logging.debug(f'Wrong. The right answer is "{card_dict[order_list[reset_counter]]}", but '
                              f'your definition is correct for "{check_definition(guess, True)}".')
                statistics_dict[order_list[reset_counter]][0] = statistics_dict[order_list[reset_counter]][0] + 1
            else:
                print(f'Wrong. The right answer is "{card_dict[order_list[reset_counter]]}".')
                logging.debug(f'Wrong. The right answer is "{card_dict[order_list[reset_counter]]}".')
                statistics_dict[order_list[reset_counter]][0] = statistics_dict[order_list[reset_counter]][0] + 1
            reset_counter += 1
            if reset_counter == (len(order_list)):
                reset_counter = 0
            num_remaining_questions -= 1
        return

    for i in range(num_cards):
        guess = input(f'Print the definition of "{order_list[i]}":\n')
        logging.debug(f'Print the definition of "{order_list[i]}":')
        logging.debug(guess)
        if guess == card_dict[order_list[i]]:
            print("Correct!")
            logging.debug("Correct!")
            statistics_dict[order_list[i]][0] = statistics_dict[order_list[i]][0] + 1
            statistics_dict[order_list[i]][1] = statistics_dict[order_list[i]][1] + 1
        elif check_definition(guess):
            print(f'Wrong. The right answer is "{card_dict[order_list[i]]}", but your definition '
                  f'is correct for "{check_definition(guess, True)}".')
            logging.debug(f'Wrong. The right answer is "{card_dict[order_list[i]]}", but your definition '
                          f'is correct for "{check_definition(guess, True)}".')
            statistics_dict[order_list[i]][0] = statistics_dict[order_list[i]][0] + 1
        else:
            print(f'Wrong. The right answer is "{card_dict[order_list[i]]}".')
            logging.debug(f'Wrong. The right answer is "{card_dict[order_list[i]]}".')
            statistics_dict[order_list[i]][0] = statistics_dict[order_list[i]][0] + 1


def remove_cards():
    add_to_stat_dict()
    to_remove = input("Which card?\n")
    logging.debug("Which card?")
    logging.debug(to_remove)
    found_return_string = check_term(to_remove, True)
    if found_return_string:
        found_index, found_value = found_return_string.split(":")
        del card_dict[found_value]
        check_list.pop(int(found_index))
        order_list.pop(int(found_index))
        print("The card has been removed")
        logging.debug("The card has been removed")

    else:
        print(f"Can't remove \"{to_remove}\": there is no such card.")
        logging.debug(f"Can't remove \"{to_remove}\": there is no such card.")

    existing_card_file = open("/home/luc/test/existing_cards.txt", "w")
    for term, definition in card_dict.items():
        existing_card_file.write(f"{term}:{definition}\n")
    existing_card_file.close()


def import_cards(starting_file=None):
    add_to_stat_dict()
    if starting_file:
        to_import = starting_file
    else:
        to_import = input("File name:\n")
        logging.debug("File name:")
        logging.debug(to_import)
    try:
        file_to_import = open(to_import, "r")
    except FileNotFoundError:
        print("File not found")
        logging.debug("File not found")
    else:
        lines = 0
        for line in file_to_import:
            duplicate = False
            term, definition = line.strip().split(":")
            card_dict[term] = definition
            for index in check_list:
                if index[0] == term:
                    duplicate = True
                    change_index = check_list.index(index)
                    check_list.pop(change_index)
                    check_list.insert(change_index, [term, definition])
                    order_list.pop(change_index)
                    order_list.insert(change_index, term)

            if not duplicate:
                check_list.append([term, definition])
                order_list.append(term)

            cards_save_file = open("/home/luc/test/existing_cards.txt", "a+")
            cards_save_file.write(f"{term}:{definition}\n")
            lines += 1
            cards_save_file.close()

        file_to_import.close()
        print(f"{lines} cards have been loaded.")
        logging.debug(f"{lines} cards have been loaded.")

        existing_cards_file = open("/home/luc/test/existing_cards.txt", "w")
        for key, value in card_dict.items():
            existing_cards_file.write(f"{key}:{value}\n")
        existing_cards_file.close()


def export_cards(closing_file=None):
    if closing_file:
        to_export_to = closing_file
    else:
        to_export_to = input("File name:\n")
        logging.debug("File name:")
        logging.debug(to_export_to)
    exported_file = open(to_export_to, "w")
    exported = 0
    for key, val in card_dict.items():
        exported_file.write(f"{key}:{val}\n")
        exported += 1

    print(f"{exported} cards have been saved.")
    logging.debug(f"{exported} cards have been saved.")
    exported_file.close()


def export_logs():
    file_name = input("File name:\n")
    logging.debug("File name")
    logging.debug(file_name)
    with open(file_name, "w") as export_file, open("/home/luc/test/logging_data.txt", "r") as read_file:
        for line in read_file:
            export_file.write(line)
    print("The log has been saved.")
    logging.debug("The log has been saved")


def hardest_card():
    add_to_stat_dict()
    hardest_card_list = [["", 0]]
    argument_parse_list = list()
    for term, stat_val in statistics_dict.items():
        if stat_val[0] != 0:
            num_wrong_answers = stat_val[0] - stat_val[1]
            if num_wrong_answers > hardest_card_list[0][1]:
                hardest_card_list = [[term, num_wrong_answers]]
                argument_parse_list = [term]
            elif num_wrong_answers == hardest_card_list[0][1]:
                hardest_card_list.append([term, num_wrong_answers])
                argument_parse_list.append(term)

    if hardest_card_list[0][1] == 0:
        print("There are no cards with errors.")
        logging.debug("There are no cards with errors.")
    elif len(hardest_card_list) == 1:
        print(f'The hardest card is "{hardest_card_list[0][0]}" You have.'
              f' {statistics_dict[hardest_card_list[0][0]][0] - statistics_dict[hardest_card_list[0][0]][1]}'
              f' errors answering it.')
        logging.debug(f'The hardest card is "{hardest_card_list[0][0]}". You have'
                      f' {statistics_dict[hardest_card_list[0][0]][0] - statistics_dict[hardest_card_list[0][0]][1]}'
                      f' errors answering it.')
    else:
        print(f'The hardest cards are {hardest_card_string(argument_parse_list)}.')
        logging.debug(f'The hardest cards are {hardest_card_string(argument_parse_list)}')


def hardest_card_string(argument_parse_list):
    r_string = ""
    mistakes = 0
    for i in argument_parse_list:
        r_string += f'"{i}"'
        if i != argument_parse_list[-1]:
            r_string += ", "
    # r_string += ". You have"
    # for i in argument_parse_list:
    #     mistakes += statistics_dict[i][0]
    # r_string += f' {mistakes} errors answering it'
    return r_string


def reset_stats():
    for key in statistics_dict.keys():
        statistics_dict[key] = [0, 0, False]
    print("Card statistics have been reset.")
    logging.info("Card statistics have been reset.")


def exit_():
    print("Bye bye!")
    logging.info("Bye bye!")
    if args.export_to:
        export_cards(args.export_to)
    quit()


def navigation(force_navigate=None):
    action = input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
    logging.debug("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    logging.debug(action)
    if action == "add" or force_navigate == "add":
        add_cards()

    elif action == "remove" or force_navigate == "remove":
        remove_cards()

    elif action == "import" or force_navigate == "import":
        import_cards()

    elif action == "export" or force_navigate == "export":
        export_cards()

    elif action == "ask" or force_navigate == "ask":
        logging.debug("How many times to ask?")
        ask_cards(int(input("How many times to ask?\n")))

    elif action == "exit" or force_navigate == "exit":
        exit_()

    elif action == "log":
        export_logs()

    elif action == "hardest card":
        hardest_card()

    elif action == "reset stats":
        reset_stats()


file = open("/home/luc/test/existing_cards.txt", "w")

parser = argparse.ArgumentParser()
parser.add_argument("--import_from", default=False)
parser.add_argument("--export_to", default=False)

args = parser.parse_args()
if args.import_from:
    import_cards(args.import_from)


while True:
    navigation()