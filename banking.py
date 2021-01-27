import random
import sqlite3
#conn = sqlite3.connect('card.s3db')
#c = conn.cursor()
#
conn = sqlite3.connect('card.s3db')
c = conn.cursor()
#c.execute("CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
c.execute("SELECT * FROM card")
items = c.fetchall()

conn.commit()
accounts = []  # List of the accounts
for item in items:
    accounts.append(item)

class Account:
    def __init__(self, account_id, card_number=None, pin=0000, balance=0):
        self.account_id = account_id
        self.card_number = card_number
        self.pin = pin
        self.balance = balance

    def __str__(self):
        return '[account_id: {}, card_number: {}, pin: {}, balance: {}]' \
            .format(self.account_id, self.card_number, self.pin, self.balance)


def card_number_creator():
    while True:
        last_digits = str(random.randint(1000000000, 9999999999))
        number_check = list('400000' + last_digits)

        number_check_copy = [0 for i in range(0, len(number_check))]

        for integer in range(len(number_check)):
            number_check_copy[integer] = int(number_check[integer])

        for num in range(0, 16, 2):
            number_check_copy[num] *= 2

        for nums in range(1, 15):
            if number_check_copy[nums] > 9:
                number_check_copy[nums] -= 9

        if (sum(number_check_copy[:15]) + int(number_check[15])) % 10 == 0:
            break
        else:
            continue

    return int('400000' + last_digits)


def card_number_check():
    card_number = list(str(card_number_input))
    card_number_copy = [0 for i in range(0, len(card_number))]
    for integer in range(len(card_number_copy)):
        card_number_copy[integer] = int(card_number[integer])

    for num in range(0, 16, 2):
        card_number_copy[num] *= 2

    for nums in range(1, 15):
        if card_number_copy[nums] > 9:
            card_number_copy[nums] -= 9

    if (sum(card_number_copy[:15]) + int(card_number[15])) % 10 == 0:
        return True
    else:
        return False


def pin_creator():
    return random.randint(1000, 9999)


def id_creator():
    while True:
        account_id = random.randint(1000000000, 9999999999)
        if account_id not in accounts:
            break
        else:
            continue
    return account_id


while True:


    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    selection = int(input())
    print()

    if selection == 1:
        account = Account(id_creator(), card_number_creator(), pin_creator())
        accounts.append((account.account_id, str(account.card_number), str(account.pin), account.balance))
        c.execute(f"""INSERT INTO card
                     VALUES('{account.account_id}', '{account.card_number}', '{account.pin}', '{account.balance}')
                """)
        conn.commit()
        print('Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}'.format(account.card_number,
                                                                                             account.pin))
        print()
        continue

    elif selection == 2:
        print('Enter your card number:')
        card_number_input = input()  # '4000005696033357'
        correct_pin = None
        account_num = None
        for number in range(len(accounts)):
            if card_number_input == accounts[number][1]:
                correct_pin = accounts[number][2]
                account_num = number
        print('Enter your PIN:')
        pin_input = input()  # '7588'
        current_account = []

        if pin_input == correct_pin and card_number_check() is True:
            print('You have successfully logged in!')
            for item in accounts[account_num]:
                current_account.append(item)

            # current_account = accounts[account_num]

        else:
            print()
            print('Wrong card number or PIN!')
            continue

        while True:
            print("\n1 - Balance \n2 - Add income \n3 - Do transfer \n4 - Close account \n5 - Log out \n0 - Exit ")
            selection1 = int(input('>'))
            print()

            if selection1 == 1:
                print('Balance: {}'.format(current_account[3]))


            elif selection1 == 2:
                income = int(input('Enter income:'))
                current_account[3] += income
                print('Income was added!')
                c.execute(f"""UPDATE card
                     SET balance = '{current_account[3]}' 
                     WHERE id = '{current_account[0]}'
                """)
                conn.commit()
                print()
                continue

            elif selection1 == 3:
                print('Transfer')
                print('Enter card number:')
                card_number_input = input()  # '4000002801423805'
                while True:
                    if card_number_check() is False:
                        print('Probably you made a mistake in the card number. Please try again!')
                        break

                    existing_cards = [accounts[x][1] for x in range(len(accounts))]

                    if card_number_input not in existing_cards:
                        print('Such a card does not exist.')
                        break

                    if current_account[1] == card_number_input:
                        print("You can't transfer money to the same account")
                        break

                    print('Enter how much money you want to transfer:')
                    transfer_amount = int(input())

                    if current_account[3] - transfer_amount < 0:
                        print('Not enough money!')
                        break

                    current_account[3] -= transfer_amount
                    c.execute(f"""UPDATE card
                                 SET balance = balance + '{transfer_amount}'
                                 WHERE number = {card_number_input}
                                            """)
                    c.execute(f"""UPDATE card
                     SET balance = '{current_account[3]}' 
                     WHERE id = '{current_account[0]}'
                                """)
                    conn.commit()
                    print('Success')
                    break

                continue

            elif selection1 == 4:
                c.execute(f"""DELETE FROM card WHERE number = '{current_account[1]}'
                """)
                conn.commit()

            elif selection1 == 5:
                print('You have successfully logged out!')
                print()
                c.execute(f"""UPDATE card
                     SET balance = '{current_account[3]}' 
                     WHERE id = '{current_account[0]}'
                """)
                conn.commit()
                # accounts[account_num][3]
                break

            elif selection1 == 0:
                print("Bye!")
                conn.close()
                exit()

    elif selection == 0:
        print('Bye!')
        break
conn.close()
