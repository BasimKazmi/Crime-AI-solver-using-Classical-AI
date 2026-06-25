# main.py
from data import crime_cases
from algorithms import automated_search

def main():
    print("\n===== CLASSIC AI CRIME ENGINE =====")
    print("1. Run Automated Murder Investigation")
    print("2. Run Automated Pickpocket Investigation")
    
    choice = input("\nSelect Case Scenario: ")
    
    if choice == "1":
        suspects = crime_cases["Murder"]["suspects"]
        clue_order = ["jacket", "height", "weapon", "hair", "beard", "fingerprint"]
        
        # Simulated profile fed into the automated search agent
        print("\nEnter target crime evidence profile to solve for:")
        profile = {
            "jacket": input("Jacket color (e.g., black, red, blue): ").strip(),
            "height": input("Height (tall, medium, short): ").strip(),
            "weapon": input("Weapon (knife, gun): ").strip(),
            "hair": input("Hair style (short, long): ").strip(),
            "beard": input("Beard (True/False): ").strip().capitalize() == "True",
            "fingerprint": input("Fingerprint Match (True/False): ").strip().capitalize() == "True"
        }
        
        strategy = input("Choose AI Search Strategy (DFS / BFS): ").strip().upper()
        if strategy not in ["DFS", "BFS"]: strategy = "DFS"
        
        automated_search(suspects, clue_order, profile, strategy=strategy)
        
    elif choice == "2":
        suspects = crime_cases["Pickpocket"]["suspects"]
        clue_order = ["cap", "height", "shirt", "beard", "bag", "witness_match"]
        
        print("\nEnter target crime evidence profile to solve for:")
        profile = {
            "cap": input("Cap color: ").strip(),
            "height": input("Height: ").strip(),
            "shirt": input("Shirt color: ").strip(),
            "beard": input("Beard (True/False): ").strip().capitalize() == "True",
            "bag": input("Carrying bag (True/False): ").strip().capitalize() == "True",
            "witness_match": input("Witness Match (True/False): ").strip().capitalize() == "True"
        }
        
        strategy = input("Choose AI Search Strategy (DFS / BFS): ").strip().upper()
        if strategy not in ["DFS", "BFS"]: strategy = "DFS"
        
        automated_search(suspects, clue_order, profile, strategy=strategy)

if __name__ == "__main__":
    main()