import json
import os
from typing import Dict, List

class HerbInventory:
    def __init__(self):
        self.filename = 'herbs_data.json'
        self.herbs = self.load_data()

    def load_data(self) -> List[Dict]:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.herbs, file, indent=4)

    def add_herb(self):
        while True:
            print("\n=== Add New Herb ===")
            print("Enter 0 to return to main menu")
            name = input("Enter herb name (or 'back' to return): ").strip()
            if name == '0':
                return 'main'
            if name.lower() == 'back':
                return

            while True:
                print("Enter 0 to return to main menu")
                price = input("Enter price (or 'back' to return): ").strip()
                if price == '0':
                    return 'main'
                if price.lower() == 'back':
                    break  # Go back to name input
                try:
                    price = float(price)
                    if price < 0:
                        print("Price cannot be negative! Please enter a valid number.")
                        continue
                    break  # Valid price, continue with location
                except ValueError:
                    print("Invalid price! Please enter a number.")
                    continue
                
            if price == 'back':
                continue  # Go back to name input

            print("Enter 0 to return to main menu")
            location = input("Enter city (or 'back' to return): ").strip()
            if location == '0':
                return 'main'
            if location.lower() == 'back':
                continue  # Go back to price input

            print("\nConfirm details:")
            print(f"Name: {name}")
            print(f"Price: ${price:.2f}")
            print(f"Location: {location}")
            
            print("Enter 0 to return to main menu")
            confirm = input("\nSave this herb? (yes/no/back): ").lower()
            if confirm == '0':
                return 'main'
            if confirm == 'back':
                continue
            if confirm == 'yes':
                self.herbs.append({
                    'name': name,
                    'price': price,
                    'location': location
                })
                print("Herb added successfully!")
                break

    def view_herbs(self):
        if not self.herbs:
            print("\nNo herbs in inventory!")
            return

        print("\n=== Current Inventory ===")
        print("ID  | Name                 | Price    | Location")
        print("-" * 50)
        for idx, herb in enumerate(self.herbs, 1):
            print(f"{idx:3} | {herb['name']:<20} | ${herb['price']:<7.2f} | {herb['location']}")
        input("\nPress Enter to continue...")

    def delete_herb(self):
        while True:
            self.view_herbs()
            if not self.herbs:
                return

            print("Enter 0 to return to main menu")
            choice = input("\nEnter ID to delete (or 'back' to return): ").strip()
            if choice == '0':
                return 'main'
            if choice.lower() == 'back':
                return

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.herbs):
                    herb = self.herbs[idx]
                    print("Enter 0 to return to main menu")
                    confirm = input(f"Confirm deletion of {herb['name']}? (yes/no/back): ").lower()
                    if confirm == '0':
                        return 'main'
                    if confirm == 'back':
                        continue
                    if confirm == 'yes':
                        self.herbs.pop(idx)
                        print("Herb deleted successfully!")
                        break
                else:
                    print("Invalid ID!")
            except ValueError:
                print("Please enter a valid number!")

    def edit_herb(self):
        while True:
            self.view_herbs()
            if not self.herbs:
                return

            print("Enter 0 to return to main menu")
            choice = input("\nEnter ID to edit (or 'back' to return): ").strip()
            if choice == '0':
                return 'main'
            if choice.lower() == 'back':
                return

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.herbs):
                    while True:  # Add loop for edit menu
                        herb = self.herbs[idx]
                        print("\nWhat would you like to edit?")
                        print("0. Return to main menu")
                        print("1. Name")
                        print("2. Price")
                        print("3. Location")
                        print("4. Back to herb selection")
                        edit_choice = input("Enter your choice: ").strip()

                        if edit_choice == '0':
                            return 'main'
                        if edit_choice == '4':
                            break  # Go back to herb selection

                        if edit_choice == '1':
                            print("Enter 0 to return to main menu")
                            new_name = input(f"Current name: {herb['name']}\nNew name (or 'back' to return): ").strip()
                            if new_name == '0':
                                return 'main'
                            if new_name.lower() == 'back':
                                continue
                            herb['name'] = new_name
                        elif edit_choice == '2':
                            while True:
                                print("Enter 0 to return to main menu")
                                new_price = input(f"Current price: ${herb['price']}\nNew price (or 'back' to return): ").strip()
                                if new_price == '0':
                                    return 'main'
                                if new_price.lower() == 'back':
                                    break
                                try:
                                    price = float(new_price)
                                    if price < 0:
                                        print("Price cannot be negative! Please enter a valid number.")
                                        continue
                                    herb['price'] = price
                                    break
                                except ValueError:
                                    print("Invalid price! Please enter a number.")
                        elif edit_choice == '3':
                            print("Enter 0 to return to main menu")
                            new_location = input(f"Current location: {herb['location']}\nNew location (or 'back' to return): ").strip()
                            if new_location == '0':
                                return 'main'
                            if new_location.lower() == 'back':
                                continue
                            herb['location'] = new_location
                        else:
                            print("Invalid choice!")
                            continue

                        print("Update successful!")
                else:
                    print("Invalid ID!")
            except ValueError:
                print("Please enter a valid number!")

def main():
    inventory = HerbInventory()
    
    while True:
        print("\n=== Herb Inventory System ===")
        print("1. Add Herb")
        print("2. View Inventory")
        print("3. Edit Herb")
        print("4. Delete Herb")
        print("5. Save and Quit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            result = inventory.add_herb()
        elif choice == '2':
            inventory.view_herbs()
        elif choice == '3':
            result = inventory.edit_herb()
        elif choice == '4':
            result = inventory.delete_herb()
        elif choice == '5':
            inventory.save_data()
            print("Data saved successfully! Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
            
        # Check if we need to continue the main loop
        if result == 'main':
            continue

if __name__ == "__main__":
    main()