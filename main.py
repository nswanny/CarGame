# A game where you select between a list of certain cars, all with varying durability depending on the color of car and a base amount of money ($10000)
# The better the car, the higher the cost of the car.
# The user types the color of car to select it.
# Once the car is selected they take this car down a road. They decide every "mile" if they wish to continue or if they wish to repair.
# It costs money to repair the car ($500)
# Every mile there is a chance of a 'collision' where the car takes more durability. This does not happen every time.
# The game ends when they either hit 20miles or run out of durability in the car. 

import random
import time

class Car:

    def __init__(self, color, cost, max_durability):
        self.color = color
        self.cost = cost
        self.max_durability = max_durability
        self.current_durability = max_durability

    def damage(self, amount):
        self.current_durability -= amount

    def repair(self, amount):
        self.current_durability = min(self.max_durability, self.current_durability + amount)

    def is_driveable(self):
        return self.current_durability > 0


# Keep the player and the car seperate  
class Player:
    def __init__(self, starting_money):
        self.money = starting_money
        self.car = None

    def can_afford(self,amount):
        return self.money >= amount
    
    def pay(self, amount):
        self.money -= amount
    
    def assign_car(self, car):
        self.car = car

# Game mechanics

class CarGame:
    def __init__(self):
        
        # Rules of the game
        self.player = Player(10000)
        self.target_miles = 20
        self.repair_cost = 500
        self.repair_amount = 40
        self.base_wear = 5
        self.collision_chance = 0.30

        # Car options
        self.car_options = {"rusty": Car("rusty", 1000, 50), "green": Car("green", 3000, 70), "blue": Car("blue", 5000, 90), "red": Car("red", 8000, 120)}


    def start(self):
        print("Welcome to The CarGame")
        print(f"You have ${self.player.money} to buy a car and survive a {self.target_miles} miles.")
        print("")
        
        
        self.select_car()
        self.journey_loop()
        self.end_game()

    def select_car(self):
        print("Cars available for purchase: ")
        for color, car in self.car_options.items():
            print(f"{color.capitalize()}: Cost ${car.cost}, Durability: {car.max_durability}")
        
        while True:
            choice = input("\nType the color of car that you want to select: ").strip().lower()

            if choice not in self.car_options:
                print("Invalid color. Please select a color from the list!")
                continue

            select_car = self.car_options[choice]

            # to show the purchase
            self.player.pay(select_car.cost)
            self.player.assign_car(select_car)
            print(f"\n You bought the {select_car.color.capitalize()} car.")
            print(f"Remaining balance: ${self.player.money}")
            time.sleep(1)
            break

    def journey_loop(self):
        miles_traveled = 0

        while miles_traveled < self.target_miles and self.player.car.is_driveable():
            print("")
            print(f"Mile {miles_traveled + 1}")
            print(f"Durability: {self.player.car.current_durability}/{self.player.car.max_durability} | Money: ${self.player.money}")

            self.handle_player_action()

            print("Driving...")
            time.sleep(1)
            miles_traveled += 1

            self.apply_road_events()

        self.final_miles = miles_traveled # to be used at the end of the game

    def handle_player_action(self):
        action = ""
        while action not in ['c', 'r']:
            action = input("Type 'c' to continue driving or 'r' to repair ($500): ").strip().lower()

        if action == 'r':
            if self.player.can_afford(self.repair_cost):
                self.player.pay(self.repair_cost)
                self.player.car.repair(self.repair_amount)
                print(f"You repaired your car! Durability is now {self.player.car.current_durability}. Money left: ${self.player.money}")
            else:
                print("You don't have enough money to repair! You are forced to continue.")

    def apply_road_events(self):
        # Normal wear and tear
        self.player.car.damage(self.base_wear)

        # Random collision logic
        if random.random() < self.collision_chance:
            collision_damage = random.randint(15, 30)
            self.player.car.damage(collision_damage)
            print(f"CRASH! You hit a major pothole. You lost {collision_damage} extra durability!")
        else:
            print("The road was clear. Normal wear and tear applied.")

    def end_game(self):
        print("")
        if not self.player.car.is_driveable():
            print(f"GAME OVER. Your {self.player.car.color} car broke down at mile {self.final_miles}.")
        else:
            print(f"YOU WIN! You successfully drove {self.target_miles} miles in your {self.player.car.color} car!")
            print(f"Remaining money: ${self.player.money}")
            print(f"Remaining durability: {self.player.car.current_durability}/{self.player.car.max_durability}")
        print("")


if __name__ == "__main__":
    game = CarGame()
    game.start()    
    
    
