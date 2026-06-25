# Forensics AI: Classical State-Space Crime Solver

An automated reasoning agent that models forensic criminal investigations as a classical **AI State-Space Search** problem. This repository demonstrates the transition of a procedural filtering script into an engineered, modular graph-traversal framework capable of executing both uninformed and informed search strategies to isolate target goal states.

---

## 🏗️ Architecture & Core Paradigms

Instead of evaluating criteria using standard procedural logic loops or hardcoded conditionals, the engine abstracts the investigation into an explicit **State-Space Tree**.
              [ Root Node: All 6 Suspects ]
                 /          |            \
   [Jacket: Black]    [Jacket: Red]     [Jacket: Blue]
     (4 Suspects)      (1 Suspect)       (1 Suspect)
      /         \           |                 |
[Height: Tall]  [...]      [Goal Found]      [Goal Found]


### 1. The State Wrapper (`InvestigationNode`)
Every checkpoint in the search space is tracked independently inside a custom object instance. The node retains:
* `remaining_suspects`: The shrinking subset of valid records matching the current path.
* `applied_clues`: The history of decisions and filters traversed to reach this state.
* `path_cost` $g(n)$: The explicit transitions (clues evaluated) from the root.

### 2. Uninformed Explorations (BFS vs. DFS)
By altering the operational mechanics of the **Frontier (Open List)** via Python's `collections.deque`, the agent evaluates the state space using two fundamental methodologies:
* **Depth-First Search (DFS):** Operates as a LIFO Stack (`frontier.pop()`), plunging down a singular sequence of criteria before backtracking.
* **Breadth-First Search (BFS):** Operates as a FIFO Queue (`frontier.popleft()`), traversing horizontally level-by-level across all attribute variations.

### 3. Informed Optimization ($A^*$ Search)
To maximize search space efficiency, an informed search agent calculates prioritization using an evaluation function:

$$f(n) = g(n) + h(n)$$

Where:
* $g(n)$ is the true step depth (`path_cost`).
* $h(n)$ is a strictly **admissible heuristic** estimating the remaining distance to a solution: 

$$\text{Total Expected Attributes} - \text{Currently Applied Attributes}$$

The frontier is managed via a binary Min-Heap (`heapq`), guaranteeing $O(\log n)$ extraction efficiency for the lowest $f(n)$ node.

---

## 📂 Repository Structure

* **`main.py`** - Interactive command-line interface. Captures simulated evidence profiles from witnesses and executes the chosen search agent.
* **`algorithms.py`** - Core algorithmic powerhouse containing the `InvestigationNode` state engine, uninformed traversal routines, and the informed $A^*$ min-heap pipeline.
* **`data.py`** - Static knowledge base separating the application logic from data attributes. Tracks profiles across multiple case files (`Murder` and `Pickpocket`).
* **`analysis.py`** - Automated benchmarking suite that runs algorithms concurrently against fixed target profiles to gather metrics.
* **`search_tree.py`** & **`utils.py`** - Architectural metadata blueprints and baseline validator scripts.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher
* Standard library utilities (`collections`, `heapq`, `time`)

### Installation
Clone the repository to your local workspace:
```bash
git clone [https://github.com/BasimKazmi/Crime-AI-solver-using-Classical-AI.git](https://github.com/BasimKazmi/Crime-AI-solver-using-Classical-AI.git)
cd Crime-AI-solver-using-Classical-AI


```
==================================================
   AI SEARCH ALGORITHM PERFORMANCE BENCHMARK   
==================================================
Target Criminal Profile: {'jacket': 'black', 'height': 'tall', 'weapon': 'knife', ...}

Algorithm  | Nodes Expanded  | Execution Time (ms)  | Result
---------------------------------------------------------------------------
DFS        | 3               | 0.1245               | Bilal
BFS        | 6               | 0.2891               | Bilal
A*         | 2               | 0.0812               | Bilal
---------------------------------------------------------------------------
Benchmark Complete.
