# main.py
import time
import sys
from data import crime_cases
from algorithms import automated_search, a_star_search
from search_tree import MURDER_CLUES, PICKPOCKET_CLUES

# --- ANSI Color Codes for Terminal Styling ---
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    """Prints a styled ASCII banner."""
    print(f"\n{CYAN}{BOLD}")
    print("==================================================")
    print("             CLASSICAL AI CRIME SOLVER            ")
    print("             State-Space Search Engine            ")
    print("==================================================")
    print(f"{RESET}")

def simulate_thinking():
    """Adds a dramatic delay to simulate graph traversal."""
    print(f"\n{YELLOW}Initializing AI Agent...{RESET}")
    time.sleep(0.5)
    print(f"{YELLOW}Constructing State-Space Tree...{RESET}")
    time.sleep(0.5)
    print(f"{YELLOW}Traversing Frontier...{RESET}")
    
    # Simple loading spinner effect
    for _ in range(15):
        sys.stdout.write(f"{CYAN}█{RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n")

def main():
    print_banner()
    
    print(f"{BOLD}AVAILABLE SCENARIOS:{RESET}")
    print(f"{GREEN}[ 1 ]{RESET} Run Automated Murder Investigation")
    print(f"{GREEN}[ 2 ]{RESET} Run Automated Pickpocket Investigation")
    
    choice = input(f"\n{BOLD}Select Case Scenario (1 or 2): {RESET}").strip()
    
    if choice == "1":
        suspects = crime_cases["Murder"]["suspects"]
        clue_order = MURDER_CLUES
        scenario_name = "Murder"
        
        print(f"\n{MAGENTA}--- Loading {scenario_name} Evidence Profile ---{RESET}")
        profile = {
            "jacket": input(f"Jacket color {CYAN}(e.g., black, red, blue){RESET}: ").strip(),
            "height": input(f"Height {CYAN}(tall, medium, short){RESET}: ").strip(),
            "weapon": input(f"Weapon {CYAN}(knife, gun){RESET}: ").strip(),
            "hair": input(f"Hair style {CYAN}(short, long){RESET}: ").strip(),
            "beard": input(f"Beard {CYAN}(True/False){RESET}: ").strip().capitalize() == "True",
            "fingerprint": input(f"Fingerprint Match {CYAN}(True/False){RESET}: ").strip().capitalize() == "True"
        }
        
    elif choice == "2":
        suspects = crime_cases["Pickpocket"]["suspects"]
        clue_order = PICKPOCKET_CLUES
        scenario_name = "Pickpocket"
        
        print(f"\n{MAGENTA}--- Loading {scenario_name} Evidence Profile ---{RESET}")
        profile = {
            "cap": input(f"Cap color {CYAN}(e.g., blue, red, black){RESET}: ").strip(),
            "height": input(f"Height {CYAN}(tall, medium, short){RESET}: ").strip(),
            "shirt": input(f"Shirt color {CYAN}(e.g., white, black){RESET}: ").strip(),
            "beard": input(f"Beard {CYAN}(True/False){RESET}: ").strip().capitalize() == "True",
            "bag": input(f"Carrying bag {CYAN}(True/False){RESET}: ").strip().capitalize() == "True",
            "witness_match": input(f"Witness Match {CYAN}(True/False){RESET}: ").strip().capitalize() == "True"
        }
    else:
        print(f"{RED}Invalid selection. Aborting.{RESET}")
        return

    print(f"\n{BOLD}SELECT ALGORITHM:{RESET}")
    print(f"{CYAN}DFS{RESET} - Depth-First Search (Uninformed)")
    print(f"{CYAN}BFS{RESET} - Breadth-First Search (Uninformed)")
    print(f"{CYAN}A*{RESET}  - A-Star Search (Informed Heuristic)")
    
    strategy = input(f"\n{BOLD}Enter Strategy: {RESET}").strip().upper()
    
    # Trigger the visual loading effect
    simulate_thinking()
    
    # Execute the selected search
    if strategy == "A*":
        criminal, nodes = a_star_search(suspects, clue_order, profile)
    else:
        if strategy not in ["DFS", "BFS"]: 
            strategy = "DFS"
            print(f"{YELLOW}Defaulting to DFS...{RESET}")
        criminal, nodes = automated_search(suspects, clue_order, profile, strategy=strategy)
        
    # Beautiful formatting for the final output
    print(f"{CYAN}{BOLD}=================================================={RESET}")
    if criminal:
        print(f"{GREEN}{BOLD}>> CASE CLOSED <<{RESET}")
        print(f"Target Identified : {RED}{BOLD}{criminal}{RESET}")
        print(f"Algorithm Used    : {YELLOW}{strategy}{RESET}")
        print(f"Nodes Expanded    : {YELLOW}{nodes}{RESET}")
    else:
        print(f"{RED}{BOLD}>> INVESTIGATION FAILED <<{RESET}")
        print("No suspect in the database matches this exact profile.")
        print(f"Nodes Expanded    : {YELLOW}{nodes}{RESET}")
    print(f"{CYAN}{BOLD}=================================================={RESET}\n")

if __name__ == "__main__":
    main()