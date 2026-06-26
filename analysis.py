# analysis.py
import time
from data import crime_cases
from algorithms import automated_search, a_star_search

def run_benchmark():
    print("\n" + "="*50)
    print("   AI SEARCH ALGORITHM PERFORMANCE BENCHMARK   ")
    print("="*50)

    # 1. Setup the Test Environment
    suspects = crime_cases["Murder"]["suspects"]
    clue_order = ["jacket", "height", "weapon", "hair", "beard", "fingerprint"]
    
    # Let's use Moeez as our target target. 
    # His traits: black jacket, tall, knife, short hair, beard, fingerprint=True
    target_profile = {
        "jacket": "black",
        "height": "tall",
        "weapon": "knife",
        "hair": "short",
        "beard": "True",
        "fingerprint": "True"
    }

    print(f"Target Criminal Profile: {target_profile}\n")
    print(f"{'Algorithm':<10} | {'Nodes Expanded':<15} | {'Execution Time (ms)':<20} | {'Result'}")
    print("-" * 75)

    # 2. Define the competitors
    strategies = ["DFS", "BFS"]
    
    # 3. Execute Uninformed Searches
    for strategy in strategies:
        start_time = time.perf_counter()
        
        # We suppress standard print outputs in a real benchmark, 
        # but here we'll just let them run and capture the returns.
        criminal, nodes = automated_search(suspects, clue_order, target_profile, strategy=strategy)
        
        end_time = time.perf_counter()
        exec_time = (end_time - start_time) * 1000 # Convert to milliseconds
        
        print(f"{strategy:<10} | {nodes:<15} | {exec_time:<20.4f} | {criminal}")

    # 4. Execute Informed Search (A*)
    start_time = time.perf_counter()
    criminal, nodes = a_star_search(suspects, clue_order, target_profile)
    end_time = time.perf_counter()
    exec_time = (end_time - start_time) * 1000
    
    print(f"{'A*':<10} | {nodes:<15} | {exec_time:<20.4f} | {criminal}")
    print("-" * 75)
    print("Benchmark Complete.\n")

if __name__ == "__main__":
    # Temporarily mute prints from algorithms.py if you want a clean table, 
    # or just let it print the trace above the table!
    run_benchmark()