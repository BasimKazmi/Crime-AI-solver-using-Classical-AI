# algorithms.py
import heapq
from collections import deque

class InvestigationNode:
    """Represents a state in the AI search space tree."""
    def __init__(self, remaining_suspects, applied_clues=None, path_cost=0, total_clues_count=6):
        self.remaining_suspects = remaining_suspects
        self.applied_clues = applied_clues if applied_clues is not None else {}
        self.path_cost = path_cost
        self.total_clues_count = total_clues_count

    def is_goal(self):
        """Goal state is reached when exactly one suspect remains."""
        return len(self.remaining_suspects) == 1

    def is_dead_end(self):
        """A state is a dead end if no suspects match the current path criteria."""
        return len(self.remaining_suspects) == 0

    def heuristic(self):
        """
        Admissible Heuristic h(n): Number of clues left to match.
        Never overestimates because it takes exactly 1 step per clue level.
        """
        return self.total_clues_count - len(self.applied_clues)

    def f_cost(self):
        """Total evaluation function f(n) = g(n) + h(n)"""
        return self.path_cost + self.heuristic()

    def __lt__(self, other):
        """Required for heapq to sort nodes based on lowest f(n) cost."""
        return self.f_cost() < other.f_cost()


def automated_search(suspects, clue_order, evidence_profile, strategy="DFS"):
    """
    Classic AI State-Space Search Framework (Uninformed).
    Traverses the problem space using an explicit Frontier.
    """
    # Root node contains all possibilities
    root = InvestigationNode(
        remaining_suspects=suspects.copy(), 
        total_clues_count=len(clue_order)
    )
    
    # Initialize Frontier based on Strategy
    frontier = deque([root]) # Acts as Stack for DFS, Queue for BFS
    nodes_expanded = 0
    
    print(f"\n--- Starting Automated {strategy} Crime-Solving Agent ---")
    
    while frontier:
        # Pop from right for DFS (LIFO Stack), pop from left for BFS (FIFO Queue)
        current_node = frontier.pop() if strategy == "DFS" else frontier.popleft()
        nodes_expanded += 1
        
        # 1. Goal Check
        if current_node.is_goal():
            criminal_name = list(current_node.remaining_suspects.keys())[0]
            print(f"\n[SUCCESS] Goal State Found in {nodes_expanded} expansions!")
            print(f"Criminal Identified: {criminal_name}")
            print(f"Path Traversed: {current_node.applied_clues}")
            return criminal_name, nodes_expanded
            
        # Determine the next clue attribute to evaluate based on search depth
        clue_depth = len(current_node.applied_clues)
        if clue_depth >= len(clue_order):
            continue # No more clues to expand from this branch
            
        next_clue_attr = clue_order[clue_depth]
        
        # 2. Expansion / Generating Successors
        target_value = str(evidence_profile.get(next_clue_attr)).lower()
        
        # Filter down suspects for the next branch
        child_suspects = {}
        for name, data in current_node.remaining_suspects.items():
            if str(data.get(next_clue_attr)).lower() == target_value:
                child_suspects[name] = data
                
        # Create child state node
        next_applied = current_node.applied_clues.copy()
        next_applied[next_clue_attr] = target_value
        
        child_node = InvestigationNode(
            remaining_suspects=child_suspects,
            applied_clues=next_applied,
            path_cost=current_node.path_cost + 1,
            total_clues_count=len(clue_order)
        )
        
        # 3. Pruning dead branches early
        if not child_node.is_dead_end():
            print(f"Expanding Node Level {clue_depth}: Clue [{next_clue_attr}={target_value}] -> Potential Pool Size: {len(child_suspects)}")
            frontier.append(child_node)
            
    print(f"\n[FAILURE] Search space exhausted after {nodes_expanded} expansions. No suspect matches profile.")
    return None, nodes_expanded


def a_star_search(suspects, clue_order, evidence_profile):
    """
    Informed A* Search Algorithm.
    Uses a Priority Queue sorted by f(n) = g(n) + h(n).
    """
    total_clues = len(clue_order)
    root = InvestigationNode(
        remaining_suspects=suspects.copy(), 
        total_clues_count=total_clues
    )
    
    # The priority queue stores nodes directly. 
    # heapq automatically uses the __lt__ method we defined on the node
    priority_queue = []
    heapq.heappush(priority_queue, root)
    
    nodes_expanded = 0
    print("\n--- Starting Informed A* Crime-Solving Agent ---")
    
    while priority_queue:
        # Pop the node with the lowest f(n) value
        current_node = heapq.heappop(priority_queue)
        nodes_expanded += 1
        
        # Goal Test
        if current_node.is_goal():
            criminal_name = list(current_node.remaining_suspects.keys())[0]
            print(f"\n[SUCCESS] A* Found Goal State in {nodes_expanded} expansions!")
            print(f"Criminal Identified: {criminal_name}")
            print(f"Path Evaluation Cost f(n): {current_node.f_cost()} (g={current_node.path_cost}, h={current_node.heuristic()})")
            return criminal_name, nodes_expanded
            
        clue_depth = len(current_node.applied_clues)
        if clue_depth >= total_clues:
            continue
            
        next_clue_attr = clue_order[clue_depth]
        target_value = str(evidence_profile.get(next_clue_attr)).lower()
        
        # Generate successor state
        child_suspects = {}
        for name, data in current_node.remaining_suspects.items():
            if str(data.get(next_clue_attr)).lower() == target_value:
                child_suspects[name] = data
                
        next_applied = current_node.applied_clues.copy()
        next_applied[next_clue_attr] = target_value
        
        child_node = InvestigationNode(
            remaining_suspects=child_suspects,
            applied_clues=next_applied,
            path_cost=current_node.path_cost + 1,
            total_clues_count=total_clues
        )
        
        if not child_node.is_dead_end():
            print(f"Queueing Node -> Clue [{next_clue_attr}={target_value}] | f(n)={child_node.f_cost()}")
            heapq.heappush(priority_queue, child_node)
            
    print(f"\n[FAILURE] Search space exhausted. No criminal matches profile.")
    return None, nodes_expanded