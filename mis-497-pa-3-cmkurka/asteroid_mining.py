import random


def display_rules():
    print("")
    print("--- Asteroid Mining Rules ---")
    print("You will be shown 5 possible mining outcomes.")
    print("When you choose to mine, the system randomly picks one outcome for you.")
    print("The 5 possible outcomes are:")
    print("  1. Earn 50 energy crystals")
    print("  2. Randomly gain OR lose 100 energy crystals")
    print("  3. Lose 25 energy crystals")
    print("  4. Lose ALL energy crystals")
    print("  5. Nothing happens")
    print("-----------------------------")
    print("")


def display_options():
    print("")
    print("The 5 possible mining sites are:")
    print("  1. Rich Vein        - Earn 50 energy crystals")
    print("  2. Unstable Core    - Randomly gain or lose 100 energy crystals")
    print("  3. Sparse Deposit   - Lose 25 energy crystals")
    print("  4. Cave-In          - Lose ALL energy crystals")
    print("  5. Empty Rock       - Nothing happens")
    print("")


def apply_outcome(energy_manager):
    # Pick a random number from 1 to 5 to decide the outcome
    outcome = random.randint(1, 5)

    if outcome == 1:
        print("The system selected: Rich Vein")
        print("You earned 50 energy crystals!")
        energy_manager.add(50)

    elif outcome == 2:
        print("The system selected: Unstable Core")
        gain = random.choice([True, False])
        if gain:
            print("Lucky! You gained 100 energy crystals!")
            energy_manager.add(100)
        else:
            if energy_manager.get_crystals() >= 100:
                print("Unlucky! You lost 100 energy crystals!")
                energy_manager.subtract(100)
            else:
                lost = energy_manager.get_crystals()
                print("Unlucky! You lost all " + str(lost) + " energy crystals!")
                energy_manager.lose_all()

    elif outcome == 3:
        print("The system selected: Sparse Deposit")
        if energy_manager.get_crystals() >= 25:
            print("Only dust here. You lost 25 energy crystals.")
            energy_manager.subtract(25)
        else:
            lost = energy_manager.get_crystals()
            print("Only dust here. You lost your remaining " + str(lost) + " crystals.")
            energy_manager.lose_all()

    elif outcome == 4:
        print("The system selected: Cave-In!")
        lost = energy_manager.get_crystals()
        print("The asteroid collapsed! You lost all " + str(lost) + " energy crystals!")
        energy_manager.lose_all()

    elif outcome == 5:
        print("The system selected: Empty Rock")
        print("Nothing to be found here. Moving on.")


def play(energy_manager):
    energy_manager.reset_session()
    display_rules()

    while True:
        energy_manager.display()
        display_options()

        answer = input("Ready to start mining? (yes/no): ").strip().lower()

        if answer != "yes" and answer != "y":
            print("Mining aborted. Returning to menu.")
            break

        apply_outcome(energy_manager)

        print("You now have " + str(energy_manager.get_crystals()) + " energy crystals.")

        if energy_manager.is_dead():
            print("")
            print("You have no energy crystals left. THE ALIENS EAT YOU FOR BREAKFAST!")
            return energy_manager.session_earned

        if energy_manager.has_won():
            print("")
            print("You reached 300 energy crystals! Your evacuation ship is ready!")
            return energy_manager.session_earned

        again = input("Continue mining? (yes/no): ").strip().lower()
        if again != "yes" and again != "y":
            break

    return energy_manager.session_earned