keep_running = True

# MAIN MENU
while keep_running == True:
    print("MAIN MENU")
    print("1. Inventory Check")
    print("2. Transaction Calculator")
    print("3. Staff Available")
    print("4. Exit")
    
    choice = input("Enter 1, 2, 3, or 4: ")

    # OPTION 1: INVENTORY
    if choice == "1":
        print("INVENTORY CHECK")
        gallons_in_fridge = float(input("How many gallons of milk do you have? "))
        lattes_to_sell = int(input("How many lattes do you expect to sell? "))
        
        gallons_needed = lattes_to_sell * 0.1
        
        if gallons_in_fridge > gallons_needed:
            difference = gallons_in_fridge - gallons_needed
            print("Status: Surplus")
            print("You have", difference, "extra gallons.")
            
        elif gallons_in_fridge < gallons_needed:
            difference = gallons_needed - gallons_in_fridge
            print("Status: Shortage")
            print("You need", difference, "more gallons.")
            
        else:
            print("Status: Exact")
            print("You have exactly enough milk")

    # OPTION 2: TRANSACTIONS
    elif choice == "2":
        print("TRANSACTION CALCULATOR")
        print("A. Specialty Cold Brew ($6)")
        print("B. Standard Drip ($3)")
        drink_type = input("Pick A or B: ")
        
        # Set price
        if drink_type == "A" or drink_type == "a":
            price_per_drink = 6
        else:
            price_per_drink = 3
            
        number_of_drinks = int(input("How many drinks? "))
        
        # Drink subtotal
        drink_subtotal = number_of_drinks * price_per_drink
        
        # 15% discount 
        if number_of_drinks >= 10:
            discount = drink_subtotal * 0.15
            drink_subtotal = drink_subtotal - discount
            print("Bulk discount applied")

        # Pastry Bundle is $5 extra
        total_before_tax = drink_subtotal
        wants_pastry = input("Add a Pastry Bundle for $5? (yes/no): ")
        if wants_pastry == "yes":
            total_before_tax = total_before_tax + 5
            
        # 10% Barista Tax 
        tax = total_before_tax * 0.10
        final_bill = total_before_tax + tax
        
        print("Total amount due: $", final_bill)
        
        # Payment Logic
        user_payment = float(input("How much money did the customer give you? "))
        
        if user_payment < final_bill:
            print("Error: That is not enough money")
        elif user_payment == final_bill:
            print("Exact amount paid.")
        else:
            change = user_payment - final_bill
            print("Transaction complete, give them $", change, "in change.")

# OPTION 3: STAFF AVAILABLE (EXTRA)
    elif choice == "3":
        print("STAFFING CHECK")
        staff = int(input("How many staff members are available? "))
        drinks = int(input("How many drinks are expected to be made? "))
        
        if drinks >= 800:
            if staff < 7:
                print("You're understaffed!")
            else:
                print("You have enough staff.")
        else:
            if staff >= 4:
                print("You have enough staff.")
            else:
                print("You are very understaffed.")

    # OPTION 4: EXIT 
    elif choice == "4":
        print("Goodbye!")
        keep_running = False

    # ERROR CHECKING
    else:
        print("That is not a valid choice. Try again.")