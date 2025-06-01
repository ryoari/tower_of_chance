# game_bot.py
import random
import time
import os
import json
import sys
import traceback
import builtins # To patch input and print
from collections import deque, Counter 
import re

# Assuming tower_of_chance.py is in the same directory
from tower_of_chance import TowerOfChance, Fore, Style # Import necessary components

LOG_FILE = "bot_log.txt"
MAX_RECENT_PRINTS = 20 # How many recent print lines to keep for context

class GameTesterBot:
    def __init__(self, game_instance, log_file_path=LOG_FILE):
        self.game = game_instance
        self.log_file = open(log_file_path, "w", encoding="utf-8")
        self.original_input = builtins.input
        self.original_print = builtins.print
        self.recent_prints = deque(maxlen=MAX_RECENT_PRINTS)
        self.unhandled_prompts = []
        self.exceptions_found = 0
        self.current_turn = 0 
        self.turns_to_run_session = 0 
        self.game_loop_quit_choice = "10" 

        self._char_skill_choice_counter = 0
        
        # For Riddle Solver
        self._known_riddles = [
            {"q": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "a": "echo"},
            {"q": "The more you take, the more you leave behind. What am I?", "a": "footsteps"},
            {"q": "What has keys but no locks, space but no room, and you can enter but not go in?", "a": "keyboard"}
        ]

        # For Challenge Editor state
        self.bot_context = "in_game_loop" # "in_game_loop", "challenge_editor"
        self.editor_state = "idle" 
        # "idle", "selecting_type", "selecting_challenge_from_list", 
        # "editing_fields_name", "editing_fields_desc", "editing_fields_diff", 
        # "exiting_current_type_editor"
        self.current_editing_type_key = None # e.g., "luck", "skill"
        self.has_completed_one_edit_cycle_in_editor = False


    def log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] BOT: {message}"
        self.original_print(full_message) 
        self.log_file.write(full_message + "\n")
        self.log_file.flush()

    def _patched_print(self, *args, **kwargs):
        sep = kwargs.get('sep', ' ')
        message = sep.join(map(str, args))
        
        plain_message = re.sub(r'\x1b\[[0-9;]*[mK]', '', message)
        if plain_message.strip(): 
            self.recent_prints.append(plain_message.strip())
            
        self.original_print(*args, **kwargs)

    def _patched_input(self, prompt=""):
        # Strip color codes from the prompt itself for reliable matching
        plain_prompt_for_matching = re.sub(r'\x1b\[[0-9;]*[mK]', '', prompt)
        prompt_strip = plain_prompt_for_matching.strip()
        
        self.log(f"GAME_INPUT_PROMPT (raw): {prompt.strip()}")
        # Log what bot uses for logic, after stripping color codes
        self.log(f"GAME_INPUT_PROMPT (parsed for bot): {prompt_strip}") 
        
        # Add the clean prompt to recent_prints for context parsing
        # This ensures recent_prints contains what the bot "sees" for prompts too.
        if prompt_strip: # Avoid adding empty prompts
            self.recent_prints.append(f"PROMPT: {prompt_strip}")

        response = None
        prompt_lower = prompt_strip.lower()

        # --- Main Game Loop Action ---
        if "enter your choice (1-10):" == prompt_lower: # Exact match for main game loop prompt
            self.current_turn += 1
            self.bot_context = "in_game_loop" 
            if self.editor_state != "idle": # Reset editor state if we are back to main loop
                self.log("BOT: Detected main game loop, resetting editor state.")
                self.editor_state = "idle"
                self.current_editing_type_key = None
                self.has_completed_one_edit_cycle_in_editor = False

            if self.turns_to_run_session > 0 and self.current_turn > self.turns_to_run_session:
                response = self.game_loop_quit_choice
                self.log(f"BOT: MainLoop - Reached max turns ({self.turns_to_run_session}). Quitting with '{response}'.")
            else:
                rand_val = random.random()
                if rand_val < 0.70: # 70% chance to climb
                    response = "1"
                elif rand_val < 0.75: # 5% chance for inventory/stats
                    response = "2"
                elif rand_val < 0.80: # 5% chance for challenge editor
                    response = "8"
                    self.bot_context = "challenge_editor" 
                    self.editor_state = "idle" 
                    self.has_completed_one_edit_cycle_in_editor = False 
                elif rand_val < 0.85: # 5% chance to save
                    response = "9"
                else: # Remaining 15% for other safe options
                    response = random.choice(["3", "4", "5", "6", "7"])
                self.log(f"BOT: MainLoop - Turn {self.current_turn}. Chosen action: '{response}'.")
        
        # --- Challenge Editor Specific Logic ---
        # This block should come BEFORE generic menu navigation
        if response is None and self.bot_context == "challenge_editor":
            self.log(f"BOT: Editor - Current state: {self.editor_state}, Prompt: '{prompt_lower}'")

            if self.editor_state == "idle" and "select challenge type to edit" in prompt_lower:
                if not self.has_completed_one_edit_cycle_in_editor:
                    response = "1" # Select first type
                    try:
                        self.current_editing_type_key = list(self.game.challenges.keys())[0]
                    except IndexError: # Should not happen if challenges exist
                        self.log("BOT: Editor - ERROR! No challenge types found in game.challenges.")
                        self.bot_context = "in_game_loop" # Bail out
                        response = "10" # Try to quit game if editor is broken
                    self.editor_state = "selecting_challenge_from_list"
                    self.log(f"BOT: Editor - State: idle -> selecting_challenge_from_list. Chose type 1 ({self.current_editing_type_key}).")
                else: # We've done an edit cycle, now exit editor
                    num_types = len(self.game.challenges.keys())
                    response = str(num_types + 1) # Option to "Return to Main Menu"
                    self.log(f"BOT: Editor - Attempting to exit editor via option {response}.")
                    self.bot_context = "in_game_loop" # Fully exited editor flow
                    self.editor_state = "idle" 
                    self.has_completed_one_edit_cycle_in_editor = False 

            elif self.editor_state == "selecting_challenge_from_list" and "enter your choice:" == prompt_lower and \
                 self.current_editing_type_key and \
                 any(f"editing {self.current_editing_type_key.lower()} challenges" in p.lower() for p in list(self.recent_prints)[-5:]):
                response = "1" # Select first challenge in the list
                self.editor_state = "editing_fields_name"
                self.log(f"BOT: Editor - State: selecting_challenge_from_list -> editing_fields_name. Chose challenge 1 from type {self.current_editing_type_key}.")

            elif self.editor_state == "editing_fields_name" and "enter new name" in prompt_lower:
                response = f"BotName{random.randint(1,9)}"
                self.editor_state = "editing_fields_desc"
                self.log("BOT: Editor - State: editing_fields_name -> editing_fields_desc.")
            elif self.editor_state == "editing_fields_desc" and "enter new description" in prompt_lower:
                response = "Bot edited description."
                self.editor_state = "editing_fields_diff"
                self.log("BOT: Editor - State: editing_fields_desc -> editing_fields_diff.")
            elif self.editor_state == "editing_fields_diff" and "enter new difficulty" in prompt_lower:
                response = str(random.randint(1, 15))
                self.editor_state = "exiting_current_type_editor" # Next prompt will be "Press Enter", then challenge list
                self.has_completed_one_edit_cycle_in_editor = True 
                self.log("BOT: Editor - State: editing_fields_diff -> exiting_current_type_editor.")

            elif self.editor_state == "exiting_current_type_editor" and "enter your choice:" == prompt_lower and \
                 self.current_editing_type_key and \
                 any(f"editing {self.current_editing_type_key.lower()} challenges" in p.lower() for p in list(self.recent_prints)[-5:]):
                # We are back at the list of challenges for the current type. Choose "Save and Return".
                num_listed_challenges = 0
                relevant_prints_for_menu_count = []
                for p_text_idx in range(len(self.recent_prints) - 2, -1, -1):
                    p_text = self.recent_prints[p_text_idx].lower()
                    if f"editing {self.current_editing_type_key.lower()} challenges" in p_text: break
                    if "press enter to continue" in p_text: continue # Skip this common line
                    relevant_prints_for_menu_count.insert(0, p_text)
                
                for p_text in relevant_prints_for_menu_count:
                    if re.match(r"^\s*\d+\.\s*.+\(difficulty: \d+\)", p_text):
                        num_listed_challenges += 1
                    elif "add new challenge" in p_text: break 
                
                if num_listed_challenges > 0:
                    response = str(num_listed_challenges + 2) 
                    self.log(f"BOT: Editor - Counted {num_listed_challenges} challenges. Trying 'Save and Return' for type with option {response}.")
                else: 
                    response = "3" # Fallback: assumes 1 challenge listed + Add New + Save and Return
                    self.log(f"BOT: Editor - Failed to count challenges for type, guessing 'Save and Return' as option {response}.")
                
                self.editor_state = "idle" 
                self.current_editing_type_key = None 
                # The `has_completed_one_edit_cycle_in_editor` is true, so next "select type" prompt will exit.

        # --- Character Creation ---
        if response is None:
            if "enter your adventurer's name:" in prompt_lower:
                response = f"Bot{random.randint(100,999)}"
                self._char_skill_choice_counter = 0 
            elif "select your class (1-5):" in prompt_lower:
                if not response: 
                    response = str(random.randint(1, 5))
            elif "which skill to improve? (1-4):" in prompt_lower:
                response = str((self._char_skill_choice_counter % 4) + 1)
                self._char_skill_choice_counter += 1

        # --- Riddle Solver ---
        if response is None and "your answer:" == prompt_lower and \
           any("riddle:" in p.lower() for p in list(self.recent_prints)[-4:]): # Check last few prints for "riddle:" context
            riddle_question_text = None
            for i in range(len(self.recent_prints) - 2, -1, -1): 
                text_line = self.recent_prints[i]
                if "riddle:" in text_line.lower():
                    riddle_question_text = text_line.split("Riddle:", 1)[-1].split("riddle:", 1)[-1].strip()
                    break
            
            if riddle_question_text:
                for r_obj in self._known_riddles:
                    if r_obj["q"].lower() == riddle_question_text.lower():
                        response = r_obj["a"]
                        self.log(f"BOT: Riddle - Found answer '{response}' for riddle '{riddle_question_text}'.")
                        break
                if not response:
                    self.log(f"BOT: Riddle - No known answer for riddle: '{riddle_question_text}'. Using fallback.")
                    response = "a guess" 
            else:
                self.log("BOT: Riddle - Could not extract riddle question from recent prints. Using fallback.")
                response = "a guess"

        # --- Other Challenge Specific Inputs (Memory, Scramble, etc.) ---
        if response is None:
            if "heads or tails? (h/t)" in prompt_lower:
                response = random.choice(["h", "t"])
            elif "press enter to" in prompt_lower or \
                 "meditate on the correct order" in prompt_lower:
                response = "" 
            elif "enter the sequence (symbols separated by spaces):" in prompt_lower: 
                parsed_sequence = None
                try:
                    memo_prompt_idx = -1
                    for i in range(len(self.recent_prints) -1, -1, -1):
                        if "memorize this sequence:" in self.recent_prints[i].lower():
                            memo_prompt_idx = i
                            break
                    if memo_prompt_idx != -1 and memo_prompt_idx + 1 < len(self.recent_prints):
                        potential_sequence = self.recent_prints[memo_prompt_idx + 1]
                        if re.match(r'^([★♦♥♠♣▲■●]\s?)+$', potential_sequence.strip()):
                            parsed_sequence = potential_sequence.strip()
                            self.log(f"Bot attempting to use memorized sequence: '{parsed_sequence}'")
                except Exception as e:
                    self.log(f"Error parsing memory sequence: {e}")
                if parsed_sequence: response = parsed_sequence
                else: response = "★ ♦ ♥ ♠"; self.log("Memory sequence parsing failed, using fallback.")

            elif "where is the treasure hidden?" in prompt_lower:
                response = random.choice(["chest", "box", "a chest"])
            elif "choose chest 1, 2, or 3:" in prompt_lower:
                response = str(random.randint(1, 3))
            elif "will you use your wits (w) or speed (s)?" in prompt_lower:
                response = random.choice(["w", "s"])
            elif "which do you choose? (s/w/c):" in prompt_lower: 
                response = random.choice(["s", "w", "c"])

        # --- Yes/No Prompts ---
        if response is None and "(y/n)" in prompt_lower:
            response = random.choice(["y", "n"])

        # --- Mini-Games ---
        if response is None:
            if any("unscramble the following word:" in p.lower() for p in list(self.recent_prints)[-3:]) and "your answer:" in prompt_lower:
                word_to_unscramble = None
                try:
                    unscramble_prompt_idx = -1
                    for i in range(len(self.recent_prints) -1, -1, -1):
                        if "unscramble the following word:" in self.recent_prints[i].lower():
                            unscramble_prompt_idx = i
                            break
                    if unscramble_prompt_idx != -1 and unscramble_prompt_idx + 1 < len(self.recent_prints):
                        potential_word = self.recent_prints[unscramble_prompt_idx + 1].strip()
                        if re.match(r'^[a-zA-Z]+$', potential_word): 
                            word_to_unscramble = potential_word
                except Exception as e:
                    self.log(f"Error parsing scrambled word: {e}")

                if word_to_unscramble:
                    self.log(f"Bot found scrambled word: {word_to_unscramble}")
                    known_words = ["tower", "chance", "adventure", "challenge", "destiny", "fortune", "journey", "quest", "skill", "luck", "player", "level", "floor"]
                    scrambled_counts = Counter(word_to_unscramble.lower())
                    for kw in known_words:
                        if Counter(kw) == scrambled_counts:
                            response = kw
                            self.log(f"Bot attempting to answer with anagram: {response}")
                            break
                if not response: response = "tower" 

            elif "guess " in prompt_lower and ":" in prompt_lower and \
                 any("i'm thinking of a number" in p.lower() for p in list(self.recent_prints)[-5:]): 
                range_match = re.search(r'between 1 and (\d+)', "".join(self.recent_prints).lower())
                max_num_guess = 10 
                if range_match:
                    try: max_num_guess = int(range_match.group(1))
                    except ValueError: self.log(f"Could not parse max number for guessing game, using default {max_num_guess}")
                response = str(random.randint(1, max_num_guess))
            elif "choose rock, paper, or scissors (r/p/s):" in prompt_lower:
                response = random.choice(["r", "p", "s"])
            elif "enter the sequence (space-separated colors):" in prompt_lower and \
                 any("simon says" in p.lower() for p in list(self.recent_prints)[-10:]): 
                response = "red green blue yellow" 

        # --- Settings Editor (Game Settings, not Challenge Editor) ---
        if response is None:
            if "enter animation speed" in prompt_lower:
                response = f"{random.uniform(0.01, 0.05):.2f}"
            elif "enter mini-game chance" in prompt_lower:
                response = f"{random.uniform(0.1, 0.3):.1f}"
            elif "enter boss frequency" in prompt_lower or "enter hidden floor frequency" in prompt_lower:
                response = str(random.randint(5,15))
        
        # --- Generic Menu Navigation (if not handled by more specific logic like editor or main loop) ---
        if response is None:
            if "enter your choice" in prompt_lower or \
               "select a theme" in prompt_lower or \
               "which path will you take" in prompt_lower or \
               "select difficulty" in prompt_lower: # Removed "select challenge type to edit" as it's handled above
                match = re.search(r'\((\d+)-(\d+)\)', prompt_lower)
                if not match and "1-" in prompt_lower: 
                    match_simple = re.search(r'1-(\d+)', prompt_lower)
                    if match_simple:
                        class MockMatch:
                            def __init__(self, g1, g2): self.g1, self.g2 = g1, g2
                            def group(self, i): return self.g1 if i == 1 else self.g2
                        match = MockMatch("1", match_simple.group(1))
                if match:
                    try:
                        min_val, max_val = int(match.group(1)), int(match.group(2))
                        if min_val <= max_val: response = str(random.randint(min_val, max_val))
                    except (ValueError, AttributeError): pass 
                elif "1-3" in prompt_lower: response = str(random.randint(1,3))
                elif "1-4" in prompt_lower: response = str(random.randint(1,4))
                elif "1-5" in prompt_lower: response = str(random.randint(1,5))
                # "1-10" is usually main game loop, handled earlier.

        # --- Fallback for unhandled prompts ---
        if response is None:
            self.log(f"WARNING: Unhandled prompt: '{prompt_strip}'")
            self.unhandled_prompts.append(prompt_strip)
            if "choice" in prompt_lower or "select" in prompt_lower:
                response = "1" # Default to "1" if it seems like a menu
            elif "continue" in prompt_lower:
                 response = "" 
            else:
                response = "" 
            self.log(f"BOT: Fallback response '{response}' for unhandled prompt.")

        self.log(f"BOT_RESPONSE: '{response}' for prompt '{prompt_strip}'")
        return response

    def _setup_patches(self):
        builtins.input = self._patched_input
        builtins.print = self._patched_print

    def _restore_patches(self):
        builtins.input = self.original_input
        builtins.print = self.original_print

    def run_test_session(self, num_turns=0): # Default num_turns to 0 for "all levels"
        self._setup_patches()
        if num_turns == 0:
            self.log("Starting test session to go through all levels (or until game ends).")
            self.turns_to_run_session = float('inf') # Effectively infinite for this purpose
        else:
            self.log(f"Starting test session for {num_turns} turns.")
            self.turns_to_run_session = num_turns
            
        self.current_turn = 0 
        self.unhandled_prompts = []
        self.exceptions_found = 0
        self._char_skill_choice_counter = 0 
        
        self.bot_context = "in_game_loop"
        self.editor_state = "idle"
        self.current_editing_type_key = None
        self.has_completed_one_edit_cycle_in_editor = False


        try:
            self.log("Attempting to start game via self.game.start_game().")
            self.game.start_game() 

            # Post-game execution checks
            if self.game.player and self.game.player.get("name"):
                self.log(f"Player '{self.game.player['name']}' was active during the session.")
                self.log(f"Character final state: Level {self.game.player.get('level')}, Skills {self.game.player.get('skills')}")
            elif self.current_turn == 0 and not self.unhandled_prompts and self.exceptions_found == 0:
                self.log("Session ended very early. Bot might have chosen to quit at the initial main menu.")
            else:
                self.log("Player character may not have been fully created or game exited before main loop started.")

            if self.turns_to_run_session != float('inf') and self.current_turn >= self.turns_to_run_session :
                self.log(f"Game session completed the target of {self.turns_to_run_session} turns (actual: {self.current_turn}).")
            elif self.exceptions_found == 0 and self.turns_to_run_session != float('inf'): 
                self.log(f"Game session ended after {self.current_turn} turns (target was {self.turns_to_run_session}). This could be due to game completion, player defeat, or bot choosing to quit early from a sub-menu.")
            elif self.exceptions_found == 0 and self.turns_to_run_session == float('inf'):
                 self.log(f"Game session ran for {self.current_turn} turns and ended naturally (e.g., game completion, defeat, or bot quit).")

        except Exception as e:
            self.log(f"CRITICAL ERROR during test session on bot's game turn {self.current_turn}: {e}")
            tb_str = traceback.format_exc()
            self.log(f"Traceback:\n{tb_str}")
            self.exceptions_found += 1
            if hasattr(self.game, 'player') and self.game.player:
                try:
                    player_state_dump = json.dumps(self.game.player, indent=2)
                    self.log(f"Player state at time of error:\n{player_state_dump}")
                except Exception as dump_e:
                    self.log(f"Could not dump player state: {dump_e}")
            else:
                self.log("Player object not available or not initialized at time of error.")

        finally:
            self._restore_patches()
            self.log("Test session finished.")
            self.log(f"Total unhandled prompts: {len(self.unhandled_prompts)}")
            if self.unhandled_prompts:
                self.log("Unhandled prompts list:")
                for p_idx, p_val in enumerate(self.unhandled_prompts):
                    self.log(f"  {p_idx+1}: {p_val}")
            self.log(f"Total exceptions caught by bot: {self.exceptions_found}")
            if self.log_file:
                self.log_file.close()

if __name__ == "__main__":
    print("Initializing game for bot testing...")
    game_instance = TowerOfChance() 
    
    log_file_abs_path = os.path.abspath(LOG_FILE)
    print(f"Initializing bot. Log will be at: {log_file_abs_path}")
    
    bot = GameTesterBot(game_instance, log_file_abs_path)
    
    print("Running bot test session...")
    # Set num_turns=0 to try and complete the game
    # Set num_turns to a specific number for a limited run
    bot.run_test_session(num_turns=0) 
    
    print(f"Bot session complete. Check {log_file_abs_path} for details.")
    if bot.exceptions_found > 0:
        print(f"{Fore.RED}WARNING: Bot encountered {bot.exceptions_found} exceptions!{Style.RESET_ALL}")
    if bot.unhandled_prompts:
        print(f"{Fore.YELLOW}WARNING: Bot encountered {len(bot.unhandled_prompts)} unhandled input prompts.{Style.RESET_ALL}")
