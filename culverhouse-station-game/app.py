import energy
import asteroid_mining
import alien_duel
 
 
def print_welcome():
    print("")
    print("Welcome to Culverhouse Station X!")
    print("A remote space station orbiting the distant planet Baileylandia.")
    print("")
    print("Your ship CRASH LANDED!")
    print("You were able to save 50 energy crystals.")
    print("You need to reach 300 energy crystals to jumpstart your evacuation ship.")
    print("If you lose all your crystals... THE ALIENS EAT YOU FOR BREAKFAST!")
    print("")
 
 
def print_menu():
    print("")
    print("--- Station Menu ---")
    print("1. Asteroid Mining")
    print("2. Alien Duel")
    print("3. Quit")
    print("--------------------")
 
 
def print_session_summary(game_name, session_crystals, total_crystals):
    print("")
    print("--- Session Summary ---")
    print("Game played: " + game_name)
    if session_crystals >= 0:
        print("Crystals earned this session: " + str(session_crystals))
    else:
        print("Crystals lost this session: " + str(session_crystals))
    print("Total crystals in your pocket: " + str(total_crystals))
    print("-----------------------")
    print("")
 
 
def main():
    print_welcome()
 
    em = energy.EnergyManager()
 
    while True:
        em.display()
        print_menu()
 
        choice = input("Choose an option (1, 2, or 3): ").strip()
 
        if choice == "1":
            session = asteroid_mining.play(em)
            print_session_summary("Asteroid Mining", session, em.get_crystals())
 
        elif choice == "2":
            session = alien_duel.play(em)
            print_session_summary("Alien Duel", session, em.get_crystals())
 
        elif choice == "3":
            print("Goodbye, space traveler!")
            break
 
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue
 
        if em.has_won():
            print("CONGRATULATIONS! You escaped Baileylandia! Mission complete!")
            break
 
        if em.is_dead():
            print("GAME OVER - THE ALIENS EAT YOU FOR BREAKFAST!")
            break
 
 
if __name__ == "__main__":
    main()