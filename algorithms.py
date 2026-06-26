# algorithms.py
import heapq
from collections import deque

class InvestigationNode:
    """Represents a branching state in the AI search tree."""
    def __init__(self, remaining_suspects, applied_clues=None, path_cost=0):
        self.remaining_suspects = remaining_suspects
        self.applied_clues = applied_clues if applied_clues is not None else {}
        self.path_cost = path_cost  # g(n)

    def is_goal(self):
        """Goal state is reached when exactly one suspect remains."""
        return len(self.remaining_suspects) == 1

    def is_dead_end(self):
        """A state is a dead end if no suspects match the current path criteria."""
        return len(self.remaining_suspects) == 0

    def heuristic(self):
        """
        Admissible Heuristic h(n): Number of suspects left to eliminate.
        Guards optimization by favoring paths that shrink the pool fastest.
        """
        return max(0, len(self.remaining_suspects) - 1)

    def f_cost(self):
        """Total evaluation function f(n) = g(n) + h(n)"""
        return self.path_cost + self.heuristic()

    def __lt__(self, other):
        """Required for heapq to sort nodes based on lowest f(n) cost."""
        return self.f_cost() < other.f_cost()


def automated_search(suspects, clue_order, evidence_profile, strategy="DFS"):
    """
    Uninformed branching search (BFS/DFS) exploring all clue options.
    """
    root = InvestigationNode(remaining_suspects=suspects.copy())
    frontier = deque([root])
    nodes_expanded = 0
    
    print(f"\n--- Starting Automated {strategy} Crime-Solving Agent ---")
    
    while frontier:
        # Pop from right for DFS (LIFO Stack), pop from left for BFS (FIFO Queue)
        current_node = frontier.pop() if strategy == "DFS" else frontier.popleft()
        nodes_expanded += 1
        
        # 1. Goal Check
        if current_node.is_goal():
            criminal_name = list(current_node.remaining_suspects.keys())[0]
            print(f"[SUCCESS] {strategy} found {criminal_name} (Expanded {nodes_expanded} nodes)")
            return criminal_name, nodes_expanded
            
        # 2. Branch out: Try EVERY clue that hasn't been used yet in this path
        for clue in clue_order:
            if clue not in current_node.applied_clues:
                target_value = str(evidence_profile.get(clue)).lower()
                
                # Filter down suspects for the next branch
                child_suspects = {}
                for name, data in current_node.remaining_suspects.items():
                    if str(data.get(clue)).lower() == target_value:
                        child_suspects[name] = data
                
                # Create child state node
                next_applied = current_node.applied_clues.copy()
                next_applied[clue] = target_value
                
                child_node = InvestigationNode(
                    remaining_suspects=child_suspects,
                    applied_clues=next_applied,
                    path_cost=current_node.path_cost + 1
                )
                
                # 3. Pruning dead branches early
                if not child_node.is_dead_end():
                    frontier.append(child_node)
                    
    return None, nodes_expanded


def a_star_search(suspects, clue_order, evidence_profile):
    """
    Informed A* Search using a priority queue to select the most optimal clue.
    """
    root = InvestigationNode(remaining_suspects=suspects.copy())
    
    priority_queue = []
    heapq.heappush(priority_queue, root)
    nodes_expanded = 0
    
    print("\n--- Starting Informed A* Crime-Solving Agent ---")
    
    while priority_queue:
        # Pop the node with the lowest f(n) value
        current_node = heapq.heappop(priority_queue)
        nodes_expanded += 1
        
        # 1. Goal Check
        if current_node.is_goal():
            criminal_name = list(current_node.remaining_suspects.keys())[0]
            print(f"[SUCCESS] A* found {criminal_name} (Expanded {nodes_expanded} nodes)")
            return criminal_name, nodes_expanded
            
        # 2. Branch out intelligently
        for clue in clue_order:
            if clue not in current_node.applied_clues:
                target_value = str(evidence_profile.get(clue)).lower()
                
                # Filter down suspects for the next branch
                child_suspects = {}
                for name, data in current_node.remaining_suspects.items():
                    if str(data.get(clue)).lower() == target_value:
                        child_suspects[name] = data
                
                # Create child state node
                next_applied = current_node.applied_clues.copy()
                next_applied[clue] = target_value
                
                child_node = InvestigationNode(
                    remaining_suspects=child_suspects,
                    applied_clues=next_applied,
                    path_cost=current_node.path_cost + 1
                )
                
                # 3. Pruning dead branches early
                if not child_node.is_dead_end():
                    heapq.heappush(priority_queue, child_node)
                    
    return None, nodes_expanded