#!/usr/bin/env python3
"""
Tower of Chance - A colorful, modular game of luck and skill
"""
import random
import time
import os
import json
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# ASCII Art for the game
ASCII_ART = {
    "tower": """
    ╔════════════════════════════════════════════╗
    ║                  /\\                        ║
    ║                 /  \\                       ║
    ║                /    \\                      ║
    ║               /      \\                     ║
    ║              /        \\                    ║
    ║             /          \\                   ║
    ║            /            \\                  ║
    ║           /              \\                 ║
    ║          /                \\                ║
    ║         /                  \\               ║
    ║        /____________________\\              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |                    |              ║
    ║        |____________________|              ║
    ╚════════════════════════════════════════════╝
    """,
    "boss": '''
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║              BOSS CHALLENGE                ║
    ║                                            ║
    ║               .-"""""-.                    ║
    ║              /         \\                   ║
    ║             |  O   O   |                   ║
    ║             |    ∆     |                   ║
    ║              \\ \'---\'  /                    ║
    ║               \'-___-\'                      ║
    ║                  |                         ║
    ║              .-"""""-.                     ║
    ║             /  \\ | /  \\                    ║
    ║             |   \\|/   |                    ║
    ║              \\  /|\\  /                     ║
    ║               `-""""-`                     ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
    ''',
    "hidden": """
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║            HIDDEN FLOOR FOUND              ║
    ║                                            ║
    ║               .---------.                  ║
    ║              /           \\                 ║
    ║             /             \\                ║
    ║            |  .---------. |                ║
    ║            | |  .-----.  | |               ║
    ║            | | |       | | |               ║
    ║            | | |  ✧✧✧  | | |               ║
    ║            | | |       | | |               ║
    ║            | |  '-----'  | |               ║
    ║            |  '---------' |                ║
    ║            |   _________  |                ║
    ║            |  |         | |                ║
    ║            '--'         '--'               ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
    """,
    "achievement": """
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║           ACHIEVEMENT UNLOCKED             ║
    ║                                            ║
    ║                  .--.                      ║
    ║                 /.-. '----------.          ║
    ║                 \\'-' .--"--""-"-'         ║
    ║                  '--'                      ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
    """,
    "game_over": """
    ╔════════════════════════════════╗
    ║                                ║
    ║           GAME OVER            ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ╚════════════════════════════════╝
    """,
    "victory": """
    ╔════════════════════════════════╗
    ║                                ║
    ║            VICTORY!            ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ║                                ║
    ╚════════════════════════════════╝
    """
}

class TowerOfChance:
    def __init__(self):
        self.player = {
            "name": "",
            "class": "",
            "level": 1,
            "max_level": 1,
            "items": [],
            "companions": [],
            "buffs": [],
            "debuffs": [],
            "achievements": [],
            "hidden_floors_found": [],
            "bosses_defeated": [],
            "color_theme": "default",
            "skills": {
                "luck": 1,
                "strength": 1,
                "agility": 1,
                "wisdom": 1
            }
        }
        
        # Load configuration
        config = self.load_config()
        self.tower_height = config["game_settings"]["tower_height"]
        self.animation_speed = config["game_settings"]["animation_speed"]
        
        self.challenges = self.load_challenges()
        self.colors = {
            "default": {
                "title": Fore.CYAN,
                "success": Fore.GREEN,
                "failure": Fore.RED,
                "warning": Fore.YELLOW,
                "info": Fore.WHITE,
                "luck": Fore.YELLOW,
                "skill": Fore.BLUE,
                "mixed": Fore.MAGENTA,
                "legendary": Fore.RED + Style.BRIGHT,
                "highlight": Fore.CYAN
            },
            "dark": {
                "title": Fore.BLUE,
                "success": Fore.GREEN,
                "failure": Fore.RED,
                "warning": Fore.YELLOW,
                "info": Fore.WHITE,
                "luck": Fore.YELLOW,
                "skill": Fore.CYAN,
                "mixed": Fore.MAGENTA,
                "legendary": Fore.RED,
                "highlight": Fore.BLUE
            },
            "light": {
                "title": Fore.MAGENTA,
                "success": Fore.GREEN,
                "failure": Fore.RED,
                "warning": Fore.YELLOW,
                "info": Fore.BLUE,
                "luck": Fore.YELLOW,
                "skill": Fore.CYAN,
                "mixed": Fore.MAGENTA,
                "legendary": Fore.RED + Style.BRIGHT,
                "highlight": Fore.MAGENTA
            },
            "retro": {
                "title": Fore.GREEN,
                "success": Fore.GREEN,
                "failure": Fore.RED,
                "warning": Fore.YELLOW,
                "info": Fore.GREEN,
                "luck": Fore.GREEN,
                "skill": Fore.GREEN,
                "mixed": Fore.GREEN,
                "legendary": Fore.GREEN + Style.BRIGHT,
                "highlight": Fore.GREEN
            }
        }
        self.backgrounds = [
            Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, 
            Back.MAGENTA, Back.CYAN
        ]
        self.stats = {
            "challenges_completed": 0,
            "challenges_failed": 0,
            "luck_challenges": 0,
            "skill_challenges": 0,
            "mixed_challenges": 0,
            "legendary_challenges": 0,
            "rewards_found": 0,
            "companions_met": 0,
            "bosses_faced": 0,
            "hidden_floors": 0,
            "mini_games_played": 0,
            "mini_games_won": 0
        }
        
    def load_challenges(self):
        """Load challenges from file or use defaults if file doesn't exist"""
        default_challenges = {
            "luck": [
                {"name": "Coin Flip", "description": "Guess the outcome of a coin flip", "difficulty": 1},
                {"name": "Lucky Draw", "description": "Draw a card from the deck", "difficulty": 2},
                {"name": "Roll of Fate", "description": "Roll the dice of destiny", "difficulty": 3}
            ],
            "skill": [
                {"name": "Quick Reflexes", "description": "Press the key when the timer hits zero", "difficulty": 1},
                {"name": "Memory Test", "description": "Remember the sequence of symbols", "difficulty": 2},
                {"name": "Riddle Master", "description": "Solve the ancient riddle", "difficulty": 3}
            ],
            "mixed": [
                {"name": "Treasure Hunt", "description": "Find the hidden treasure with limited clues", "difficulty": 2},
                {"name": "Dragon's Gambit", "description": "Outsmart or outrun the tower's dragon", "difficulty": 4},
                {"name": "Leap of Faith", "description": "Jump across the chasm with uncertain footing", "difficulty": 3}
            ]
        }
        
        try:
            with open("challenges.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return default_challenges
            
    def save_game(self, silent=False):
        """Save the current game state"""
        # Create saves directory if it doesn't exist
        if not os.path.exists("saves"):
            os.makedirs("saves")
            
        with open(f"saves/{self.player['name']}_save.json", "w") as f:
            save_data = {
                "player": self.player,
                "stats": self.stats
            }
            json.dump(save_data, f)
            
        if not silent:
            self.print_colored("Game saved successfully!", 
                              self.colors[self.player["color_theme"]]["success"])
            self.play_sound("success")
            
    def load_game(self, player_name):
        """Load a saved game"""
        try:
            with open(f"saves/{player_name}_save.json", "r") as f:
                save_data = json.load(f)
                
                # Handle both new and old save formats
                if "player" in save_data:
                    self.player = save_data["player"]
                    if "stats" in save_data:
                        self.stats = save_data["stats"]
                else:
                    # Old format where save_data is just the player
                    self.player = save_data
                    
            self.print_colored(f"Welcome back, {self.player['name']}!", 
                              self.colors[self.player["color_theme"]]["highlight"])
            self.play_sound("success")
            return True
        except FileNotFoundError:
            self.print_colored("No saved game found with that name.", 
                              self.colors[self.player["color_theme"]]["failure"])
            self.play_sound("failure")
            return False
            
    def print_colored(self, text, color=None, background=None):
        """Print text with colors based on the current theme"""
        if color is None:
            color = self.colors[self.player["color_theme"]]["info"]
        if background is None:
            print(f"{color}{text}")
        else:
            print(f"{color}{background}{text}")
            
    def animate_text(self, text, color=None, delay=None):
        """Animate text printing character by character"""
        if color is None:
            color = self.colors[self.player["color_theme"]]["info"]
        
        if delay is None:
            delay = self.animation_speed
        
        for char in text:
            print(f"{color}{char}", end='', flush=True)
            time.sleep(delay)
        print()
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_ascii_art(self, art_name, color=None):
        """Print ASCII art with color"""
        if color is None:
            color = self.colors[self.player["color_theme"]]["title"]
            
        if art_name in ASCII_ART:
            for line in ASCII_ART[art_name].split('\n'):
                self.print_colored(line, color)
        else:
            self.print_colored(f"ASCII art '{art_name}' not found", self.colors[self.player["color_theme"]]["warning"])
            
    def print_title(self):
        """Print the game title in a colorful way"""
        self.clear_screen()
        self.print_ascii_art("tower")
        
        title = r"""
        +--------------------------------+
        |                                |
        |       THE TOWER OF CHANCE      |
        |                                |
        |  A Game of Luck, Skill & Destiny |
        |                                |
        +--------------------------------+
        """
        
        title_color = self.colors[self.player["color_theme"]]["title"]
        for line in title.split('\n'):
            self.print_colored(line, title_color)
        print()
        
    def display_tower(self):
        """Display the tower and player's position"""
        tower_height = 20  # Visual representation height
        level_spacing = self.tower_height / tower_height
        
        self.print_colored("\n=== THE TOWER OF CHANCE ===", self.colors[self.player["color_theme"]]["title"])
        
        # Draw tower structure
        for i in range(tower_height, 0, -1):
            level = int(i * level_spacing)
            
            # Determine what to display at this level
            if level == self.player["level"]:
                marker = f"{self.colors[self.player['color_theme']]['success']}▶ YOU ARE HERE ◀{Style.RESET_ALL}"
            elif level == 100:
                marker = f"{self.colors[self.player['color_theme']]['legendary']}★ FINAL CHALLENGE ★{Style.RESET_ALL}"
            elif level % 20 == 0:
                marker = f"{self.colors[self.player['color_theme']]['legendary']}★ LEGENDARY FLOOR ★{Style.RESET_ALL}"
            elif level % 10 == 0:
                marker = f"{self.colors[self.player['color_theme']]['warning']}★ BOSS FLOOR ★{Style.RESET_ALL}"
            elif level % 5 == 0:
                marker = f"{self.colors[self.player['color_theme']]['highlight']}◆ CHECKPOINT ◆{Style.RESET_ALL}"
            else:
                marker = ""
                
            # Create the tower level visualization
            if level == self.player["level"]:
                level_str = f"{Back.GREEN}{Fore.BLACK} {level:3d} {Style.RESET_ALL}"
            elif level <= self.player["max_level"]:
                level_str = f"{self.colors[self.player['color_theme']]['success']} {level:3d} {Style.RESET_ALL}"
            else:
                level_str = f"{self.colors[self.player['color_theme']]['info']} {level:3d} {Style.RESET_ALL}"
                
            # Draw the tower structure with appropriate width based on level
            tower_width = 30 + (level // 20)  # Tower gets wider at the base
            tower_line = '║' + '═' * tower_width + '║'
            
            print(f"{level_str} {tower_line} {marker}")
            
        # Draw tower base
        base_width = 32 + (5 // 20)
        self.print_colored("╚" + "═" * base_width + "╝", self.colors[self.player["color_theme"]]["highlight"])
        print()
    def get_challenge(self, forced_type=None):
        """Get a random challenge appropriate for the current level"""
        # Determine available challenge types based on player level
        challenge_types = list(self.challenges.keys())
        
        # Filter challenge types based on player level and forced type
        available_types = []
        if forced_type and forced_type in challenge_types:
            available_types = [forced_type]
        else:
            for challenge_type in challenge_types:
                if challenge_type == "legendary" and self.player["level"] >= 20:
                    available_types.append(challenge_type)
                elif challenge_type != "legendary":
                    available_types.append(challenge_type)
                    
        # Select a challenge type
        challenge_type = random.choice(available_types)
        
        # Filter challenges by appropriate difficulty
        suitable_challenges = [c for c in self.challenges[challenge_type] 
                              if c["difficulty"] <= self.player["level"] // 5 + 1]
        
        if not suitable_challenges:
            suitable_challenges = self.challenges[challenge_type]
            
        return random.choice(suitable_challenges), challenge_type
    
    def run_luck_challenge(self, challenge, modifier=0):
        """Run a luck-based challenge"""
        self.print_colored(f"\n=== {challenge['name']} ===", Fore.YELLOW)
        self.print_colored(challenge["description"], Fore.WHITE)
        
        luck_bonus = self.player["skills"]["luck"] - 1 + modifier
        success_chance = 0.5 + (luck_bonus * 0.05)
        success_chance = max(0.1, min(0.9, success_chance))  # Cap between 10% and 90%
        
        if challenge["name"] == "Coin Flip":
            guess = input("\nHeads or Tails? (h/t): ").lower()
            result = random.choice(["h", "t"])
            
            self.print_colored("\nThe coin flips through the air...", Fore.CYAN)
            time.sleep(1)
            
            if result == "h":
                self.print_colored("It's HEADS!", Fore.YELLOW)
            else:
                self.print_colored("It's TAILS!", Fore.YELLOW)
                
            return guess == result or random.random() < success_chance
            
        elif challenge["name"] == "Lucky Draw":
            cards = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7"]
            target = random.choice(cards)
            
            self.print_colored(f"\nYou must draw the {target} to succeed!", Fore.CYAN)
            input("Press Enter to draw a card...")
            
            drawn = random.choice(cards)
            self.print_colored(f"\nYou drew the {drawn}!", Fore.YELLOW)
            
            return drawn == target or random.random() < success_chance
            
        elif challenge["name"] == "Roll of Fate":
            target = random.randint(1, 6)
            
            self.print_colored(f"\nYou must roll a {target} to succeed!", Fore.CYAN)
            input("Press Enter to roll the dice...")
            
            roll = random.randint(1, 6)
            self.print_colored(f"\nYou rolled a {roll}!", Fore.YELLOW)
            
            return roll == target or random.random() < success_chance
            
        # Default fallback
        return random.random() < success_chance
    
    def run_skill_challenge(self, challenge, modifier=0):
        """Run a skill-based challenge"""
        self.print_colored(f"\n=== {challenge['name']} ===", Fore.BLUE)
        self.print_colored(challenge["description"], Fore.WHITE)
        
        if challenge["name"] == "Quick Reflexes":
            self.print_colored("\nPress Enter exactly when the countdown reaches 0!", Fore.CYAN)
            
            for i in range(3, 0, -1):
                self.print_colored(f"{i}...", Fore.YELLOW)
                time.sleep(random.uniform(0.7, 1.3))
                
            self.print_colored("NOW!", Fore.GREEN)
            start_time = time.time()
            input()
            reaction_time = time.time() - start_time
            
            self.print_colored(f"Your reaction time: {reaction_time:.3f} seconds", Fore.CYAN)
            
            # Adjust threshold based on agility and modifier
            threshold = 0.5 + (self.player["skills"]["agility"] * 0.1) + (modifier * 0.1)
            return reaction_time < threshold
            
        elif challenge["name"] == "Memory Test":
            sequence_length = 4 + self.player["level"] // 10
            # Adjust for difficulty modifier
            sequence_length = max(3, sequence_length - modifier)
            
            symbols = ["★", "♦", "♥", "♠", "♣", "▲", "■", "●"]
            sequence = [random.choice(symbols) for _ in range(sequence_length)]
            
            self.print_colored("\nMemorize this sequence:", Fore.CYAN)
            self.print_colored(" ".join(sequence), Fore.YELLOW)
            
            time.sleep(2 + sequence_length * 0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            guess = input("Enter the sequence (symbols separated by spaces): ")
            guess_sequence = guess.split()
            
            return guess_sequence == sequence
            
        elif challenge["name"] == "Riddle Master":
            riddles = [
                {"q": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "a": "echo"},
                {"q": "The more you take, the more you leave behind. What am I?", "a": "footsteps"},
                {"q": "What has keys but no locks, space but no room, and you can enter but not go in?", "a": "keyboard"}
            ]
            
            riddle = random.choice(riddles)
            self.print_colored(f"\nRiddle: {riddle['q']}", Fore.CYAN)
            
            answer = input("Your answer: ").lower().strip()
            
            # Wisdom helps with partial answers, modified by the modifier
            wisdom_threshold = 2 - modifier
            if answer == riddle["a"]:
                return True
            elif self.player["skills"]["wisdom"] > wisdom_threshold and riddle["a"] in answer:
                self.print_colored("Your wisdom helped you find the answer!", Fore.GREEN)
                return True
            else:
                self.print_colored(f"The correct answer was: {riddle['a']}", Fore.RED)
                return False
                
        # Default fallback
        return random.random() < (0.5 + (modifier * 0.1))
        
    def run_mixed_challenge(self, challenge, modifier=0):
        """Run a challenge that combines luck and skill"""
        self.print_colored(f"\n=== {challenge['name']} ===", Fore.MAGENTA)
        self.print_colored(challenge["description"], Fore.WHITE)
        
        if challenge["name"] == "Treasure Hunt":
            self.print_colored("\nYou must find the hidden treasure!", Fore.CYAN)
            
            # Skill component - solve a simple puzzle
            puzzle_solved = False
            clues = ["The treasure is hidden in a place that rhymes with 'test'", 
                    "Look for something that can hold items", 
                    "It might be where you store valuable things"]
            
            self.print_colored("Here are your clues:", Fore.YELLOW)
            for clue in clues:
                self.print_colored(f"- {clue}", Fore.WHITE)
                
            answer = input("\nWhere is the treasure hidden? ").lower()
            if "chest" in answer:
                puzzle_solved = True
                
            # Luck component - find the right chest
            if puzzle_solved:
                self.print_colored("\nYou found the chests! But which one contains the treasure?", Fore.CYAN)
                chest_choice = input("Choose chest 1, 2, or 3: ")
                
                lucky_chest = str(random.randint(1, 3))
                luck_bonus = self.player["skills"]["luck"] * 0.1 + modifier * 0.05
                
                return chest_choice == lucky_chest or random.random() < (0.33 + luck_bonus)
            else:
                return False
                
        elif challenge["name"] == "Dragon's Gambit":
            self.print_colored("\nA dragon blocks your path! You can try to outsmart it or outrun it.", Fore.RED)
            choice = input("Will you use your wits (w) or speed (s)? ").lower()
            
            if choice == 'w':
                # Wisdom-based challenge
                wisdom_check = random.random() < (0.4 + self.player["skills"]["wisdom"] * 0.1 + modifier * 0.05)
                if wisdom_check:
                    self.print_colored("You cleverly distract the dragon with a riddle!", Fore.GREEN)
                    return True
                else:
                    self.print_colored("The dragon sees through your ploy!", Fore.RED)
                    return False
            else:
                # Agility-based challenge
                agility_check = random.random() < (0.4 + self.player["skills"]["agility"] * 0.1 + modifier * 0.05)
                if agility_check:
                    self.print_colored("You dash past the dragon with incredible speed!", Fore.GREEN)
                    return True
                else:
                    self.print_colored("The dragon is too quick for you!", Fore.RED)
                    return False
                    
        elif challenge["name"] == "Leap of Faith":
            self.print_colored("\nYou must jump across a chasm with uncertain footing.", Fore.CYAN)
            
            # Strength affects jump distance
            strength_factor = self.player["skills"]["strength"] * 0.15 + modifier * 0.05
            # Luck affects finding good footing
            luck_factor = self.player["skills"]["luck"] * 0.1 + modifier * 0.05
            
            input("Press Enter to jump...")
            
            jump_success = random.random() < (0.5 + strength_factor)
            footing_success = random.random() < (0.5 + luck_factor)
            
            if jump_success and footing_success:
                self.print_colored("Perfect jump! You land safely on the other side.", Fore.GREEN)
                return True
            elif jump_success:
                self.print_colored("You jump far enough but slip on landing! You barely hang on!", Fore.YELLOW)
                return True
            elif footing_success:
                self.print_colored("You found good footing but didn't jump far enough. You fall!", Fore.RED)
                return False
            else:
                self.print_colored("You slip and fall into the chasm!", Fore.RED)
                return False
                
        # Default fallback
        return random.random() < (0.5 + modifier * 0.1)
        
    def run_challenge(self):
        """Run a random challenge based on the player's level"""
        # Check for boss floor
        if self.check_for_boss_floor():
            success = self.run_boss_challenge()
            if success:
                self.player["level"] += 1
                if self.player["level"] > self.player["max_level"]:
                    self.player["max_level"] = self.player["level"]
                self.check_for_achievement("level")
            return success
            
        # Check for hidden floor
        if self.check_for_hidden_floor():
            self.player["level"] += 1
            if self.player["level"] > self.player["max_level"]:
                self.player["max_level"] = self.player["level"]
            self.check_for_achievement("level")
            return True
            
        # Random chance for mini-game
        if random.random() < 0.15:
            self.stats["mini_games_played"] += 1
            result = self.run_mini_game()
            if result:
                self.stats["mini_games_won"] += 1
        
        # Check for branching paths
        chosen_path = self.present_branching_path()
        
        if chosen_path:
            challenge_type = chosen_path["challenge_type"]
            difficulty_mod = chosen_path["difficulty_mod"]
            reward_chance = chosen_path["reward_chance"]
        else:
            challenge_type = None
            difficulty_mod = 0
            reward_chance = 0.3
        
        # Get challenge
        challenge, challenge_type = self.get_challenge(challenge_type)
        
        # Update challenge type stats
        if challenge_type == "luck":
            self.stats["luck_challenges"] += 1
        elif challenge_type == "skill":
            self.stats["skill_challenges"] += 1
        elif challenge_type == "mixed":
            self.stats["mixed_challenges"] += 1
        elif challenge_type == "legendary":
            self.stats["legendary_challenges"] += 1
        
        # Display environment information
        self.display_environment()
        
        # Show active effects
        if self.player["buffs"] or self.player["debuffs"]:
            self.print_colored("\n=== ACTIVE EFFECTS ===", 
                              self.colors[self.player["color_theme"]]["title"])
            self.show_active_effects()
        
        # Show companions
        if self.player["companions"]:
            self.print_colored("\n=== COMPANIONS ===", 
                              self.colors[self.player["color_theme"]]["title"])
            self.show_companions()
        
        self.print_colored(f"\nFloor {self.player['level']} Challenge:", 
                          self.colors[self.player["color_theme"]]["title"])
        
        # Apply environment effects
        environment_mod = self.apply_weather_effects(challenge_type)
        if environment_mod != 0:
            effect_type = "bonus" if environment_mod > 0 else "penalty"
            self.print_colored(f"Environment {effect_type}: {environment_mod}", 
                             self.colors[self.player["color_theme"]]["success" if environment_mod > 0 else "failure"])
        
        # Apply buffs and debuffs
        effects_mod = self.apply_buffs_and_debuffs(challenge_type)
        if effects_mod != 0:
            effect_type = "bonus" if effects_mod > 0 else "penalty"
            self.print_colored(f"Status effects {effect_type}: {effects_mod}", 
                             self.colors[self.player["color_theme"]]["success" if effects_mod > 0 else "failure"])
        
        # Apply companion effects
        companion_mod = self.apply_companion_effects(challenge_type)
        if companion_mod != 0:
            self.print_colored(f"Companion bonus: {companion_mod}", 
                              self.colors[self.player["color_theme"]]["success"])
        
        # Apply total modifier to challenge
        total_mod = environment_mod + effects_mod + companion_mod + difficulty_mod
        
        if challenge_type == "luck":
            success = self.run_luck_challenge(challenge, total_mod)
        elif challenge_type == "skill":
            success = self.run_skill_challenge(challenge, total_mod)
        elif challenge_type == "legendary":
            success = self.run_legendary_challenge(challenge, total_mod)
        else:  # mixed
            success = self.run_mixed_challenge(challenge, total_mod)
            
        if success:
            self.clear_screen()
            self.print_colored("\nCHALLENGE COMPLETED SUCCESSFULLY!", 
                              self.colors[self.player["color_theme"]]["success"])
            self.player["level"] += 1
            if self.player["level"] > self.player["max_level"]:
                self.player["max_level"] = self.player["level"]
                
            # Check for achievements
            self.check_for_achievement("level")
            
            # Check for skill achievements
            for skill, value in self.player["skills"].items():
                self.check_for_achievement("skill", (skill, value))
                
            # Check for reward based on path
            if random.random() < reward_chance:
                self.give_reward()
                self.stats["rewards_found"] += 1
                
            # Random chance for buffs on success
            if random.random() < 0.2:
                buff_types = ["luck", "skill", "mixed", "all"]
                buff_type = random.choice(buff_types)
                self.add_buff(f"Victory Surge", buff_type, 1, random.randint(1, 3))
                
            # Check for game completion
            if self.player["level"] >= self.tower_height:
                self.game_completed()
                
            return True
        else:
            self.clear_screen()
            self.print_colored("\nCHALLENGE FAILED!", 
                              self.colors[self.player["color_theme"]]["failure"])
            
            # Random chance for debuffs on failure
            if random.random() < 0.3:
                debuff_types = ["luck", "skill", "mixed", "all"]
                debuff_type = random.choice(debuff_types)
                self.add_debuff(f"Setback", debuff_type, -1, random.randint(1, 2))
                
            return False
            
    def game_completed(self):
        """Handle game completion"""
        self.clear_screen()
        self.print_ascii_art("victory", self.colors[self.player["color_theme"]]["success"])
        
        self.animate_text("CONGRATULATIONS!", 
                         self.colors[self.player["color_theme"]]["success"], 0.05)
        self.animate_text("You have reached the top of the Tower of Chance!", 
                         self.colors[self.player["color_theme"]]["title"], 0.03)
        self.animate_text("Your journey has come to an end, but your legend will live on.", 
                         self.colors[self.player["color_theme"]]["info"], 0.02)
        
        # Show final stats
        self.print_colored("\n=== FINAL STATISTICS ===", 
                          self.colors[self.player["color_theme"]]["title"])
        self.print_colored(f"Character: {self.player['name']} the {self.player['class']}", 
                          self.colors[self.player["color_theme"]]["info"])
        self.print_colored(f"Challenges Completed: {self.stats['challenges_completed']}", 
                          self.colors[self.player["color_theme"]]["success"])
        self.print_colored(f"Challenges Failed: {self.stats['challenges_failed']}", 
                          self.colors[self.player["color_theme"]]["failure"])
        self.print_colored(f"Bosses Defeated: {len(self.player['bosses_defeated'])}", 
                          self.colors[self.player["color_theme"]]["warning"])
        self.print_colored(f"Hidden Floors Found: {len(self.player['hidden_floors_found'])}", 
                          self.colors[self.player["color_theme"]]["highlight"])
        self.print_colored(f"Achievements Earned: {len(self.player['achievements'])}", 
                          self.colors[self.player["color_theme"]]["warning"])
        
        input("\nPress Enter to return to the main menu...")
        self.start_game()
            
    def give_reward(self, force=False):
        """Give the player a random reward"""
        # Different tiers of rewards based on player level
        basic_rewards = [
            "Lucky Coin (+1 Luck)",
            "Strength Potion (+1 Strength)",
            "Agility Boots (+1 Agility)",
            "Wisdom Scroll (+1 Wisdom)",
            "Health Potion (Restore health)",
            "Magic Map (Reveal next challenge)"
        ]
        
        advanced_rewards = [
            "Fortune's Charm (+2 Luck)",
            "Giant's Elixir (+2 Strength)",
            "Wind Walker Boots (+2 Agility)",
            "Ancient Tome (+2 Wisdom)",
            "Phoenix Feather (Automatic revival)",
            "Oracle's Eye (Skip a challenge)"
        ]
        
        legendary_rewards = [
            "Destiny's Die (+3 to all stats)",
            "Titan's Heart (Double strength for 3 floors)",
            "Cosmic Insight (Automatic success on wisdom challenges)",
            "Fate's Favor (Reroll any failed challenge once)"
        ]
        
        # Select reward tier based on player level
        if self.player["level"] >= 40:
            reward_pool = legendary_rewards + advanced_rewards
        elif self.player["level"] >= 20:
            reward_pool = advanced_rewards + basic_rewards
        else:
            reward_pool = basic_rewards
        
        reward = random.choice(reward_pool)
        self.player["items"].append(reward)
        
        self.print_colored(f"\nYou found a reward: {reward}", Fore.YELLOW)
        
        # Apply stat bonuses
        if "Luck" in reward:
            if "+3" in reward:
                self.player["skills"]["luck"] += 3
            elif "+2" in reward:
                self.player["skills"]["luck"] += 2
            else:
                self.player["skills"]["luck"] += 1
        elif "Strength" in reward:
            if "+3" in reward:
                self.player["skills"]["strength"] += 3
            elif "+2" in reward:
                self.player["skills"]["strength"] += 2
            else:
                self.player["skills"]["strength"] += 1
        elif "Agility" in reward:
            if "+3" in reward:
                self.player["skills"]["agility"] += 3
            elif "+2" in reward:
                self.player["skills"]["agility"] += 2
            else:
                self.player["skills"]["agility"] += 1
        elif "Wisdom" in reward:
            if "+3" in reward:
                self.player["skills"]["wisdom"] += 3
            elif "+2" in reward:
                self.player["skills"]["wisdom"] += 2
            else:
                self.player["skills"]["wisdom"] += 1
        elif "all stats" in reward:
            for skill in self.player["skills"]:
                self.player["skills"][skill] += 3
                
        # Check for skill achievements after rewards
        for skill, value in self.player["skills"].items():
            self.check_for_achievement("skill", (skill, value))
            
    def show_inventory(self):
        """Display the player's inventory and stats"""
        self.print_colored("\n=== INVENTORY & STATS ===", Fore.CYAN)
        self.print_colored(f"Name: {self.player['name']}", Fore.WHITE)
        self.print_colored(f"Class: {self.player['class']}", Fore.YELLOW)
        self.print_colored(f"Current Level: {self.player['level']}", Fore.GREEN)
        self.print_colored(f"Highest Level: {self.player['max_level']}", Fore.YELLOW)
        
        self.print_colored("\nSkills:", Fore.CYAN)
        for skill, value in self.player["skills"].items():
            self.print_colored(f"  {skill.capitalize()}: {value}", Fore.WHITE)
            
        if self.player["items"]:
            self.print_colored("\nItems:", Fore.CYAN)
            for item in self.player["items"]:
                self.print_colored(f"  - {item}", Fore.WHITE)
        else:
            self.print_colored("\nItems: None", Fore.WHITE)
            
        # Show companions
        self.print_colored("\nCompanions:", Fore.CYAN)
        if self.player["companions"]:
            for companion in self.player["companions"]:
                self.print_colored(f"  - {companion['name']}: {companion['ability']}", Fore.WHITE)
        else:
            self.print_colored("  None", Fore.WHITE)
            
        # Show active effects
        self.print_colored("\nActive Effects:", Fore.CYAN)
        if self.player["buffs"] or self.player["debuffs"]:
            self.show_active_effects()
        else:
            self.print_colored("  None", Fore.WHITE)
            
        # Show achievements
        self.print_colored("\nAchievements:", Fore.CYAN)
        if self.player["achievements"]:
            for achievement in self.player["achievements"]:
                self.print_colored(f"  - {achievement['name']}: {achievement['description']}", Fore.WHITE)
        else:
            self.print_colored("  None", Fore.WHITE)
            
        # Show special discoveries
        self.print_colored("\nSpecial Discoveries:", Fore.CYAN)
        
        # Hidden floors
        if self.player["hidden_floors_found"]:
            self.print_colored(f"  Hidden Floors Found: {len(self.player['hidden_floors_found'])}", Fore.WHITE)
        else:
            self.print_colored("  Hidden Floors Found: 0", Fore.WHITE)
            
        # Bosses defeated
        if self.player["bosses_defeated"]:
            self.print_colored(f"  Bosses Defeated: {len(self.player['bosses_defeated'])}", Fore.WHITE)
        else:
            self.print_colored("  Bosses Defeated: 0", Fore.WHITE)
            
    def game_loop(self):
        """Main game loop"""
        while True:
            # Auto-save if enabled
            self.auto_save()
            
            # Update environment (time of day, weather) each turn
            current_weather = self.get_weather()
            current_time = self.get_time_of_day()
            
            self.display_tower()
            
            print("\nWhat would you like to do?")
            self.print_colored("1. Climb to next floor (challenge)", 
                              self.colors[self.player["color_theme"]]["highlight"])
            self.print_colored("2. View inventory and stats", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored("3. Check environment", 
                              self.colors[self.player["color_theme"]]["mixed"])
            self.print_colored("4. View achievements", 
                              self.colors[self.player["color_theme"]]["warning"])
            self.print_colored("5. View progress statistics", 
                              self.colors[self.player["color_theme"]]["luck"])
            self.print_colored("6. Change color theme", 
                              self.colors[self.player["color_theme"]]["skill"])
            self.print_colored("7. Game settings", 
                              self.colors[self.player["color_theme"]]["highlight"])
            self.print_colored("8. Challenge editor", 
                              self.colors[self.player["color_theme"]]["mixed"])
            self.print_colored("9. Save game", 
                              self.colors[self.player["color_theme"]]["success"])
            self.print_colored("10. Quit", 
                              self.colors[self.player["color_theme"]]["failure"])
            
            choice = input("\nEnter your choice (1-10): ")
            
            if choice == "1":
                # Random chance to encounter a companion before a challenge
                config = self.load_config()
                encounter_chance = config["companion_settings"]["encounter_chance"]
                max_companions = config["companion_settings"]["max_companions"]
                
                if random.random() < encounter_chance and len(self.player["companions"]) < max_companions:
                    self.encounter_companion()
                    self.stats["companions_met"] += 1
                
                result = self.run_challenge()
                if result:
                    self.stats["challenges_completed"] += 1
                else:
                    self.stats["challenges_failed"] += 1
                    
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.show_inventory()
                input("\nPress Enter to continue...")
            elif choice == "3":
                self.display_environment()
                input("\nPress Enter to continue...")
            elif choice == "4":
                self.show_achievements()
                input("\nPress Enter to continue...")
            elif choice == "5":
                self.show_progress_visualization()
            elif choice == "6":
                self.choose_color_theme()
            elif choice == "7":
                self.edit_settings()
            elif choice == "8":
                self.challenge_editor()
            elif choice == "9":
                self.save_game()
                input("\nPress Enter to continue...")
            elif choice == "10":
                self.clear_screen()
                self.animate_text("Thanks for playing Tower of Chance!", 
                                 self.colors[self.player["color_theme"]]["title"])
                break
            else:
                self.print_colored("Invalid choice! Please try again.", 
                                  self.colors[self.player["color_theme"]]["failure"])
                
    def start_game(self):
        """Start the game"""
        self.clear_screen()
        self.print_title()
        
        # Set default color theme
        if "color_theme" not in self.player or not self.player["color_theme"]:
            self.player["color_theme"] = "default"
        
        self.animate_text("Welcome to the Tower of Chance!", 
                         self.colors[self.player["color_theme"]]["title"], 0.03)
        self.print_colored("1. New Game", self.colors[self.player["color_theme"]]["success"])
        self.print_colored("2. Load Game", self.colors[self.player["color_theme"]]["info"])
        self.print_colored("3. Quit", self.colors[self.player["color_theme"]]["failure"])
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            self.create_character()
            self.choose_color_theme()
            self.game_loop()
        elif choice == "2":
            player_name = input("Enter your character's name: ")
            if self.load_game(player_name):
                self.game_loop()
        elif choice == "3":
            self.animate_text("Maybe next time!", 
                             self.colors[self.player["color_theme"]]["title"], 0.03)
        else:
            self.print_colored("Invalid choice!", 
                              self.colors[self.player["color_theme"]]["failure"])
            
    def run_legendary_challenge(self, challenge, modifier=0):
        """Run a legendary challenge that tests the limits of the player's abilities"""
        self.print_colored(f"\n=== {challenge['name']} ===", Fore.RED + Style.BRIGHT)
        self.print_colored(challenge["description"], Fore.WHITE)
        
        if challenge["name"] == "Phoenix Rebirth":
            self.print_colored("\nThe flames of the phoenix surround you. To be reborn, you must face your greatest failure.", Fore.RED)
            
            # Combine all skills for this challenge
            total_skill = sum(self.player["skills"].values())
            success_chance = 0.3 + (total_skill * 0.02) + (modifier * 0.05)
            success_chance = max(0.1, min(0.9, success_chance))  # Cap between 10% and 90%
            
            input("Press Enter to embrace the flames...")
            
            if random.random() < success_chance:
                self.print_colored("\nYou emerge from the flames, stronger than before!", Fore.YELLOW)
                # Boost a random skill
                skill = random.choice(list(self.player["skills"].keys()))
                self.player["skills"][skill] += 1
                self.print_colored(f"Your {skill} has increased!", Fore.GREEN)
                return True
            else:
                self.print_colored("\nThe flames consume you, but you are not yet ready to be reborn.", Fore.RED)
                return False
                
        elif challenge["name"] == "Titan's Challenge":
            self.print_colored("\nA colossal titan blocks your path. It offers you three trials - strength, wisdom, or chance.", Fore.CYAN)
            choice = input("Which do you choose? (s/w/c): ").lower()
            
            if choice == 's':
                # Strength challenge
                strength_check = random.random() < (0.3 + self.player["skills"]["strength"] * 0.05 + modifier * 0.05)
                if strength_check:
                    self.print_colored("\nYou match the titan's strength, impressing it greatly!", Fore.GREEN)
                    return True
                else:
                    self.print_colored("\nThe titan's might is too great for you to overcome.", Fore.RED)
                    return False
            elif choice == 'w':
                # Wisdom challenge
                wisdom_check = random.random() < (0.3 + self.player["skills"]["wisdom"] * 0.05 + modifier * 0.05)
                if wisdom_check:
                    self.print_colored("\nYour wisdom allows you to solve the titan's ancient riddle!", Fore.GREEN)
                    return True
                else:
                    self.print_colored("\nThe riddle's complexity is beyond your current understanding.", Fore.RED)
                    return False
            else:
                # Chance challenge
                luck_check = random.random() < (0.3 + self.player["skills"]["luck"] * 0.05 + modifier * 0.05)
                if luck_check:
                    self.print_colored("\nFortune favors you in this gamble with the titan!", Fore.GREEN)
                    return True
                else:
                    self.print_colored("\nLuck is not on your side today.", Fore.RED)
                    return False
                    
        elif challenge["name"] == "Cosmic Harmony":
            self.print_colored("\nYou must align the elements of existence into perfect balance.", Fore.MAGENTA)
            
            # This challenge tests all skills
            elements = ["fire", "water", "earth", "air", "void"]
            random.shuffle(elements)
            
            self.print_colored("\nArrange these elements in harmonious order:", Fore.CYAN)
            for i, element in enumerate(elements):
                self.print_colored(f"{i+1}. {element}", Fore.WHITE)
                
            # The player needs to make a choice, but the outcome is influenced by their skills
            input("\nMeditate on the correct order and press Enter when ready...")
            
            # Calculate success chance based on all skills
            total_skill = sum(self.player["skills"].values())
            success_chance = 0.2 + (total_skill * 0.015) + (modifier * 0.05)
            success_chance = max(0.1, min(0.9, success_chance))  # Cap between 10% and 90%
            
            if random.random() < success_chance:
                self.print_colored("\nYou feel the elements align under your guidance!", Fore.GREEN)
                return True
            else:
                self.print_colored("\nThe elements resist your attempt to bring them into harmony.", Fore.RED)
                return False
                
        elif challenge["name"] == "Ultimate Ascension":
            self.print_colored("\nYou stand at the pinnacle of the tower. One final challenge remains.", Fore.CYAN)
            self.print_colored("To ascend beyond your mortal form, you must prove your mastery of all skills.", Fore.WHITE)
            
            # This is the final challenge - it should be difficult but fair
            trials_passed = 0
            trials_needed = 3
            
            # Luck trial
            self.print_colored("\n--- Trial of Fortune ---", Fore.YELLOW)
            luck_roll = random.random()
            luck_threshold = 0.5 - (self.player["skills"]["luck"] * 0.04) - (modifier * 0.05)
            luck_threshold = max(0.1, min(0.9, luck_threshold))  # Cap between 10% and 90%
            if luck_roll > luck_threshold:
                self.print_colored("You pass the Trial of Fortune!", Fore.GREEN)
                trials_passed += 1
            else:
                self.print_colored("Fortune does not favor you in this trial.", Fore.RED)
                
            # Strength trial
            self.print_colored("\n--- Trial of Power ---", Fore.RED)
            strength_roll = random.random()
            strength_threshold = 0.5 - (self.player["skills"]["strength"] * 0.04) - (modifier * 0.05)
            strength_threshold = max(0.1, min(0.9, strength_threshold))  # Cap between 10% and 90%
            if strength_roll > strength_threshold:
                self.print_colored("You pass the Trial of Power!", Fore.GREEN)
                trials_passed += 1
            else:
                self.print_colored("Your strength falters in this trial.", Fore.RED)
                
            # Wisdom trial
            self.print_colored("\n--- Trial of Wisdom ---", Fore.BLUE)
            wisdom_roll = random.random()
            wisdom_threshold = 0.5 - (self.player["skills"]["wisdom"] * 0.04) - (modifier * 0.05)
            wisdom_threshold = max(0.1, min(0.9, wisdom_threshold))  # Cap between 10% and 90%
            if wisdom_roll > wisdom_threshold:
                self.print_colored("You pass the Trial of Wisdom!", Fore.GREEN)
                trials_passed += 1
            else:
                self.print_colored("Your wisdom is insufficient for this trial.", Fore.RED)
                
            # Agility trial
            self.print_colored("\n--- Trial of Grace ---", Fore.CYAN)
            agility_roll = random.random()
            agility_threshold = 0.5 - (self.player["skills"]["agility"] * 0.04) - (modifier * 0.05)
            agility_threshold = max(0.1, min(0.9, agility_threshold))  # Cap between 10% and 90%
            if agility_roll > agility_threshold:
                self.print_colored("You pass the Trial of Grace!", Fore.GREEN)
                trials_passed += 1
            else:
                self.print_colored("Your agility fails you in this trial.", Fore.RED)
                
            # Determine final outcome
            if trials_passed >= trials_needed:
                self.print_colored(f"\nYou passed {trials_passed} of 4 trials!", Fore.GREEN)
                self.print_colored("\nA blinding light envelops you as you transcend your mortal form!", Fore.YELLOW)
                return True
            else:
                self.print_colored(f"\nYou passed only {trials_passed} of 4 trials.", Fore.RED)
                self.print_colored("\nYou are not yet ready for ascension.", Fore.RED)
                return False
                
        # Default fallback for other legendary challenges
        self.print_colored("\nYou face a legendary challenge that tests the limits of your abilities.", Fore.YELLOW)
        
        # Base chance of success is low but scales with player skills
        total_skill = sum(self.player["skills"].values())
        success_chance = 0.2 + (total_skill * 0.01) + (modifier * 0.05)
        success_chance = max(0.1, min(0.9, success_chance))  # Cap between 10% and 90%
        
        input("Press Enter to face your destiny...")
        
        if random.random() < success_chance:
            self.print_colored("\nAgainst all odds, you triumph!", Fore.GREEN)
            return True
        else:
            self.print_colored("\nDespite your best efforts, you fail to overcome this legendary challenge.", Fore.RED)
            return False
    def get_time_of_day(self):
        """Get the current time of day in the tower"""
        # Cycle through day and night every 5 floors
        if self.player["level"] % 10 < 5:
            return "day"
        else:
            return "night"
            
    def get_weather(self):
        """Determine the current weather in the tower"""
        # Weather changes every 3 floors
        weather_seed = self.player["level"] // 3
        random.seed(weather_seed)
        
        weathers = [
            {"name": "Clear", "effect": "No special effects", "modifier": 0},
            {"name": "Foggy", "effect": "Reduced visibility affects Wisdom challenges", "modifier": -1},
            {"name": "Stormy", "effect": "Lightning affects Luck challenges", "modifier": -1},
            {"name": "Windy", "effect": "Strong winds affect Agility challenges", "modifier": -1},
            {"name": "Sunny", "effect": "Bright sun boosts all challenges", "modifier": 1},
            {"name": "Moonlit", "effect": "Mystical moonlight boosts Luck challenges", "modifier": 1}
        ]
        
        weather = random.choice(weathers)
        # Reset the random seed
        random.seed()
        
        return weather
        
    def apply_weather_effects(self, challenge_type):
        """Apply weather effects to challenges"""
        weather = self.get_weather()
        time_of_day = self.get_time_of_day()
        
        # Apply weather modifiers
        modifier = 0
        
        if weather["name"] == "Foggy" and challenge_type == "skill":
            modifier += weather["modifier"]
        elif weather["name"] == "Stormy" and challenge_type == "luck":
            modifier += weather["modifier"]
        elif weather["name"] == "Windy" and challenge_type == "mixed":
            modifier += weather["modifier"]
        elif weather["name"] == "Sunny":
            modifier += weather["modifier"]
        elif weather["name"] == "Moonlit" and challenge_type == "luck":
            modifier += weather["modifier"]
            
        # Apply time of day modifiers
        if time_of_day == "day" and challenge_type == "skill":
            modifier += 1
        elif time_of_day == "night" and challenge_type == "luck":
            modifier += 1
            
        return modifier
        
    def display_environment(self):
        """Display the current environment conditions"""
        weather = self.get_weather()
        time_of_day = self.get_time_of_day()
        
        self.print_colored("\n=== ENVIRONMENT ===", Fore.CYAN)
        
        # Display time of day
        if time_of_day == "day":
            self.print_colored(f"Time: {Fore.YELLOW}☀ Day{Style.RESET_ALL}", Fore.WHITE)
        else:
            self.print_colored(f"Time: {Fore.BLUE}☽ Night{Style.RESET_ALL}", Fore.WHITE)
            
        # Display weather
        weather_color = Fore.WHITE
        if weather["modifier"] > 0:
            weather_color = Fore.GREEN
        elif weather["modifier"] < 0:
            weather_color = Fore.RED
            
        self.print_colored(f"Weather: {weather_color}{weather['name']}{Style.RESET_ALL}", Fore.WHITE)
        self.print_colored(f"Effect: {weather['effect']}", Fore.WHITE)
        
    def apply_buffs_and_debuffs(self, challenge_type, skill_type=None):
        """Apply active buffs and debuffs to challenges"""
        modifier = 0
        
        # Process buffs
        active_buffs = []
        for buff in self.player["buffs"]:
            if buff["duration"] > 0:
                # Apply buff effect
                if buff["affects"] == "all" or buff["affects"] == challenge_type:
                    modifier += buff["modifier"]
                    
                # Reduce duration
                buff["duration"] -= 1
                if buff["duration"] > 0:
                    active_buffs.append(buff)
                else:
                    self.print_colored(f"Your {buff['name']} buff has expired.", Fore.YELLOW)
                    
        # Process debuffs
        active_debuffs = []
        for debuff in self.player["debuffs"]:
            if debuff["duration"] > 0:
                # Apply debuff effect
                if debuff["affects"] == "all" or debuff["affects"] == challenge_type:
                    modifier += debuff["modifier"]  # Debuffs have negative modifiers
                    
                # Reduce duration
                debuff["duration"] -= 1
                if debuff["duration"] > 0:
                    active_debuffs.append(debuff)
                else:
                    self.print_colored(f"Your {debuff['name']} debuff has expired.", Fore.GREEN)
                    
        # Update active buffs and debuffs
        self.player["buffs"] = active_buffs
        self.player["debuffs"] = active_debuffs
        
        return modifier
        
    def add_buff(self, name, affects, modifier, duration):
        """Add a buff to the player"""
        buff = {
            "name": name,
            "affects": affects,
            "modifier": modifier,
            "duration": duration
        }
        
        self.player["buffs"].append(buff)
        self.print_colored(f"You gained {name} buff for {duration} floors!", Fore.GREEN)
        
    def add_debuff(self, name, affects, modifier, duration):
        """Add a debuff to the player"""
        debuff = {
            "name": name,
            "affects": affects,
            "modifier": modifier,  # Should be negative
            "duration": duration
        }
        
        self.player["debuffs"].append(debuff)
        self.print_colored(f"You suffered {name} debuff for {duration} floors!", Fore.RED)
        
    def show_active_effects(self):
        """Display active buffs and debuffs"""
        if not self.player["buffs"] and not self.player["debuffs"]:
            self.print_colored("No active effects.", Fore.WHITE)
            return
            
        if self.player["buffs"]:
            self.print_colored("\nActive Buffs:", Fore.GREEN)
            for buff in self.player["buffs"]:
                self.print_colored(f"  - {buff['name']}: +{buff['modifier']} to {buff['affects']} challenges for {buff['duration']} more floors", Fore.WHITE)
                
        if self.player["debuffs"]:
            self.print_colored("\nActive Debuffs:", Fore.RED)
            for debuff in self.player["debuffs"]:
                self.print_colored(f"  - {debuff['name']}: {debuff['modifier']} to {debuff['affects']} challenges for {debuff['duration']} more floors", Fore.WHITE)
                
    def add_companion(self, companion):
        """Add a companion to the player's party"""
        self.player["companions"].append(companion)
        self.print_colored(f"\n{companion['name']} has joined your party!", Fore.CYAN)
        self.print_colored(f"Ability: {companion['ability']}", Fore.WHITE)
        
    def show_companions(self):
        """Display the player's companions"""
        if not self.player["companions"]:
            self.print_colored("You have no companions.", Fore.WHITE)
            return
            
        self.print_colored("\nCompanions:", Fore.CYAN)
        for companion in self.player["companions"]:
            self.print_colored(f"  - {companion['name']}: {companion['ability']}", Fore.WHITE)
            
    def apply_companion_effects(self, challenge_type):
        """Apply companion effects to challenges"""
        modifier = 0
        
        for companion in self.player["companions"]:
            if companion["type"] == "all" or companion["type"] == challenge_type:
                modifier += companion["modifier"]
                
        return modifier
        
    def encounter_companion(self):
        """Random chance to encounter a companion"""
        companions = [
            {"name": "Whiskers the Lucky Cat", "ability": "Improves luck challenges", "type": "luck", "modifier": 1},
            {"name": "Brutus the Warrior", "ability": "Improves strength-based challenges", "type": "skill", "modifier": 1},
            {"name": "Zephyr the Wind Spirit", "ability": "Improves agility challenges", "type": "skill", "modifier": 1},
            {"name": "Athena the Owl", "ability": "Improves wisdom challenges", "type": "skill", "modifier": 1},
            {"name": "Echo the Fairy", "ability": "Improves all challenges slightly", "type": "all", "modifier": 1},
            {"name": "Shadow the Rogue", "ability": "Improves mixed challenges", "type": "mixed", "modifier": 1},
            {"name": "Luna the Mystic", "ability": "Improves night-time challenges", "type": "all", "modifier": 1}
        ]
        
        # Filter out companions the player already has
        available_companions = [c for c in companions if c["name"] not in [pc["name"] for pc in self.player["companions"]]]
        
        if not available_companions:
            return False
            
        companion = random.choice(available_companions)
        
        self.print_colored(f"\nYou encounter {companion['name']}!", Fore.CYAN)
        self.print_colored(f"{companion['name']} offers to join your journey.", Fore.WHITE)
        self.print_colored(f"Ability: {companion['ability']}", Fore.YELLOW)
        
        choice = input("\nAccept their help? (y/n): ").lower()
        
        if choice == 'y':
            self.add_companion(companion)
            return True
        else:
            self.print_colored(f"You decide to continue alone. {companion['name']} wishes you luck.", Fore.WHITE)
            return False
            
    def present_branching_path(self):
        """Present the player with a choice of paths"""
        # Only present branching paths occasionally
        if self.player["level"] % 5 != 0:
            return False
            
        self.print_colored("\n=== BRANCHING PATH ===", Fore.MAGENTA)
        self.print_colored("The path splits before you. Which way will you go?", Fore.WHITE)
        
        # Generate path options
        paths = []
        
        # Always include one standard path
        paths.append({
            "name": "Standard Path",
            "description": "A balanced challenge awaits.",
            "challenge_type": random.choice(["luck", "skill", "mixed"]),
            "difficulty_mod": 0,
            "reward_chance": 0.3
        })
        
        # Add a harder path with better rewards
        paths.append({
            "name": "Treacherous Path",
            "description": "A difficult challenge with greater rewards.",
            "challenge_type": random.choice(["luck", "skill", "mixed"]),
            "difficulty_mod": 2,
            "reward_chance": 0.6
        })
        
        # Add an easier path with worse rewards
        paths.append({
            "name": "Safe Path",
            "description": "An easier challenge with fewer rewards.",
            "challenge_type": random.choice(["luck", "skill", "mixed"]),
            "difficulty_mod": -1,
            "reward_chance": 0.1
        })
        
        # Add a special path occasionally
        if random.random() < 0.3:
            special_paths = [
                {
                    "name": "Mysterious Portal",
                    "description": "Who knows where this leads?",
                    "challenge_type": "legendary",
                    "difficulty_mod": 1,
                    "reward_chance": 0.5
                },
                {
                    "name": "Companion's Trail",
                    "description": "You might find a new ally here.",
                    "challenge_type": random.choice(["luck", "skill", "mixed"]),
                    "difficulty_mod": 0,
                    "reward_chance": 0.2,
                    "companion_chance": 0.8
                },
                {
                    "name": "Ancient Shrine",
                    "description": "A place of power that might grant blessings or curses.",
                    "challenge_type": "luck",
                    "difficulty_mod": 0,
                    "reward_chance": 0.4,
                    "buff_chance": 0.6,
                    "debuff_chance": 0.3
                }
            ]
            paths.append(random.choice(special_paths))
            
        # Display path options
        for i, path in enumerate(paths):
            self.print_colored(f"{i+1}. {path['name']}", Fore.YELLOW)
            self.print_colored(f"   {path['description']}", Fore.WHITE)
            
        # Get player choice
        choice = input("\nWhich path will you take? (1-3): ")
        try:
            path_idx = int(choice) - 1
            if 0 <= path_idx < len(paths):
                chosen_path = paths[path_idx]
                self.print_colored(f"\nYou take the {chosen_path['name']}.", Fore.CYAN)
                
                # Handle special path effects
                if "companion_chance" in chosen_path and random.random() < chosen_path["companion_chance"]:
                    self.encounter_companion()
                    
                if "buff_chance" in chosen_path and random.random() < chosen_path["buff_chance"]:
                    buff_types = ["luck", "skill", "mixed", "all"]
                    buff_type = random.choice(buff_types)
                    self.add_buff(f"Shrine Blessing", buff_type, random.randint(1, 2), random.randint(2, 5))
                    
                if "debuff_chance" in chosen_path and random.random() < chosen_path["debuff_chance"]:
                    debuff_types = ["luck", "skill", "mixed", "all"]
                    debuff_type = random.choice(debuff_types)
                    self.add_debuff(f"Shrine Curse", debuff_type, -random.randint(1, 2), random.randint(1, 3))
                    
                return chosen_path
            else:
                self.print_colored("Invalid choice. Taking the standard path.", Fore.RED)
                return paths[0]
        except ValueError:
            self.print_colored("Invalid choice. Taking the standard path.", Fore.RED)
            return paths[0]
    def create_character(self):
        """Create a new character"""
        self.print_colored("=== Character Creation ===", Fore.CYAN)
        self.player["name"] = input("Enter your adventurer's name: ")
        
        # Character class selection
        self.print_colored("\nChoose your character class:", Fore.CYAN)
        classes = [
            {"name": "Lucky Gambler", "description": "Born under a lucky star, you have a natural affinity for games of chance.", 
             "skills": {"luck": 3, "strength": 1, "agility": 1, "wisdom": 1}},
            {"name": "Mighty Warrior", "description": "Trained in the art of combat, your physical prowess is unmatched.", 
             "skills": {"luck": 1, "strength": 3, "agility": 1, "wisdom": 1}},
            {"name": "Swift Acrobat", "description": "Your nimble movements and quick reflexes keep you one step ahead.", 
             "skills": {"luck": 1, "strength": 1, "agility": 3, "wisdom": 1}},
            {"name": "Wise Sage", "description": "Years of study have granted you knowledge beyond your years.", 
             "skills": {"luck": 1, "strength": 1, "agility": 1, "wisdom": 3}},
            {"name": "Balanced Adventurer", "description": "A jack of all trades, you prefer a balanced approach to challenges.", 
             "skills": {"luck": 2, "strength": 2, "agility": 1, "wisdom": 1}}
        ]
        
        for i, char_class in enumerate(classes):
            self.print_colored(f"{i+1}. {char_class['name']}", Fore.YELLOW)
            self.print_colored(f"   {char_class['description']}", Fore.WHITE)
            skill_str = ", ".join([f"{skill.capitalize()}: {value}" for skill, value in char_class['skills'].items()])
            self.print_colored(f"   Skills: {skill_str}", Fore.CYAN)
            print()
            
        while True:
            choice = input("Select your class (1-5): ")
            try:
                class_idx = int(choice) - 1
                if 0 <= class_idx < len(classes):
                    selected_class = classes[class_idx]
                    self.player["class"] = selected_class["name"]
                    self.player["skills"] = selected_class["skills"].copy()
                    break
                else:
                    self.print_colored("Invalid choice!", Fore.RED)
            except ValueError:
                self.print_colored("Please enter a number!", Fore.RED)
        
        self.print_colored(f"\nYou have chosen the {self.player['class']} class!", Fore.GREEN)
        
        # Additional skill points
        points = 3
        self.print_colored(f"\nYou have {points} additional skill points to distribute:", Fore.CYAN)
        
        while points > 0:
            self.print_colored(f"Points remaining: {points}", Fore.YELLOW)
            for i, skill in enumerate(self.player["skills"].keys()):
                print(f"{i+1}. {skill.capitalize()}: {self.player['skills'][skill]}")
            
            choice = input("\nWhich skill to improve? (1-4): ")
            try:
                skill_idx = int(choice) - 1
                skills = list(self.player["skills"].keys())
                if 0 <= skill_idx < len(skills):
                    self.player["skills"][skills[skill_idx]] += 1
                    points -= 1
                else:
                    self.print_colored("Invalid choice!", Fore.RED)
            except ValueError:
                self.print_colored("Please enter a number!", Fore.RED)
        
        self.print_colored(f"\nCharacter created! Welcome, {self.player['name']} the {self.player['class']}!", Fore.GREEN)
        
    def choose_color_theme(self):
        """Allow player to choose a color theme"""
        self.clear_screen()
        # Use current theme for the screen title and initial prompts
        current_theme_colors = self.colors[self.player["color_theme"]]
        self.print_colored("=== COLOR THEME SELECTION ===", current_theme_colors["title"])
        self.print_colored("Choose your preferred color theme:", current_theme_colors["info"])
        
        themes = list(self.colors.keys())
        for i, theme_name in enumerate(themes):
            # Display each theme name using its own title color for a preview
            self.print_colored(f"{i+1}. {theme_name.capitalize()}", self.colors[theme_name]["title"])
            
        while True:
            # The input prompt should also be themed using the current theme
            prompt_text = f"\nSelect a theme (1-{len(themes)}): "
            choice = input(f"{current_theme_colors['info']}{prompt_text}{Style.RESET_ALL}")
            
            try:
                theme_idx = int(choice) - 1
                if 0 <= theme_idx < len(themes):
                    selected_theme_name = themes[theme_idx]
                    self.player["color_theme"] = selected_theme_name
                    # Confirmation message should use the NEWLY selected theme's success color
                    self.print_colored(f"\nYou've selected the {selected_theme_name.capitalize()} theme!", 
                                      self.colors[selected_theme_name]["success"])
                    self.play_sound("success")
                    break
                else:
                    self.print_colored("Invalid choice!", current_theme_colors["failure"])
            except ValueError:
                self.print_colored("Please enter a number!", current_theme_colors["failure"])
                
        time.sleep(1) # Pause to let the user see the confirmation
        
    def check_for_achievement(self, achievement_type, value=None):
        """Check if player has earned an achievement"""
        achievements = {
            "level": [
                {"id": "novice", "name": "Novice Climber", "description": "Reach floor 10", "threshold": 10},
                {"id": "apprentice", "name": "Apprentice Climber", "description": "Reach floor 25", "threshold": 25},
                {"id": "adept", "name": "Adept Climber", "description": "Reach floor 50", "threshold": 50},
                {"id": "master", "name": "Master Climber", "description": "Reach floor 75", "threshold": 75},
                {"id": "grandmaster", "name": "Grandmaster Climber", "description": "Reach floor 100", "threshold": 100}
            ],
            "skill": [
                {"id": "lucky", "name": "Child of Fortune", "description": "Reach 10 Luck", "skill": "luck", "threshold": 10},
                {"id": "strong", "name": "Herculean Strength", "description": "Reach 10 Strength", "skill": "strength", "threshold": 10},
                {"id": "agile", "name": "Lightning Reflexes", "description": "Reach 10 Agility", "skill": "agility", "threshold": 10},
                {"id": "wise", "name": "Sage's Wisdom", "description": "Reach 10 Wisdom", "skill": "wisdom", "threshold": 10}
            ],
            "companions": [
                {"id": "friend", "name": "Friendly Face", "description": "Recruit your first companion", "threshold": 1},
                {"id": "party", "name": "Party Leader", "description": "Recruit 3 companions", "threshold": 3}
            ],
            "boss": [
                {"id": "boss_slayer", "name": "Boss Slayer", "description": "Defeat your first boss", "threshold": 1},
                {"id": "boss_master", "name": "Boss Master", "description": "Defeat 5 bosses", "threshold": 5}
            ],
            "hidden": [
                {"id": "explorer", "name": "Explorer", "description": "Discover your first hidden floor", "threshold": 1},
                {"id": "treasure_hunter", "name": "Treasure Hunter", "description": "Discover 3 hidden floors", "threshold": 3}
            ]
        }
        
        # Check for achievements based on type
        if achievement_type == "level" and value is None:
            value = self.player["level"]
            for achievement in achievements["level"]:
                if value >= achievement["threshold"] and achievement["id"] not in [a["id"] for a in self.player["achievements"]]:
                    self.award_achievement(achievement)
                    
        elif achievement_type == "skill" and value is not None:
            skill, skill_value = value
            for achievement in achievements["skill"]:
                if achievement["skill"] == skill and skill_value >= achievement["threshold"] and achievement["id"] not in [a["id"] for a in self.player["achievements"]]:
                    self.award_achievement(achievement)
                    
        elif achievement_type == "companions" and value is None:
            value = len(self.player["companions"])
            for achievement in achievements["companions"]:
                if value >= achievement["threshold"] and achievement["id"] not in [a["id"] for a in self.player["achievements"]]:
                    self.award_achievement(achievement)
                    
        elif achievement_type == "boss" and value is None:
            value = len(self.player["bosses_defeated"])
            for achievement in achievements["boss"]:
                if value >= achievement["threshold"] and achievement["id"] not in [a["id"] for a in self.player["achievements"]]:
                    self.award_achievement(achievement)
                    
        elif achievement_type == "hidden" and value is None:
            value = len(self.player["hidden_floors_found"])
            for achievement in achievements["hidden"]:
                if value >= achievement["threshold"] and achievement["id"] not in [a["id"] for a in self.player["achievements"]]:
                    self.award_achievement(achievement)
                    
    def award_achievement(self, achievement):
        """Award an achievement to the player"""
        self.player["achievements"].append(achievement)
        
        # Display achievement notification with animation
        self.clear_screen()
        self.print_ascii_art("achievement", self.colors[self.player["color_theme"]]["warning"])
        
        self.animate_text(f"Achievement Unlocked: {achievement['name']}", 
                         self.colors[self.player["color_theme"]]["warning"])
        self.animate_text(achievement['description'], 
                         self.colors[self.player["color_theme"]]["info"])
        
        # Award bonus for achievement
        self.print_colored("\nYou've earned a small bonus for this achievement!", 
                          self.colors[self.player["color_theme"]]["success"])
        skill = random.choice(list(self.player["skills"].keys()))
        self.player["skills"][skill] += 1
        self.print_colored(f"Your {skill} has increased by 1!", 
                          self.colors[self.player["color_theme"]]["highlight"])
        
        # Play sound effect if available
        print("\a")  # Terminal bell
        
        time.sleep(2)
        
    def show_achievements(self):
        """Display the player's achievements"""
        if not self.player["achievements"]:
            self.print_colored("You haven't earned any achievements yet.", Fore.WHITE)
            return
            
        self.print_colored("\n=== ACHIEVEMENTS ===", Fore.YELLOW)
        for achievement in self.player["achievements"]:
            self.print_colored(f"- {achievement['name']}: {achievement['description']}", Fore.WHITE)
            
    def check_for_hidden_floor(self):
        """Check if player has discovered a hidden floor"""
        # Load hidden floor frequency from config
        config = self.load_config()
        hidden_floor_frequency = config["challenge_settings"]["hidden_floor_frequency"]
        
        # Only check on floors based on the configured frequency
        if self.player["level"] % hidden_floor_frequency != 0 or self.player["level"] in self.player["hidden_floors_found"]:
            return False
            
        # Wisdom affects chance of finding hidden floors
        wisdom_bonus = self.player["skills"]["wisdom"] * 0.05
        if random.random() < (0.2 + wisdom_bonus):
            self.clear_screen()
            self.print_ascii_art("hidden", self.colors[self.player["color_theme"]]["highlight"])
            
            self.animate_text("You notice a concealed passage that seems to lead to a secret area!", 
                             self.colors[self.player["color_theme"]]["highlight"])
            choice = input("Do you want to explore it? (y/n): ").lower()
            
            if choice == 'y':
                self.player["hidden_floors_found"].append(self.player["level"])
                self.stats["hidden_floors"] += 1
                self.run_hidden_floor()
                self.check_for_achievement("hidden")
                return True
                
        return False
        
    def run_hidden_floor(self):
        """Run a special challenge on a hidden floor"""
        hidden_challenges = [
            {"name": "Ancient Library", "description": "A vast collection of forgotten knowledge"},
            {"name": "Crystal Garden", "description": "A beautiful garden of crystalline plants"},
            {"name": "Ethereal Pond", "description": "A pool of shimmering, magical water"},
            {"name": "Starlight Chamber", "description": "A room where the ceiling shows the night sky"},
            {"name": "Whispering Gallery", "description": "A circular room where whispers echo endlessly"}
        ]
        
        challenge = random.choice(hidden_challenges)
        
        self.print_colored(f"\n=== {challenge['name']} ===", Fore.MAGENTA)
        self.print_colored(challenge["description"], Fore.WHITE)
        self.print_colored("\nThis hidden floor contains special rewards!", Fore.YELLOW)
        
        # Always give a reward on hidden floors
        self.give_reward(True)  # Force a reward
        
        # Chance for additional bonuses
        if random.random() < 0.5:
            buff_types = ["luck", "skill", "mixed", "all"]
            buff_type = random.choice(buff_types)
            self.add_buff(f"Hidden Blessing", buff_type, 2, random.randint(3, 6))
            
        # Chance to find a companion
        if random.random() < 0.3 and len(self.player["companions"]) < 3:
            self.encounter_companion()
            
    def check_for_boss_floor(self):
        """Check if the current floor has a boss challenge"""
        # Load boss frequency from config
        config = self.load_config()
        boss_frequency = config["challenge_settings"]["boss_frequency"]
        
        # Boss floors are based on the configured frequency
        if self.player["level"] % boss_frequency == 0 and self.player["level"] not in self.player["bosses_defeated"]:
            return True
        return False
        
    def run_boss_challenge(self):
        """Run a boss challenge"""
        boss_level = self.player["level"] // 10
        
        bosses = [
            {"name": "Guardian of the Gate", "description": "A massive stone golem that guards the tower's entrance"},
            {"name": "The Riddlemaster", "description": "A mysterious figure who tests your mind with impossible riddles"},
            {"name": "Chronos the Time Keeper", "description": "A being who can manipulate the flow of time itself"},
            {"name": "Shadow Weaver", "description": "A creature made of living darkness that can take any form"},
            {"name": "The Architect", "description": "The creator of the tower, testing if you are worthy to continue"},
            {"name": "Elemental Fury", "description": "A being composed of all four elements in perfect harmony"},
            {"name": "Mind Flayer", "description": "A psychic entity that attacks your thoughts directly"},
            {"name": "The Void Walker", "description": "A creature from beyond reality that defies understanding"},
            {"name": "Fate's Hand", "description": "The embodiment of destiny itself, challenging your right to choose your path"},
            {"name": "The Ascended One", "description": "A previous climber who reached the top and became something more"}
        ]
        
        # Select boss based on level
        boss_idx = min(boss_level - 1, len(bosses) - 1)
        boss = bosses[boss_idx]
        
        # Dramatic boss introduction with animation
        self.clear_screen()
        self.print_ascii_art("boss", self.colors[self.player["color_theme"]]["failure"])
        
        self.animate_text(f"BOSS CHALLENGE: {boss['name']}", 
                         self.colors[self.player["color_theme"]]["failure"], 0.05)
        self.animate_text(boss["description"], 
                         self.colors[self.player["color_theme"]]["info"], 0.02)
        self.animate_text("\nThis powerful entity blocks your path! You must defeat it to continue.", 
                         self.colors[self.player["color_theme"]]["warning"], 0.02)
        
        # Update stats
        self.stats["bosses_faced"] += 1
        
        # Boss challenges are multi-stage
        stages_completed = 0
        stages_needed = 3
        
        self.print_colored("\nThe boss challenge has multiple stages. You must complete most of them to succeed.", 
                          self.colors[self.player["color_theme"]]["highlight"])
        
        input("\nPress Enter to begin the challenge...")
        
        # Stage 1: Skill challenge
        self.clear_screen()
        self.print_colored("\n=== STAGE 1: SKILL TEST ===", 
                          self.colors[self.player["color_theme"]]["skill"])
        skill_result = self.run_skill_challenge(random.choice(self.challenges["skill"]), 0)
        if skill_result:
            stages_completed += 1
            self.print_colored("You passed the skill test!", 
                              self.colors[self.player["color_theme"]]["success"])
        else:
            self.print_colored("You failed the skill test!", 
                              self.colors[self.player["color_theme"]]["failure"])
            
        input("\nPress Enter to continue...")
            
        # Stage 2: Luck challenge
        self.clear_screen()
        self.print_colored("\n=== STAGE 2: LUCK TEST ===", 
                          self.colors[self.player["color_theme"]]["luck"])
        luck_result = self.run_luck_challenge(random.choice(self.challenges["luck"]), 0)
        if luck_result:
            stages_completed += 1
            self.print_colored("You passed the luck test!", 
                              self.colors[self.player["color_theme"]]["success"])
        else:
            self.print_colored("You failed the luck test!", 
                              self.colors[self.player["color_theme"]]["failure"])
            
        input("\nPress Enter to continue...")
            
        # Stage 3: Mixed challenge
        self.clear_screen()
        self.print_colored("\n=== STAGE 3: COMBINED TEST ===", 
                          self.colors[self.player["color_theme"]]["mixed"])
        mixed_result = self.run_mixed_challenge(random.choice(self.challenges["mixed"]), 0)
        if mixed_result:
            stages_completed += 1
            self.print_colored("You passed the combined test!", 
                              self.colors[self.player["color_theme"]]["success"])
        else:
            self.print_colored("You failed the combined test!", 
                              self.colors[self.player["color_theme"]]["failure"])
            
        input("\nPress Enter to see the results...")
        self.clear_screen()
            
        # Final result
        if stages_completed >= stages_needed:
            self.print_colored(f"\nYou completed {stages_completed} of {stages_needed} stages!", 
                              self.colors[self.player["color_theme"]]["success"])
            self.animate_text(f"\nYou have defeated {boss['name']}!", 
                             self.colors[self.player["color_theme"]]["success"], 0.05)
            
            # Record boss defeat
            self.player["bosses_defeated"].append(self.player["level"])
            
            # Check for achievement
            self.check_for_achievement("boss")
            
            # Special reward for defeating a boss
            self.print_colored("\nYou receive a special reward for defeating the boss!", 
                              self.colors[self.player["color_theme"]]["warning"])
            self.give_reward(True)  # Force a reward
            
            # Chance for a powerful buff
            if random.random() < 0.7:
                self.add_buff("Boss Slayer", "all", 2, 5)
                
            return True
        else:
            self.print_colored(f"\nYou only completed {stages_completed} of {stages_needed} stages.", 
                              self.colors[self.player["color_theme"]]["failure"])
            self.animate_text(f"\nYou have been defeated by {boss['name']}!", 
                             self.colors[self.player["color_theme"]]["failure"], 0.05)
            
            # Debuff from boss defeat
            self.add_debuff("Boss's Curse", "all", -1, 3)
            
            return False
            
    def run_mini_game(self):
        """Run a mini-game for variety"""
        # Load mini-game chance from config
        config = self.load_config()
        mini_game_chance = config["challenge_settings"]["mini_game_chance"]
        
        mini_games = [
            {"name": "Word Scramble", "function": self.mini_game_word_scramble},
            {"name": "Number Guess", "function": self.mini_game_number_guess},
            {"name": "Rock Paper Scissors", "function": self.mini_game_rock_paper_scissors},
            {"name": "Simon Says", "function": self.mini_game_simon_says}
        ]
        
        mini_game = random.choice(mini_games)
        
        self.clear_screen()
        self.print_colored(f"\n=== MINI-GAME: {mini_game['name']} ===", 
                          self.colors[self.player["color_theme"]]["title"])
        
        self.stats["mini_games_played"] += 1
        result = mini_game["function"]()
        
        if result:
            self.print_colored("\nYou won the mini-game!", 
                              self.colors[self.player["color_theme"]]["success"])
            self.play_sound("success")
            self.stats["mini_games_won"] += 1
            
            # Small reward for winning mini-games
            skill = random.choice(list(self.player["skills"].keys()))
            self.player["skills"][skill] += 1
            self.print_colored(f"Your {skill} has increased by 1!", 
                              self.colors[self.player["color_theme"]]["highlight"])
        else:
            self.print_colored("\nYou lost the mini-game!", 
                              self.colors[self.player["color_theme"]]["failure"])
            self.play_sound("failure")
            
        input("\nPress Enter to continue...")
        return result
        
    def mini_game_word_scramble(self):
        """Word scramble mini-game"""
        words = ["tower", "chance", "adventure", "challenge", "destiny", "fortune", "journey", "quest", "skill", "luck"]
        word = random.choice(words)
        
        # Scramble the word
        letters = list(word)
        random.shuffle(letters)
        scrambled = ''.join(letters)
        
        self.print_colored("Unscramble the following word:", Fore.YELLOW)
        self.print_colored(scrambled, Fore.WHITE)
        
        # Wisdom affects time limit
        time_limit = 20 - (self.player["skills"]["wisdom"] - 1)
        time_limit = max(10, time_limit)  # Minimum 10 seconds
        
        self.print_colored(f"You have {time_limit} seconds to answer.", Fore.YELLOW)
        
        start_time = time.time()
        guess = input("Your answer: ").lower().strip()
        end_time = time.time()
        
        if guess == word and (end_time - start_time) <= time_limit:
            return True
        else:
            self.print_colored(f"The correct answer was: {word}", Fore.RED)
            return False
            
    def mini_game_number_guess(self):
        """Number guessing mini-game"""
        # Luck affects range
        max_number = 20 - (self.player["skills"]["luck"] - 1)
        max_number = max(10, max_number)  # Minimum 10
        
        number = random.randint(1, max_number)
        
        self.print_colored(f"I'm thinking of a number between 1 and {max_number}.", Fore.YELLOW)
        self.print_colored("You have 3 guesses.", Fore.YELLOW)
        
        for i in range(3):
            try:
                guess = int(input(f"Guess {i+1}: "))
                
                if guess == number:
                    return True
                elif guess < number:
                    self.print_colored("Too low!", Fore.BLUE)
                else:
                    self.print_colored("Too high!", Fore.RED)
            except ValueError:
                self.print_colored("Please enter a valid number!", Fore.RED)
                
        self.print_colored(f"The number was {number}.", Fore.RED)
        return False
        
    def mini_game_rock_paper_scissors(self):
        """Rock Paper Scissors mini-game"""
        self.print_colored("Best of 3 rounds of Rock, Paper, Scissors!", Fore.YELLOW)
        
        choices = ["rock", "paper", "scissors"]
        player_wins = 0
        computer_wins = 0
        
        while player_wins < 2 and computer_wins < 2:
            self.print_colored(f"\nScore: You {player_wins} - {computer_wins} Computer", Fore.CYAN)
            
            player_choice = input("Choose rock, paper, or scissors (r/p/s): ").lower()
            if player_choice.startswith('r'):
                player_choice = "rock"
            elif player_choice.startswith('p'):
                player_choice = "paper"
            elif player_choice.startswith('s'):
                player_choice = "scissors"
            else:
                self.print_colored("Invalid choice! Please choose r, p, or s.", Fore.RED)
                continue
                
            computer_choice = random.choice(choices)
            
            self.print_colored(f"You chose {player_choice}.", Fore.YELLOW)
            self.print_colored(f"Computer chose {computer_choice}.", Fore.YELLOW)
            
            if player_choice == computer_choice:
                self.print_colored("It's a tie!", Fore.WHITE)
            elif (player_choice == "rock" and computer_choice == "scissors") or \
                 (player_choice == "paper" and computer_choice == "rock") or \
                 (player_choice == "scissors" and computer_choice == "paper"):
                self.print_colored("You win this round!", Fore.GREEN)
                player_wins += 1
            else:
                self.print_colored("Computer wins this round!", Fore.RED)
                computer_wins += 1
                
        return player_wins > computer_wins
        
    def mini_game_simon_says(self):
        """Simon Says memory mini-game"""
        self.print_colored("Remember the sequence!", Fore.YELLOW)
        
        # Agility affects sequence length
        sequence_length = 4 + (self.player["skills"]["agility"] // 3)
        
        colors = ["red", "green", "blue", "yellow"]
        sequence = [random.choice(colors) for _ in range(sequence_length)]
        
        # Show sequence
        for color in sequence:
            self.print_colored(f"Simon says: {color.upper()}", Fore.YELLOW)
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(0.5)
            
        # Get player's sequence
        self.print_colored("Enter the sequence (space-separated colors):", Fore.CYAN)
        player_sequence = input().lower().split()
        
        return player_sequence == sequence
    # Removed duplicated choose_color_theme method. The version at line 999 is kept.
    def show_progress_visualization(self):
        """Show a visual representation of the player's progress"""
        self.clear_screen()
        self.print_colored("=== YOUR JOURNEY SO FAR ===", 
                          self.colors[self.player["color_theme"]]["title"])
        
        # Create a progress bar for tower climbing
        progress = self.player["max_level"] / self.tower_height
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        self.print_colored(f"Tower Progress: {self.player['max_level']}/{self.tower_height}", 
                          self.colors[self.player["color_theme"]]["highlight"])
        self.print_colored(f"[{bar}] {progress:.1%}", 
                          self.colors[self.player["color_theme"]]["info"])
        
        # Show challenge statistics
        if self.stats["challenges_completed"] > 0:
            total_challenges = self.stats["challenges_completed"] + self.stats["challenges_failed"]
            success_rate = self.stats["challenges_completed"] / total_challenges if total_challenges > 0 else 0
            
            self.print_colored("\n=== CHALLENGE STATISTICS ===", 
                              self.colors[self.player["color_theme"]]["title"])
            self.print_colored(f"Challenges Completed: {self.stats['challenges_completed']}", 
                              self.colors[self.player["color_theme"]]["success"])
            self.print_colored(f"Challenges Failed: {self.stats['challenges_failed']}", 
                              self.colors[self.player["color_theme"]]["failure"])
            self.print_colored(f"Success Rate: {success_rate:.1%}", 
                              self.colors[self.player["color_theme"]]["info"])
            
            # Challenge type breakdown
            self.print_colored("\nChallenge Types:", 
                              self.colors[self.player["color_theme"]]["highlight"])
            self.print_colored(f"Luck: {self.stats['luck_challenges']}", 
                              self.colors[self.player["color_theme"]]["luck"])
            self.print_colored(f"Skill: {self.stats['skill_challenges']}", 
                              self.colors[self.player["color_theme"]]["skill"])
            self.print_colored(f"Mixed: {self.stats['mixed_challenges']}", 
                              self.colors[self.player["color_theme"]]["mixed"])
            self.print_colored(f"Legendary: {self.stats['legendary_challenges']}", 
                              self.colors[self.player["color_theme"]]["legendary"])
            
        # Show special discoveries
        self.print_colored("\n=== SPECIAL DISCOVERIES ===", 
                          self.colors[self.player["color_theme"]]["title"])
        self.print_colored(f"Hidden Floors Found: {len(self.player['hidden_floors_found'])}/{self.tower_height//7}", 
                          self.colors[self.player["color_theme"]]["highlight"])
        self.print_colored(f"Bosses Defeated: {len(self.player['bosses_defeated'])}/{self.tower_height//10}", 
                          self.colors[self.player["color_theme"]]["warning"])
        self.print_colored(f"Companions Met: {self.stats['companions_met']}", 
                          self.colors[self.player["color_theme"]]["info"])
        self.print_colored(f"Rewards Found: {self.stats['rewards_found']}", 
                          self.colors[self.player["color_theme"]]["success"])
        
        # Mini-game statistics
        if self.stats["mini_games_played"] > 0:
            mini_game_win_rate = self.stats["mini_games_won"] / self.stats["mini_games_played"]
            self.print_colored(f"Mini-Games Played: {self.stats['mini_games_played']}", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored(f"Mini-Games Won: {self.stats['mini_games_won']}", 
                              self.colors[self.player["color_theme"]]["success"])
            self.print_colored(f"Mini-Game Win Rate: {mini_game_win_rate:.1%}", 
                              self.colors[self.player["color_theme"]]["highlight"])
            
        input("\nPress Enter to continue...")
    def load_config(self):
        """Load game configuration from file"""
        try:
            with open("tower_config.json", "r") as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            # Create default config if not found
            default_config = {
                "game_settings": {
                    "tower_height": 100,
                    "auto_save": True,
                    "sound_effects": True,
                    "default_color_theme": "default",
                    "animation_speed": 0.03,
                    "difficulty": "normal"
                },
                "challenge_settings": {
                    "luck_challenge_weight": 1.0,
                    "skill_challenge_weight": 1.0,
                    "mixed_challenge_weight": 1.0,
                    "legendary_challenge_weight": 0.5,
                    "boss_frequency": 10,
                    "hidden_floor_frequency": 7,
                    "mini_game_chance": 0.15
                },
                "reward_settings": {
                    "basic_reward_chance": 0.3,
                    "advanced_reward_threshold": 20,
                    "legendary_reward_threshold": 40,
                    "boss_reward_guaranteed": True
                },
                "companion_settings": {
                    "max_companions": 3,
                    "encounter_chance": 0.1
                },
                "environment_settings": {
                    "weather_change_frequency": 3,
                    "day_night_cycle_frequency": 5
                }
            }
            
            with open("tower_config.json", "w") as f:
                json.dump(default_config, f, indent=2)
                
            return default_config
            
    def save_config(self, config):
        """Save game configuration to file"""
        with open("tower_config.json", "w") as f:
            json.dump(config, f, indent=2)
            
    def play_sound(self, sound_type):
        """Play a sound effect if enabled"""
        config = self.load_config()
        if config["game_settings"]["sound_effects"]:
            if sound_type == "achievement":
                print("\a")  # Terminal bell
                time.sleep(0.2)
                print("\a")  # Double bell for achievements
            elif sound_type == "success":
                print("\a")  # Terminal bell
            elif sound_type == "failure":
                time.sleep(0.1)
                print("\a")
                time.sleep(0.1)
                print("\a")
            elif sound_type == "boss":
                for _ in range(3):
                    print("\a")
                    time.sleep(0.2)
                    
    def auto_save(self):
        """Automatically save the game if enabled"""
        config = self.load_config()
        if config["game_settings"]["auto_save"]:
            self.save_game(silent=True)
            
    def edit_settings(self):
        """Edit game settings"""
        config = self.load_config()
        
        while True:
            self.clear_screen()
            self.print_colored("=== GAME SETTINGS ===", 
                              self.colors[self.player["color_theme"]]["title"])
            
            # Display current settings
            self.print_colored("\nGeneral Settings:", 
                              self.colors[self.player["color_theme"]]["highlight"])
            self.print_colored(f"1. Auto-Save: {'Enabled' if config['game_settings']['auto_save'] else 'Disabled'}", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored(f"2. Sound Effects: {'Enabled' if config['game_settings']['sound_effects'] else 'Disabled'}", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored(f"3. Animation Speed: {config['game_settings']['animation_speed']}", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored(f"4. Difficulty: {config['game_settings']['difficulty'].capitalize()}", 
                              self.colors[self.player["color_theme"]]["info"])
            
            self.print_colored("\nChallenge Settings:", 
                              self.colors[self.player["color_theme"]]["highlight"])
            self.print_colored(f"5. Mini-Game Chance: {config['challenge_settings']['mini_game_chance']}", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored(f"6. Boss Frequency: Every {config['challenge_settings']['boss_frequency']} floors", 
                              self.colors[self.player["color_theme"]]["info"])
            self.print_colored(f"7. Hidden Floor Frequency: Every {config['challenge_settings']['hidden_floor_frequency']} floors", 
                              self.colors[self.player["color_theme"]]["info"])
            
            self.print_colored("\n8. Save and Return", 
                              self.colors[self.player["color_theme"]]["success"])
            self.print_colored("9. Return without Saving", 
                              self.colors[self.player["color_theme"]]["failure"])
            
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == "1":
                config["game_settings"]["auto_save"] = not config["game_settings"]["auto_save"]
            elif choice == "2":
                config["game_settings"]["sound_effects"] = not config["game_settings"]["sound_effects"]
            elif choice == "3":
                try:
                    speed = float(input("Enter animation speed (0.01-0.1, lower is faster): "))
                    if 0.01 <= speed <= 0.1:
                        config["game_settings"]["animation_speed"] = speed
                    else:
                        self.print_colored("Invalid speed! Must be between 0.01 and 0.1.", 
                                          self.colors[self.player["color_theme"]]["failure"])
                        input("Press Enter to continue...")
                except ValueError:
                    self.print_colored("Invalid input! Please enter a number.", 
                                      self.colors[self.player["color_theme"]]["failure"])
                    input("Press Enter to continue...")
            elif choice == "4":
                difficulties = ["easy", "normal", "hard"]
                self.print_colored("\nSelect difficulty:", 
                                  self.colors[self.player["color_theme"]]["highlight"])
                for i, diff in enumerate(difficulties):
                    self.print_colored(f"{i+1}. {diff.capitalize()}", 
                                      self.colors[self.player["color_theme"]]["info"])
                    
                diff_choice = input("\nEnter your choice (1-3): ")
                try:
                    diff_idx = int(diff_choice) - 1
                    if 0 <= diff_idx < len(difficulties):
                        config["game_settings"]["difficulty"] = difficulties[diff_idx]
                    else:
                        self.print_colored("Invalid choice!", 
                                          self.colors[self.player["color_theme"]]["failure"])
                        input("Press Enter to continue...")
                except ValueError:
                    self.print_colored("Invalid input! Please enter a number.", 
                                      self.colors[self.player["color_theme"]]["failure"])
                    input("Press Enter to continue...")
            elif choice == "5":
                try:
                    chance = float(input("Enter mini-game chance (0.0-1.0): "))
                    if 0.0 <= chance <= 1.0:
                        config["challenge_settings"]["mini_game_chance"] = chance
                    else:
                        self.print_colored("Invalid chance! Must be between 0.0 and 1.0.", 
                                          self.colors[self.player["color_theme"]]["failure"])
                        input("Press Enter to continue...")
                except ValueError:
                    self.print_colored("Invalid input! Please enter a number.", 
                                      self.colors[self.player["color_theme"]]["failure"])
                    input("Press Enter to continue...")
            elif choice == "6":
                try:
                    frequency = int(input("Enter boss frequency (floors between bosses): "))
                    if frequency > 0:
                        config["challenge_settings"]["boss_frequency"] = frequency
                    else:
                        self.print_colored("Invalid frequency! Must be greater than 0.", 
                                          self.colors[self.player["color_theme"]]["failure"])
                        input("Press Enter to continue...")
                except ValueError:
                    self.print_colored("Invalid input! Please enter a number.", 
                                      self.colors[self.player["color_theme"]]["failure"])
                    input("Press Enter to continue...")
            elif choice == "7":
                try:
                    frequency = int(input("Enter hidden floor frequency (floors between hidden floors): "))
                    if frequency > 0:
                        config["challenge_settings"]["hidden_floor_frequency"] = frequency
                    else:
                        self.print_colored("Invalid frequency! Must be greater than 0.", 
                                          self.colors[self.player["color_theme"]]["failure"])
                        input("Press Enter to continue...")
                except ValueError:
                    self.print_colored("Invalid input! Please enter a number.", 
                                      self.colors[self.player["color_theme"]]["failure"])
                    input("Press Enter to continue...")
            elif choice == "8":
                self.save_config(config)
                self.print_colored("Settings saved successfully!", 
                                  self.colors[self.player["color_theme"]]["success"])
                self.play_sound("success")
                time.sleep(1)
                break
            elif choice == "9":
                self.print_colored("Settings not saved.", 
                                  self.colors[self.player["color_theme"]]["warning"])
                time.sleep(1)
                break
            else:
                self.print_colored("Invalid choice!", 
                                  self.colors[self.player["color_theme"]]["failure"])
                input("Press Enter to continue...")
                
    def challenge_editor(self):
        """Edit challenges"""
        self.clear_screen()
        self.print_colored("=== CHALLENGE EDITOR ===", 
                          self.colors[self.player["color_theme"]]["title"])
        
        # Load current challenges
        challenges = self.load_challenges()
        
        # Display challenge types
        self.print_colored("\nSelect challenge type to edit:", 
                          self.colors[self.player["color_theme"]]["highlight"])
        challenge_types = list(challenges.keys())
        for i, c_type in enumerate(challenge_types):
            self.print_colored(f"{i+1}. {c_type.capitalize()} Challenges", 
                              self.colors[self.player["color_theme"]]["info"])
            
        self.print_colored(f"{len(challenge_types)+1}. Return to Main Menu", 
                          self.colors[self.player["color_theme"]]["warning"])
        
        choice = input("\nEnter your choice: ")
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(challenge_types):
                selected_type = challenge_types[choice_idx]
                self.edit_challenge_type(challenges, selected_type)
            elif choice_idx == len(challenge_types):
                return
            else:
                self.print_colored("Invalid choice!", 
                                  self.colors[self.player["color_theme"]]["failure"])
                input("Press Enter to continue...")
        except ValueError:
            self.print_colored("Invalid input! Please enter a number.", 
                              self.colors[self.player["color_theme"]]["failure"])
            input("Press Enter to continue...")
            
    def edit_challenge_type(self, challenges, challenge_type):
        """Edit challenges of a specific type"""
        while True:
            self.clear_screen()
            self.print_colored(f"=== EDITING {challenge_type.upper()} CHALLENGES ===", 
                              self.colors[self.player["color_theme"]]["title"])
            
            # Display challenges of this type
            for i, challenge in enumerate(challenges[challenge_type]):
                self.print_colored(f"{i+1}. {challenge['name']} (Difficulty: {challenge['difficulty']})", 
                                  self.colors[self.player["color_theme"]]["info"])
                
            self.print_colored(f"\n{len(challenges[challenge_type])+1}. Add New Challenge", 
                              self.colors[self.player["color_theme"]]["success"])
            self.print_colored(f"{len(challenges[challenge_type])+2}. Save and Return", 
                              self.colors[self.player["color_theme"]]["warning"])
            
            choice = input("\nEnter your choice: ")
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(challenges[challenge_type]):
                    # Edit existing challenge
                    self.edit_challenge(challenges, challenge_type, choice_idx)
                elif choice_idx == len(challenges[challenge_type]):
                    # Add new challenge
                    self.add_challenge(challenges, challenge_type)
                elif choice_idx == len(challenges[challenge_type]) + 1:
                    # Save and return
                    self.save_challenges(challenges)
                    break
                else:
                    self.print_colored("Invalid choice!", 
                                      self.colors[self.player["color_theme"]]["failure"])
                    input("Press Enter to continue...")
            except ValueError:
                self.print_colored("Invalid input! Please enter a number.", 
                                  self.colors[self.player["color_theme"]]["failure"])
                input("Press Enter to continue...")
                
    def edit_challenge(self, challenges, challenge_type, challenge_idx):
        """Edit a specific challenge"""
        challenge = challenges[challenge_type][challenge_idx]
        
        self.clear_screen()
        self.print_colored(f"=== EDITING CHALLENGE: {challenge['name']} ===", 
                          self.colors[self.player["color_theme"]]["title"])
        
        # Edit name
        self.print_colored(f"Current name: {challenge['name']}", 
                          self.colors[self.player["color_theme"]]["info"])
        new_name = input("Enter new name (leave blank to keep current): ")
        if new_name:
            challenge['name'] = new_name
            
        # Edit description
        self.print_colored(f"Current description: {challenge['description']}", 
                          self.colors[self.player["color_theme"]]["info"])
        new_desc = input("Enter new description (leave blank to keep current): ")
        if new_desc:
            challenge['description'] = new_desc
            
        # Edit difficulty
        self.print_colored(f"Current difficulty: {challenge['difficulty']}", 
                          self.colors[self.player["color_theme"]]["info"])
        new_diff = input("Enter new difficulty (1-15, leave blank to keep current): ")
        if new_diff:
            try:
                diff = int(new_diff)
                if 1 <= diff <= 15:
                    challenge['difficulty'] = diff
                else:
                    self.print_colored("Invalid difficulty! Must be between 1 and 15.", 
                                      self.colors[self.player["color_theme"]]["failure"])
            except ValueError:
                self.print_colored("Invalid input! Difficulty not changed.", 
                                  self.colors[self.player["color_theme"]]["failure"])
                
        # Update the challenge
        challenges[challenge_type][challenge_idx] = challenge
        self.print_colored("Challenge updated successfully!", 
                          self.colors[self.player["color_theme"]]["success"])
        input("Press Enter to continue...")
        
    def add_challenge(self, challenges, challenge_type):
        """Add a new challenge"""
        self.clear_screen()
        self.print_colored(f"=== ADDING NEW {challenge_type.upper()} CHALLENGE ===", 
                          self.colors[self.player["color_theme"]]["title"])
        
        # Get challenge details
        name = input("Enter challenge name: ")
        if not name:
            self.print_colored("Challenge name cannot be empty!", 
                              self.colors[self.player["color_theme"]]["failure"])
            input("Press Enter to continue...")
            return
            
        description = input("Enter challenge description: ")
        if not description:
            self.print_colored("Challenge description cannot be empty!", 
                              self.colors[self.player["color_theme"]]["failure"])
            input("Press Enter to continue...")
            return
            
        difficulty = input("Enter challenge difficulty (1-15): ")
        try:
            diff = int(difficulty)
            if 1 <= diff <= 15:
                # Create new challenge
                new_challenge = {
                    "name": name,
                    "description": description,
                    "difficulty": diff
                }
                
                # Add to challenges
                challenges[challenge_type].append(new_challenge)
                self.print_colored("Challenge added successfully!", 
                                  self.colors[self.player["color_theme"]]["success"])
                input("Press Enter to continue...")
            else:
                self.print_colored("Invalid difficulty! Must be between 1 and 15.", 
                                  self.colors[self.player["color_theme"]]["failure"])
                input("Press Enter to continue...")
        except ValueError:
            self.print_colored("Invalid input! Please enter a number for difficulty.", 
                              self.colors[self.player["color_theme"]]["failure"])
            input("Press Enter to continue...")
            
    def save_challenges(self, challenges):
        """Save challenges to file"""
        with open("challenges.json", "w") as f:
            json.dump(challenges, f, indent=2)
            
        self.print_colored("Challenges saved successfully!", 
                          self.colors[self.player["color_theme"]]["success"])
        self.play_sound("success")
        
        # Reload challenges
        self.challenges = challenges
    # Removed duplicated start_game method. The version at line 1016 is kept.

if __name__ == "__main__":
    game = TowerOfChance()
    game.start_game()
