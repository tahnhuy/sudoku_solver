import time
import copy
from collections import deque
import random
import math
import numpy as np

class AlgorithmManager:
    def __init__(self):
        self.algorithms = {
            "Depth-First Search": self.depth_first_search,
            "Breadth-First Search": self.breadth_first_search,
            "Uniform Cost Search": self.uniform_cost_search,
            "A* Search": self.a_star_search,
            "Best-First Search": self.best_first_search,
            "Hill Climbing": self.hill_climbing,
            "Simulated Annealing": self.simulated_annealing,
            "Backtracking": self.backtracking,
            "Forward Checking": self.forward_checking,
            "AC-3": self.ac3
        }
        self.steps = 0
        self.start_state = None
        self.target_state = None

    def solve(self, board, algorithm_name):
        self.steps = 0
        self.start_state = board.get_board_state()
        
        start_time = time.time()
        if algorithm_name in self.algorithms:
            result = self.algorithms[algorithm_name](board)
        else:
            return None
        
        end_time = time.time()
        
        if result:
            self.target_state = board.get_board_state()
            return {
                "steps": self.steps,
                "time": end_time - start_time,
                "complexity": self.get_complexity(algorithm_name),
                "start_state": self.start_state,
                "target_state": self.target_state
            }
        return None

    def get_complexity(self, algorithm_name):
        # Theoretical complexity for each algorithm
        complexities = {
            "Depth-First Search": "O(b^d)",
            "Breadth-First Search": "O(b^d)",
            "Uniform Cost Search": "O(b^(1 + floor(C/ε)))",
            "A* Search": "O(b^d)",
            "Best-First Search": "O(b^d)",
            "Hill Climbing": "O(n)",
            "Simulated Annealing": "O(n)",
            "Backtracking": "O(n!)",
            "Forward Checking": "O(n!)",
            "AC-3": "O(n^2d^3)"
        }
        return complexities.get(algorithm_name, "Unknown")

    def depth_first_search(self, board):
        def dfs(pos):
            self.steps += 1
            if not pos:
                return True
            
            row, col = pos
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    board.set_value(row, col, num)
                    next_pos = board.find_empty()
                    if dfs(next_pos):
                        return True
                    board.set_value(row, col, 0)
            return False

        start_pos = board.find_empty()
        return dfs(start_pos)

    def breadth_first_search(self, board):
        # Implementation for BFS
        from collections import deque
        import numpy as np
        
        def get_state_key(state):
            return tuple(map(tuple, state))
            
        queue = deque()
        start_state = board.get_board_state()
        start_pos = board.find_empty()
        
        # If no empty positions, the board is already solved
        if not start_pos:
            return True
            
        queue.append((start_state, start_pos))
        visited = set([get_state_key(start_state)])

        while queue:
            self.steps += 1
            current_state, pos = queue.popleft()
            
            # Set the board to the current state for valid move checking
            board.set_board_state(current_state)
            
            # If no empty positions, we've found a solution
            if not pos:
                return True
                
            row, col = pos
            
            # Try all possible values for the current empty cell
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    # Create a new state with the number placed
                    new_state = np.copy(current_state)
                    new_state[row][col] = num
                    
                    # Find the next empty cell
                    board.set_board_state(new_state)
                    next_pos = board.find_empty()
                    
                    # If no more empty cells, we've found a solution
                    if not next_pos:
                        board.set_board_state(new_state)
                        return True
                    
                    # Add the new state to the queue if not visited
                    new_key = get_state_key(new_state)
                    if new_key not in visited:
                        visited.add(new_key)
                        queue.append((new_state, next_pos))
        
        # If we've exhausted all possibilities without finding a solution
        board.set_board_state(start_state)
        return False

    def uniform_cost_search(self, board):
        # Basic implementation of Uniform Cost Search
        return self.depth_first_search(board)  # Simplified version

    def get_heuristic(self, board):
        # Count the number of empty cells as a heuristic
        empty_count = 0
        for i in range(9):
            for j in range(9):
                if board.get_value(i, j) == 0:
                    empty_count += 1
        return empty_count

    def a_star_search(self, board):
        from queue import PriorityQueue
        import numpy as np
        
        # Simple wrapper class to make comparison work in priority queue
        class PrioritizedItem:
            def __init__(self, priority, item):
                self.priority = priority
                self.item = item
                
            def __lt__(self, other):
                return self.priority < other.priority
        
        def get_state_key(state):
            return tuple(map(tuple, state))
            
        pq = PriorityQueue()
        start_state = board.get_board_state()
        start_pos = board.find_empty()
        
        # If no empty positions, the board is already solved
        if not start_pos:
            return True
            
        g_score = {get_state_key(start_state): 0}
        visited = set([get_state_key(start_state)])
        
        # Priority queue items with wrapper
        h_score = self.get_heuristic(board)
        pq.put(PrioritizedItem(h_score, (start_state, start_pos)))
        
        while not pq.empty():
            self.steps += 1
            current = pq.get().item
            current_state, pos = current
            
            # Set the board to the current state
            board.set_board_state(current_state)
            
            # If no empty positions, we've found a solution
            if not pos:
                return True
                
            row, col = pos
            state_key = get_state_key(current_state)
            
            # Try all possible values for the current empty cell
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    # Create a new state with the number placed
                    new_state = np.copy(current_state)
                    new_state[row][col] = num
                    
                    # Find the next empty cell
                    board.set_board_state(new_state)
                    next_pos = board.find_empty()
                    
                    # If no more empty cells, we've found a solution
                    if not next_pos:
                        board.set_board_state(new_state)
                        return True
                    
                    # Calculate new g_score
                    new_key = get_state_key(new_state)
                    tentative_g_score = g_score[state_key] + 1
                    
                    # If we found a better path or haven't visited this state
                    if new_key not in g_score or tentative_g_score < g_score[new_key]:
                        # Update g_score
                        g_score[new_key] = tentative_g_score
                        
                        # Calculate f_score = g_score + heuristic
                        h_score = self.get_heuristic(board)
                        f_score = tentative_g_score + h_score
                        
                        # Add to priority queue if not visited
                        if new_key not in visited:
                            visited.add(new_key)
                            pq.put(PrioritizedItem(f_score, (new_state, next_pos)))
        
        # If we've exhausted all possibilities without finding a solution
        board.set_board_state(start_state)
        return False

    def best_first_search(self, board):
        from queue import PriorityQueue
        import numpy as np
        
        # Simple wrapper class to make comparison work in priority queue
        class PrioritizedItem:
            def __init__(self, priority, item):
                self.priority = priority
                self.item = item
                
            def __lt__(self, other):
                return self.priority < other.priority
        
        def get_state_key(state):
            return tuple(map(tuple, state))
            
        pq = PriorityQueue()
        start_state = board.get_board_state()
        start_pos = board.find_empty()
        
        # If no empty positions, the board is already solved
        if not start_pos:
            return True
            
        # Priority queue items with wrapper
        h_score = self.get_heuristic(board)
        pq.put(PrioritizedItem(h_score, (start_state, start_pos)))
        
        visited = set([get_state_key(start_state)])
        
        while not pq.empty():
            self.steps += 1
            current = pq.get().item
            current_state, pos = current
            
            # Set the board to the current state
            board.set_board_state(current_state)
            
            # If no empty positions, we've found a solution
            if not pos:
                return True
                
            row, col = pos
            
            # Try all possible values for the current empty cell
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    # Create a new state with the number placed
                    new_state = np.copy(current_state)
                    new_state[row][col] = num
                    
                    # Find the next empty cell
                    board.set_board_state(new_state)
                    next_pos = board.find_empty()
                    
                    # If no more empty cells, we've found a solution
                    if not next_pos:
                        board.set_board_state(new_state)
                        return True
                    
                    # Add the new state to the queue if not visited
                    new_key = get_state_key(new_state)
                    if new_key not in visited:
                        visited.add(new_key)
                        h_score = self.get_heuristic(board)
                        pq.put(PrioritizedItem(h_score, (new_state, next_pos)))
        
        # If we've exhausted all possibilities without finding a solution
        board.set_board_state(start_state)
        return False

    def hill_climbing(self, board):
        current_state = board.get_board_state()
        while True:
            self.steps += 1
            improved = False
            pos = board.find_empty()
            
            if not pos:
                return True
                
            row, col = pos
            current_conflicts = self.count_conflicts(board)
            best_value = None
            min_conflicts = float('inf')
            
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    board.set_value(row, col, num)
                    conflicts = self.count_conflicts(board)
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_value = num
                        improved = True
                    board.set_value(row, col, 0)
            
            if not improved:
                board.set_board_state(current_state)
                return False
                
            board.set_value(row, col, best_value)
            if min_conflicts == 0:
                return True

    def simulated_annealing(self, board):
        def acceptance_probability(old_cost, new_cost, temperature):
            if new_cost < old_cost:
                return 1.0
            return math.exp((old_cost - new_cost) / temperature)

        current_state = board.get_board_state()
        current_cost = self.count_conflicts(board)
        temperature = 1.0
        cooling_rate = 0.95
        
        while temperature > 0.01:
            self.steps += 1
            pos = board.find_empty()
            if not pos:
                return True
                
            row, col = pos
            num = random.randint(1, 9)
            
            if board.is_valid_move(row, col, num):
                board.set_value(row, col, num)
                new_cost = self.count_conflicts(board)
                
                if acceptance_probability(current_cost, new_cost, temperature) > random.random():
                    current_cost = new_cost
                    if current_cost == 0:
                        return True
                else:
                    board.set_value(row, col, 0)
                    
            temperature *= cooling_rate
            
        board.set_board_state(current_state)
        return False

    def backtracking(self, board):
        return self.depth_first_search(board)  # Same as DFS for Sudoku

    def get_domain(self, board, row, col):
        domain = set(range(1, 10))
        # Check row
        for j in range(9):
            if board.get_value(row, j) != 0:
                domain.discard(board.get_value(row, j))
        # Check column
        for i in range(9):
            if board.get_value(i, col) != 0:
                domain.discard(board.get_value(i, col))
        # Check box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board.get_value(i, j) != 0:
                    domain.discard(board.get_value(i, j))
        return domain

    def forward_checking(self, board):
        def fc(domains):
            self.steps += 1
            pos = board.find_empty()
            if not pos:
                return True
                
            row, col = pos
            for num in domains[(row, col)]:
                if board.is_valid_move(row, col, num):
                    board.set_value(row, col, num)
                    
                    # Save current domains
                    old_domains = {k: v.copy() for k, v in domains.items()}
                    
                    # Update domains
                    updated = True
                    for i in range(9):
                        for j in range(9):
                            if board.get_value(i, j) == 0:
                                new_domain = self.get_domain(board, i, j)
                                if not new_domain:
                                    updated = False
                                    break
                                domains[(i, j)] = new_domain
                        if not updated:
                            break
                            
                    if updated and fc(domains):
                        return True
                        
                    # Restore domains and backtrack
                    domains.update(old_domains)
                    board.set_value(row, col, 0)
                    
            return False

        # Initialize domains for all empty cells
        domains = {}
        for i in range(9):
            for j in range(9):
                if board.get_value(i, j) == 0:
                    domains[(i, j)] = self.get_domain(board, i, j)
                    
        return fc(domains)

    def ac3(self, board):
        def get_neighbors(row, col):
            neighbors = set()
            # Same row
            for j in range(9):
                if j != col:
                    neighbors.add((row, j))
            # Same column
            for i in range(9):
                if i != row:
                    neighbors.add((i, col))
            # Same box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if i != row or j != col:
                        neighbors.add((i, j))
            return neighbors

        def revise(domains, xi, xj):
            revised = False
            i, j = xi
            if board.get_value(i, j) != 0:
                return False
                
            domain_i = domains[xi]
            domain_j = domains[xj]
            
            for x in list(domain_i):
                # If no value in j's domain satisfies the constraint
                if len(domain_j) == 1 and x in domain_j:
                    domain_i.remove(x)
                    revised = True
            return revised

        def ac3_algorithm(domains):
            self.steps += 1
            queue = []
            # Add all arcs to queue
            for i in range(9):
                for j in range(9):
                    if board.get_value(i, j) == 0:
                        for neighbor in get_neighbors(i, j):
                            queue.append(((i, j), neighbor))

            while queue:
                xi, xj = queue.pop(0)
                if revise(domains, xi, xj):
                    if not domains[xi]:
                        return False
                    for xk in get_neighbors(*xi):
                        if xk != xj:
                            queue.append((xk, xi))
            return True

        # Initialize domains
        domains = {}
        for i in range(9):
            for j in range(9):
                if board.get_value(i, j) == 0:
                    domains[(i, j)] = self.get_domain(board, i, j)
                else:
                    domains[(i, j)] = {board.get_value(i, j)}

        # Run AC-3
        if not ac3_algorithm(domains):
            return False

        # Use backtracking with the reduced domains
        def backtrack_with_ac3(domains):
            self.steps += 1
            pos = board.find_empty()
            if not pos:
                return True
                
            row, col = pos
            for num in domains[(row, col)]:
                if board.is_valid_move(row, col, num):
                    board.set_value(row, col, num)
                    if backtrack_with_ac3(domains):
                        return True
                    board.set_value(row, col, 0)
            return False

        return backtrack_with_ac3(domains)

    def count_conflicts(self, board):
        conflicts = 0
        for i in range(9):
            for j in range(9):
                if board.get_value(i, j) != 0:
                    # Check row
                    for k in range(9):
                        if k != j and board.get_value(i, k) == board.get_value(i, j):
                            conflicts += 1
                    # Check column
                    for k in range(9):
                        if k != i and board.get_value(k, j) == board.get_value(i, j):
                            conflicts += 1
                    # Check box
                    box_row = (i // 3) * 3
                    box_col = (j // 3) * 3
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if (r != i or c != j) and board.get_value(r, c) == board.get_value(i, j):
                                conflicts += 1
        return conflicts 