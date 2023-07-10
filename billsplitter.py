import random


def update_dict(to_update, update_value):
    for element in to_update:
        to_update[element] = update_value


def calc_split_bill(n_attendees, bill_value):
    split_bill = round(bill_value / n_attendees, 2)
    if split_bill % 1 == 0:
        return int(split_bill)
    return split_bill


number_of_attendees = int(input("Enter the number of friends joining (including you): \n"))
print()

if number_of_attendees < 1:
    print("No one is joining for the party")
else:
    attendees_names = dict()
    print("Enter the name of every friend (including you), each on a new line")
    for i in range(number_of_attendees):
        attendees_names[input()] = 0
    print()

    final_bill = int(input("Enter the total bill value: \n"))
    print()

    lucky_feature_question = input('Do you want to use the "Who is lucky?" feature? Write Yes/No \n')
    print()

    if lucky_feature_question == "Yes":
        lucky_person = random.choice(list(attendees_names.keys()))
        print(f"{lucky_person} is the lucky one!\n")
        update_dict(attendees_names, calc_split_bill(number_of_attendees -1, final_bill))
        attendees_names[lucky_person] = 0
    else:
        update_dict(attendees_names, calc_split_bill(number_of_attendees, final_bill))
        print("No one is going to be lucky")

    print(attendees_names)