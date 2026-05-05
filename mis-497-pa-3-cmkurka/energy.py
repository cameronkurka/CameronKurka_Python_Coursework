STARTING_CRYSTALS = 50
WIN_GOAL = 300
 
 
class EnergyManager:
    def __init__(self):
        self.crystals = STARTING_CRYSTALS
        self.session_earned = 0
 
    def get_crystals(self):
        return self.crystals
 
    def add(self, amount):
        self.crystals += amount
        self.session_earned += amount
 
    def subtract(self, amount):
        self.crystals -= amount
        self.session_earned -= amount
 
    def lose_all(self):
        lost = self.crystals
        self.session_earned -= lost
        self.crystals = 0
 
    def reset_session(self):
        self.session_earned = 0
 
    def has_won(self):
        return self.crystals >= WIN_GOAL
 
    def is_dead(self):
        return self.crystals <= 0
 
    def display(self):
        print("You currently have " + str(self.crystals) + " energy crystals.")