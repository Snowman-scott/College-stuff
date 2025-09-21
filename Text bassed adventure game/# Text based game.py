# Text based game
import os
import time
import json
from datetime import datetime
import re


class Savemanager:
    def __init__(self, base_save_dir="savedata"):
        self.base_save_dir = base_save_dir
        self.ensure_base_directory()

    def ensure_base_directory(self):
        """makes sure base directory exists"""
        if not os.path.exists(self.base_save_dir):
         os.makedirs(self.base_save_dir)
        print(f"Created base save Directory: {self.base_save_dir}")

    def sanitize_filename(self, filename):
        """Reomve invalid charchters from filename"""
        sanitized = re.sub(r'[<>:/\\|?*]', '', filename)
        sanitized = sanitized.replace(' ' , '_')
        return sanitized[:50]
    
    def create_save_folder(self, save_name):
        """Creates new save folder with sanatized name"""
        sanatized_name = self.sanatize_filename(save_name)
        if not sanatized_name:
            sanatized_name = "unnamed_save"
    
        save_path = os.path.join(self.base_save_dir, sanatized_name)

        counter = 1
        original_path = save_path
        while os.path.exists(save_path):
            save_path = f"{original_path}_{counter}"
            counter += 1

        os.makedirs(save_path)
        return save_path
    
    def get_timestamp_filename(self, base_name="gamedata", extension="json"):
        """generate filename with timestamp"""
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"

    def save_game_data(self, save_name, game_data):
        """Save game data to subfolde"""
        try:
            save_folder = self.create_save_folder(save_name)
            filename = self.get_timestamp_filename()
            filepath = os.path.join(save_folder, filename)

            with open(filepath, "w") as f:
                json.dump(game_data, f , indent=4)
            
            print(f"Game saved Successfully to: {filepath}")
            return filepath
        
        except Exception as e:
            print(f"Error saving game: {e}")
            return None
        
    def list_saves(self):
        """Lists all avalible save folders"""
        saves = []
        if os.path.exists(self.base_save_dir):
            for item in os.listdir(self.base_save_dir):
                item_path = os.path.join(self.base_save_dir, item)
                if os.path.isdir(item_path):
                    saves.append(item)
        return sorted(saves)
    
    def list_save_files(self, save_folder_name):
        """Lists all saves in specific save folder"""
        save_path = os.path.join(self.base_save_dir, save_folder_name)
        if not os.path.exists(save_path):
            return []
        
        files = []
        for file in os.lastdir(save_path):
            if file.endswith('.json'):
                filepath = os.path.join(self.base_save_dir, save_folder_name)
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                files.append({
                    'filename': file,
                    'filepath': filepath,
                    'modified': mod_time.strftime("%d-%m-%Y %H:%M:%S")
                })
                
        return sorted(files, key=lambda x: x['modified'], reverse=True)
    
    def laod_game_data(self, save_folder_name, filename=None):
        """Load game data from a save folder"""
        try:
            save_files = self.list_save_files(save_folder_name)
            
            if not save_files:
                print(f"No save files found in {save_folder_name}")
                return None
            
            if filename is None:
                target_file = save_files[0]['filepath']
                print(f"Loading newest save: {save_files[0]['filename']}")
            else:
                target_file = os.path.join(self.base_save_dir, save_folder_name, filename)
                if not os.path.exists(target_file):
                    print(f"File not found: {filename}")
                    return None
            
            with open(target_file, 'r') as f:
                data = json.load(f)
            
            print(f"Game loaded Successfully!")
            return data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
        
    
class TextadventureGame:
    def __init__(self):
        self.Savemanager = Savemanager
        self.House = { #The "map": 
            "The Cold As Conservatory" : {"B" : "Cooking room" , "C" : "Room For Living", "D" : "An Bathroom", "E" : "Stairs!", "Item" : "Batteries and Fuel"},
            "Cooking room" : {"Item" : "Knife"},
            "Room For Living" : {"Item" : "Broken Laptop"},
            "An Bathroom" : {"Item" : "Medical supplies"},
            "stairs!" : {}
        }
        
        # Game state variables that will be saved
        self.cl = "The Cold As Conservatory" # current location of the player
        self.inventory = ["Gun"]

        #Add more variables here if want. These will be automatically saved

    def get_game_state(self):
        """Gets all game state veriables"""
        return {
            'current_location': self.cl,
            'inventory': self.inventory,

        }

    def set_game_state(self, game_state):
        """Loafds game state from save data"""
        self.cl = game_state.get('current_location', "the Cold As Conservatory")
        self.inventory = game_state.get('inventory', ["Gun"])

        print(f"Game state loaded - Location: {self.cl} \nInvo: {len(self.inventory)}")

    def save_game(self):
        """Save current variables in game"""
        print("\n--- SAVE GAME ---")
        save_name = input("Enter a name for your save: ")
        
        if not save_name:
            save_name = f"save_{datetime.now().strftime('%d%m%Y_%H%M%S')}"
            print(f"Using default name: {save_name}")
            
        game_state = self.get_game_state()
        filepath = self.save_manager.save_game_data(save_name, game_state)
        
        if filepath:
            print("Game saved successfully :3")
            time.sleep(2)
        else:
            print("Failed to save game -_-")
            time.sleep(2)
            
    def load_game(self):
        """laod a save game state"""
        print("\n--- LOAD GAME ---")
        saves = self.save_manager.list_saves()
        
        if not saves:
            print("No saves found")
            time.sleep(2)
            return
        
        print("Avalible saves:")
        for i, save in enumerate(saves, 1):
            print(f"{i}. {save}")
            
        try:
            choice = input("Select save to laod (number): ").strip()
            if choice.isdigit():
                choice = int(choice) - 1
                if 0 <= choice < len(saves):
                    selected_save = saves[choice]
                    
                    #Show avalible files in the save folder
                    save_files = self.save_manager.list_save_files(selected_save)
                    if save_files:
                        print(f"\nSave files in '{selected_save}':")
                        for i, file_info in enumerate(save_files, 1):
                            print(f"{i}. {file_info['filename']} (Modified: {file_info['modified']})")
                    
                        file_choice = input("Select file to load (number, or press Enter for newest): ").strip()
                    
                        filename = None
                        if file_choice.isdigit():
                            file_idx = int(file_choice) - 1
                            if 0 <= file_idx < len(save_files):
                                filename = save_files[file_idx]['filename']
                            
                        laoded_data = self.save_manager.load_game_data(selected_save, filename)
                        if laoded_data:
                            self.set_game_state(laoded_data)
                            print("game laoded successfully :3")
                        else:
                            print("Failed to laod game -_-")
                    else:
                        print("No save files found in the folder")
                else:
                    print("Invalid Selection")
            else:
                print("Invalif input")
        except Exception as e:
            print(f"Error: {e}")
            
            
        time.sleep(2)
    
    def run_game(self):
        """Code below to be edited and put into her with save/laod functionalioty added"""
        os.system("cls")
        
        while True:

            print("Current (See current location)")
            print("Move (Move to a different location)")
            print("Invo (view your current items in inventory)")
            print("Pickup (Pick up a new item)")
            print("Save (Save your game)")
            print("Load (Load a Save game)")
            print("Quit (Exit THe game)")
            
            move = input("\n\n\nWhat do you want to do?").lower()
            print("\n")
            
            if move == "current":
                os.system("cls")
                print(f"You are in {self.cl}\n")

            elif move == "move":
                os.system("cls")
                print("The Cold As Conservatory = A")
                print("Cooking room = B")
                print("Room For Living = C")
                print("An Bathroom = D")
                print("Stairs! = E ")
                print("\nYour current location is: " , self.cl)
                pm = input("\nWhere would you like to move to?").upper()
                
                if self.cl == pm:
                    print("invalid move \nYou cannot move to the samce location you are currently at\n")
                elif pm in self.House[self.cl]:
                    print("you have moved to" , pm)
                    time.sleep(1)
                    cl = self.House[self.cl][pm]
                else:
                    print("Invalid input")
    
            elif move == "pickup":
                if "Item" in self.House[self.cl]:
                    self.inventory

            elif move == "invo":
                print("Inventory :\n")
                for Item in self.inventory:
                    print(Item ,"\n")
                print("")
                time.sleep(2)
                
            elif move == "save":
                self.save_game()
                
            elif move == "load":
                self.laod_game()
                
            elif move == "quit":
                print("Thanks for playing")
                break
            
            else:
                print("Invalid commmand. \nPlease Try Again")
                time.sleep(1)
                
#Run the game
if __name__ == "__main__":
    game = TextadventureGame()
    game.run_game()