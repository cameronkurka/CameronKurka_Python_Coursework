import random


def display_rules():
    print("")
    print("--- Alien Duel Rules ---")
    print("Bet between 1 and however many crystals you currently have.")
    print("You and the alien both roll 10-sided dice (values 0 through 9).")
    print("Rolling a 0 counts as 10 points.")
    print("Rolling a 1 can count as either 1 or 11. You choose!")
    print("You roll 2 dice first, then can keep rolling one at a time.")
    print("If your total goes over 21, you bust and lose your bet.")
    print("The alien rolls after you and must keep rolling until it reaches 17 or more.")
    print("The alien also uses 1 as 1 or 11, whichever keeps it under 22.")
    print("If the alien busts, you win!")
    print("Ties go to the alien, UNLESS you hit exactly 21 (called a Plasma Blast).")
    print("If you win, your bet is doubled.")
    print("------------------------")
    print("")


def roll_die():
    # Rolls a 10-sided die 
    return random.randint(0, 9)


def get_die_value(raw_roll):
    # A 0 is worth 10
    if raw_roll == 0:
        return 10
    return raw_roll


def ask_player_for_one_value(total):
    # 1 or 11
    print("You rolled a 1! It can count as 1 or 11.")
    print("Your total before this roll is: " + str(total))
    while True:
        choice = input("Do you want the 1 to count as 1 or 11? Enter 1 or 11: ").strip()
        if choice == "1":
            return 1
        elif choice == "11":
            if total + 11 > 21:
                print("Choosing 11 would bust you. You must pick 1.")
                return 1
            return 11
        else:
            print("Please enter either 1 or 11.")


def alien_choose_one_value(total):
    # The alien picks whichever value of 1 keeps it under 22
    if total + 11 <= 21:
        print("The alien's 1 counts as 11.")
        return 11
    else:
        print("The alien's 1 counts as 1.")
        return 1


def display_hand(label, dice_list, total):
    # Shows all the dice in someone's hand and their current total
    dice_string = ""
    for i in range(len(dice_list)):
        if i == 0:
            dice_string = str(dice_list[i])
        else:
            dice_string = dice_string + ", " + str(dice_list[i])
    print(label + " hand: [" + dice_string + "]  Total: " + str(total))


def get_bet(max_crystals):
    # Crystals available to bet
    while True:
        try:
            bet = int(input("Enter your bet (1 to " + str(max_crystals) + "): ").strip())
            if bet >= 1 and bet <= max_crystals:
                return bet
            else:
                print("Your bet must be between 1 and " + str(max_crystals) + ". Try again.")
        except ValueError:
            print("Please enter a whole number.")


def player_turn():
    total = 0
    dice_list = []

    print("")
    print("Your turn. Rolling 2 dice...")

    # First die
    raw1 = roll_die()
    if raw1 == 1:
        value1 = ask_player_for_one_value(total)
    else:
        value1 = get_die_value(raw1)
        print("You rolled: " + str(value1))
    total = total + value1
    dice_list.append(value1)
    display_hand("Your", dice_list, total)

    # Second die
    raw2 = roll_die()
    if raw2 == 1:
        value2 = ask_player_for_one_value(total)
    else:
        value2 = get_die_value(raw2)
        print("You rolled: " + str(value2))
    total = total + value2
    dice_list.append(value2)
    display_hand("Your", dice_list, total)

    if total > 21:
        print("You went over 21. You busted!")
        return -1

    # Extra rolls one at a time
    while True:
        answer = input("Roll another die? (yes/no): ").strip().lower()
        if answer != "yes" and answer != "y":
            break

        raw = roll_die()
        if raw == 1:
            new_value = ask_player_for_one_value(total)
        else:
            new_value = get_die_value(raw)
            print("You rolled: " + str(new_value))
        total = total + new_value
        dice_list.append(new_value)
        display_hand("Your", dice_list, total)

        if total > 21:
            print("You went over 21. You busted!")
            return -1

    return total


def alien_turn():
    total = 0
    dice_list = []

    print("")
    print("Alien's turn. Rolling 2 dice...")

    # First die
    raw1 = roll_die()
    if raw1 == 1:
        value1 = alien_choose_one_value(total)
    else:
        value1 = get_die_value(raw1)
        print("Alien rolled: " + str(value1))
    total = total + value1
    dice_list.append(value1)
    display_hand("Alien's", dice_list, total)

    # Second die
    raw2 = roll_die()
    if raw2 == 1:
        value2 = alien_choose_one_value(total)
    else:
        value2 = get_die_value(raw2)
        print("Alien rolled: " + str(value2))
    total = total + value2
    dice_list.append(value2)
    display_hand("Alien's", dice_list, total)

    # Alien keeps rolling until it reaches 17 or more
    while total < 17:
        print("Alien must keep rolling...")
        raw = roll_die()
        if raw == 1:
            new_value = alien_choose_one_value(total)
        else:
            new_value = get_die_value(raw)
            print("Alien rolled: " + str(new_value))
        total = total + new_value
        dice_list.append(new_value)
        display_hand("Alien's", dice_list, total)

    if total > 21:
        print("The alien busted!")
        return -1

    return total


def resolve_round(player_total, alien_total, bet, energy_manager):
    print("")
    print("Final scores -- You: " + str(player_total) + "  |  Alien: " + ("Bust" if alien_total == -1 else str(alien_total)))

    # Alien busted
    if alien_total == -1:
        energy_manager.add(bet)
        print("The alien busted! You win " + str(bet) + " crystals!")
        return

    # Plasma Blast tie 
    if player_total == 21 and alien_total == 21:
        energy_manager.add(bet)
        print("PLASMA BLAST! You both hit 21, but your Plasma Blast wins the tie!")
        print("You win " + str(bet) + " crystals!")
        return

    # Player wins
    if player_total > alien_total:
        energy_manager.add(bet)
        print("You win! " + str(player_total) + " beats " + str(alien_total) + ". You earned " + str(bet) + " crystals!")
        return

    # Alien wins
    if alien_total > player_total:
        energy_manager.subtract(bet)
        print("The alien wins. " + str(alien_total) + " beats " + str(player_total) + ". You lost " + str(bet) + " crystals.")
        return

    # Tie goes to alien
    energy_manager.subtract(bet)
    print("It's a tie at " + str(player_total) + ". The alien wins ties. You lost " + str(bet) + " crystals.")


def play(energy_manager):
    energy_manager.reset_session()
    display_rules()

    while True:
        energy_manager.display()

        if energy_manager.get_crystals() == 0:
            print("You have no crystals to bet. THE ALIENS EAT YOU FOR BREAKFAST!")
            return energy_manager.session_earned

        bet = get_bet(energy_manager.get_crystals())

        player_total = player_turn()

        # If player busted, alien does not need to play
        if player_total == -1:
            energy_manager.subtract(bet)
            print("You busted. You lost " + str(bet) + " crystals.")
        else:
            alien_total = alien_turn()
            resolve_round(player_total, alien_total, bet, energy_manager)

        print("You now have " + str(energy_manager.get_crystals()) + " energy crystals.")

        if energy_manager.is_dead():
            print("")
            print("You have no energy crystals left. THE ALIENS EAT YOU FOR BREAKFAST!")
            return energy_manager.session_earned

        if energy_manager.has_won():
            print("")
            print("You reached 300 energy crystals! Your evacuation ship is ready!")
            return energy_manager.session_earned

        again = input("Play another round of Alien Duel? (yes/no): ").strip().lower()
        if again != "yes" and again != "y":
            break

    return energy_manager.session_earned