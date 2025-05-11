import time
import copy
from collections import deque
import random
import math
import numpy as np
import pandas as pd
import openpyxl
import openpyxl.styles
from .csp_algorithms import ac3, forward_checking, backtracking_search
from .reinforcement_learning import QLearning

class AlgorithmManager:
    def __init__(self):
        self.algorithms = {
            # Uninformed Search
            "Depth-First Search": self.depth_first_search,
            "Breadth-First Search": self.breadth_first_search,
            "Uniform Cost Search": self.uniform_cost_search,
            "Iterative Deepening Search": self.iterative_deepening_search,
            
            # Informed Search
            "A* Search": self.a_star_search,
            "Greed Search": self.greed_search,
            "IDA* Search": self.ida_star_search,
            
            # Local Search
            "Simple Hill Climbing": self.simple_hill_climbing,
            "Steepest-Ascent Hill Climbing": self.steepest_ascent_hill_climbing,
            "Stochastic Hill Climbing": self.stochastic_hill_climbing,
            "Simulated Annealing": self.simulated_annealing,
            "Local Beam Search": self.local_beam_search,
            "Genetic Algorithm": self.genetic_algorithm,
            
            # Complex Environment Search
            "AND-OR Graph Search": self.and_or_graph_search,
            "Partial Observation Search": self.partial_observation_search,
            
            # Constraint Satisfaction Problem
            "AC-3": self.ac3_solver,
            "Forward Checking": self.forward_checking_solver,
            "Backtracking": self.backtracking_solver,
            
            # Reinforcement Learning
            "Q-Learning": self.q_learning_solver
        }
        self.steps = 0
        self.start_state = None
        self.target_state = None
        self.states = []
        self.q_learning = QLearning()  # Initialize Q-Learning agent
        
        # For Partial Observation Search
        self.observations = {}
        self.hidden_cells = set()

    def solve(self, board, algorithm_name, timeout=5, cancel_flag=None):
        self.steps = 0
        self.start_state = board.get_board_state()
        self.states = [self.start_state.copy()]
        self.timeout = timeout
        self.start_time = time.time()
        self.cancel_flag = cancel_flag if cancel_flag is not None else (lambda: False)
        
        start_time = self.start_time
        if algorithm_name in self.algorithms:
            result = self.algorithms[algorithm_name](board)
        else:
            return None
        
        end_time = time.time()
        
        if result:
            self.target_state = board.get_board_state()
            metrics = {
                "steps": self.steps,
                "time": end_time - start_time,
                "complexity": self.get_complexity(algorithm_name),
                "start_state": self.start_state,
                "target_state": self.target_state,
                "states": self.states
            }
            # Export to Excel if solution was found
            self.export_to_excel(metrics)
            return metrics
        return None

    def export_to_excel(self, metrics):
        """Export the solution process to an Excel file"""
        try:
            # Create a DataFrame for the metrics
            metrics_df = pd.DataFrame({
                'Metric': ['Steps', 'Time (seconds)', 'Complexity'],
                'Value': [metrics['steps'], f"{metrics['time']:.2f}", metrics['complexity']]
            })
            # Create Excel writer
            with pd.ExcelWriter('sudoku_solution.xlsx', engine='openpyxl') as writer:
                # Write all states to a single sheet, each state separated by a blank row and step label
                all_states = []
                for idx, state in enumerate(metrics['states']):
                    all_states.append([f"Step {idx+1}"] + [None]*8)
                    all_states.extend([list(row) for row in state])
                    all_states.append([None]*9)  # blank row
                states_df = pd.DataFrame(all_states)
                states_df.to_excel(writer, sheet_name='All States', index=False, header=False)
                metrics_df.to_excel(writer, sheet_name='Metrics', index=False)
                # Format the Excel file
                workbook = writer.book
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for row in worksheet.iter_rows():
                        for cell in row:
                            cell.alignment = openpyxl.styles.Alignment(horizontal='center')
                    if sheet_name == 'All States':
                        for col in worksheet.columns:
                            worksheet.column_dimensions[col[0].column_letter].width = 3
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False

    def get_complexity(self, algorithm_name):
        # Theoretical complexity for each algorithm
        complexities = {
            # Uninformed Search
            "Depth-First Search": "O(b^d)",
            "Breadth-First Search": "O(b^d)",
            "Uniform Cost Search": "O(b^(1 + floor(C/ε)))",
            "Iterative Deepening Search": "O(b^d)",
            
            # Informed Search
            "A* Search": "O(b^d)",
            "Greed Search": "O(b^d)",
            "IDA* Search": "O(b^d)",
            
            # Local Search
            "Simple Hill Climbing": "O(n)",
            "Steepest-Ascent Hill Climbing": "O(n)",
            "Stochastic Hill Climbing": "O(n)",
            "Simulated Annealing": "O(n)",
            "Local Beam Search": "O(k*n)",
            "Genetic Algorithm": "O(p*n*g)",
            
            # Complex Environment Search
            "AND-OR Graph Search": "O(b^d)",
            "Partial Observation Search": "O(|S|^2 * |O|)",
            
            # Constraint Satisfaction Problem
            "AC-3": "O(n²d³)",
            "Forward Checking": "O(d²n)",
            "Backtracking": "O(d^n)",
            
            # Reinforcement Learning
            "Q-Learning": "O(n * m)"  # n: states, m: actions
        }
        return complexities.get(algorithm_name, "Unknown")

    def depth_first_search(self, board):
        import numpy as np
        self.steps = 0
        self.states = []
        start_state = board.get_board_state()
        start_pos = board.find_empty()
        if not start_pos:
            return True
        stack = [(np.copy(start_state), start_pos)]
        visited = set()
        def get_state_key(state):
            return tuple(map(tuple, state))
        while stack:
            current_state, pos = stack.pop()
            board.set_board_state(current_state)
            self.steps += 1
            self.states.append(board.get_board_state().copy())
            if not pos:
                return True
            row, col = pos
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    new_state = np.copy(current_state)
                    new_state[row][col] = num
                    board.set_board_state(new_state)
                    next_pos = board.find_empty()
                    state_key = get_state_key(new_state)
                    if state_key not in visited:
                        visited.add(state_key)
                        stack.append((np.copy(new_state), next_pos))
        board.set_board_state(start_state)
        return False

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

    def iterative_deepening_search(self, board):
        import numpy as np
        self.steps = 0
        self.states = []
        start_state = board.get_board_state()
        start_pos = board.find_empty()
        if not start_pos:
            return True
        def get_state_key(state):
            return tuple(map(tuple, state))
        max_depth = 81  # Số ô tối đa của Sudoku
        for depth_limit in range(max_depth + 1):
            stack = [(np.copy(start_state), start_pos, 0)]  # (state, pos, depth)
            visited = set()
            while stack:
                current_state, pos, depth = stack.pop()
                board.set_board_state(current_state)
                self.steps += 1
                self.states.append(board.get_board_state().copy())
                if not pos:
                    return True
                if depth >= depth_limit:
                    continue
                row, col = pos
                for num in range(1, 10):
                    if board.is_valid_move(row, col, num):
                        new_state = np.copy(current_state)
                        new_state[row][col] = num
                        board.set_board_state(new_state)
                        next_pos = board.find_empty()
                        state_key = get_state_key(new_state)
                        if state_key not in visited:
                            visited.add(state_key)
                            stack.append((np.copy(new_state), next_pos, depth + 1))
        board.set_board_state(start_state)
        return False

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

    def greed_search(self, board):
        from queue import PriorityQueue
        import numpy as np
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
        if not start_pos:
            return True
        visited = set([get_state_key(start_state)])
        h_score = self.get_heuristic(board)
        pq.put(PrioritizedItem(h_score, (start_state, start_pos)))
        while not pq.empty():
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
            self.steps += 1
            current = pq.get().item
            current_state, pos = current
            board.set_board_state(current_state)
            self.states.append(board.get_board_state().copy())
            if not pos:
                return True
            row, col = pos
            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    new_state = np.copy(current_state)
                    new_state[row][col] = num
                    board.set_board_state(new_state)
                    next_pos = board.find_empty()
                    new_key = get_state_key(new_state)
                    if new_key not in visited:
                        visited.add(new_key)
                        h_score = self.get_heuristic(board)
                        pq.put(PrioritizedItem(h_score, (new_state, next_pos)))
        board.set_board_state(start_state)
        return False

    def ida_star_search(self, board):
        import numpy as np
        self.steps = 0
        self.states = []
        start_state = board.get_board_state()
        start_pos = board.find_empty()
        if not start_pos:
            return True
        def get_state_key(state):
            return tuple(map(tuple, state))
        bound = self.get_heuristic(board)
        while True:
            stack = [(np.copy(start_state), start_pos, 0)]  # (state, pos, g)
            visited = set()
            min_exceed = float('inf')
            while stack:
                current_state, pos, g = stack.pop()
                board.set_board_state(current_state)
                self.steps += 1
                self.states.append(board.get_board_state().copy())
                if not pos:
                    return True
                f = g + self.get_heuristic(board)
                if f > bound:
                    min_exceed = min(min_exceed, f)
                    continue
                row, col = pos
                for num in range(1, 10):
                    if board.is_valid_move(row, col, num):
                        new_state = np.copy(current_state)
                        new_state[row][col] = num
                        board.set_board_state(new_state)
                        next_pos = board.find_empty()
                        state_key = get_state_key(new_state)
                        if state_key not in visited:
                            visited.add(state_key)
                            stack.append((np.copy(new_state), next_pos, g + 1))
            if min_exceed == float('inf'):
                board.set_board_state(start_state)
                return False
            bound = min_exceed

    def simple_hill_climbing(self, board):
        def get_neighbors(state):
            neighbors = []
            for i in range(9):
                for j in range(9):
                    if state[i][j] == 0:
                        for num in range(1, 10):
                            if board.is_valid_move(i, j, num):
                                new_state = state.copy()
                                new_state[i][j] = num
                                neighbors.append(new_state)
            return neighbors
        
        current_state = board.get_board_state()
        while True:
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
            self.steps += 1
            
            current_cost = self.count_conflicts(board)
            if current_cost == 0:
                return True
            
            neighbors = get_neighbors(current_state)
            found_better_neighbor = False
            
            for neighbor in neighbors:
                board.set_board_state(neighbor)
                cost = self.count_conflicts(board)
                if cost < current_cost:
                    # Dừng ngay khi tìm thấy trạng thái tốt hơn đầu tiên
                    current_state = neighbor
                    found_better_neighbor = True
                    break
            
            if not found_better_neighbor:
                return False
            
            board.set_board_state(current_state)
            self.states.append(current_state.copy())

    def steepest_ascent_hill_climbing(self, board):
        def get_all_neighbors(state):
            neighbors = []
            for i in range(9):
                for j in range(9):
                    if state[i][j] == 0:
                        for num in range(1, 10):
                            if board.is_valid_move(i, j, num):
                                new_state = state.copy()
                                new_state[i][j] = num
                                neighbors.append(new_state)
            return neighbors
        
        current_state = board.get_board_state()
        while True:
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
            self.steps += 1
            
            current_cost = self.count_conflicts(board)
            if current_cost == 0:
                return True
            
            neighbors = get_all_neighbors(current_state)
            best_neighbor = None
            best_cost = current_cost
            
            for neighbor in neighbors:
                board.set_board_state(neighbor)
                cost = self.count_conflicts(board)
                if cost < best_cost:
                    best_cost = cost
                    best_neighbor = neighbor
            
            if best_neighbor is None:
                return False
            
            current_state = best_neighbor
            board.set_board_state(current_state)
            self.states.append(current_state.copy())

    def stochastic_hill_climbing(self, board):
        def get_random_neighbor(state):
            empty_cells = [(i, j) for i in range(9) for j in range(9) if state[i][j] == 0]
            if not empty_cells:
                return None
            
            i, j = random.choice(empty_cells)
            valid_numbers = [num for num in range(1, 10) if board.is_valid_move(i, j, num)]
            if not valid_numbers:
                return None
            
            new_state = state.copy()
            new_state[i][j] = random.choice(valid_numbers)
            return new_state
        
        current_state = board.get_board_state()
        while True:
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
            self.steps += 1
            
            current_cost = self.count_conflicts(board)
            if current_cost == 0:
                return True
            
            neighbor = get_random_neighbor(current_state)
            if neighbor is None:
                return False
            
            board.set_board_state(neighbor)
            neighbor_cost = self.count_conflicts(board)
            
            if neighbor_cost <= current_cost:
                current_state = neighbor
                self.states.append(current_state.copy())

    def simulated_annealing(self, board):
        def acceptance_probability(old_cost, new_cost, temperature):
            if new_cost < old_cost:
                return 1.0
            return math.exp((old_cost - new_cost) / temperature)
        
        def get_random_neighbor(state):
            empty_cells = [(i, j) for i in range(9) for j in range(9) if state[i][j] == 0]
            if not empty_cells:
                return None
            
            i, j = random.choice(empty_cells)
            valid_numbers = [num for num in range(1, 10) if board.is_valid_move(i, j, num)]
            if not valid_numbers:
                return None
            
            new_state = state.copy()
            new_state[i][j] = random.choice(valid_numbers)
            return new_state
        
        current_state = board.get_board_state()
        current_cost = self.count_conflicts(board)
        temperature = 1.0
        cooling_rate = 0.95
        
        while temperature > 0.01:
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
            self.steps += 1
            
            if current_cost == 0:
                return True
            
            neighbor = get_random_neighbor(current_state)
            if neighbor is None:
                return False
            
            board.set_board_state(neighbor)
            neighbor_cost = self.count_conflicts(board)
            
            if acceptance_probability(current_cost, neighbor_cost, temperature) > random.random():
                current_state = neighbor
                current_cost = neighbor_cost
                self.states.append(current_state.copy())
            
            temperature *= cooling_rate
        
        board.set_board_state(current_state)
        return current_cost == 0

    def local_beam_search(self, board):
        def get_neighbors(state):
            neighbors = []
            for i in range(9):
                for j in range(9):
                    if state[i][j] == 0:
                        for num in range(1, 10):
                            if board.is_valid_move(i, j, num):
                                new_state = state.copy()
                                new_state[i][j] = num
                                neighbors.append(new_state)
            return neighbors
        
        k = 5  # Number of states to maintain
        states = [board.get_board_state()]
        
        while True:
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
            self.steps += 1
            
            all_neighbors = []
            for state in states:
                board.set_board_state(state)
                if self.count_conflicts(board) == 0:
                    return True
                all_neighbors.extend(get_neighbors(state))
            
            # Evaluate all neighbors
            neighbors_with_cost = []
            for neighbor in all_neighbors:
                board.set_board_state(neighbor)
                cost = self.count_conflicts(board)
                neighbors_with_cost.append((cost, neighbor))
            
            # Select k best neighbors
            neighbors_with_cost.sort()
            states = [state for _, state in neighbors_with_cost[:k]]
            
            if not states:
                return False
            
            self.states.append(states[0].copy())

    def genetic_algorithm(self, board):
        def create_initial_population(size=50):
            """Tạo quần thể ban đầu với các cá thể là các trạng thái khả thi của bảng Sudoku"""
            population = []
            original_state = board.get_board_state().copy()
            
            for _ in range(size):
                # Đặt lại bảng về trạng thái ban đầu để tìm các vị trí hợp lệ
                board.set_board_state(original_state.copy())
                state = original_state.copy()
                
                # Điền các ô trống với giá trị hợp lệ
                empty_cells = [(i, j) for i in range(9) for j in range(9) if state[i][j] == 0]
                # Thử điền các ô theo thứ tự ngẫu nhiên
                random.shuffle(empty_cells)
                
                for i, j in empty_cells:
                    valid_numbers = [num for num in range(1, 10) if board.is_valid_move(i, j, num)]
                    if valid_numbers:
                        value = random.choice(valid_numbers)
                        state[i][j] = value
                        board.set_board_state(state.copy())
                
                population.append(state)
            
            # Đặt lại bảng về trạng thái ban đầu
            board.set_board_state(original_state)
            return population
        
        def fitness(state):
            """Tính điểm thích nghi dựa trên số lượng xung đột (càng ít xung đột càng tốt)"""
            board.set_board_state(state)
            conflicts = self.count_conflicts(board)
            
            # Bổ sung: tính thêm số ô trống để ưu tiên các trạng thái đã điền nhiều
            empty_cells = sum(1 for i in range(9) for j in range(9) if state[i][j] == 0)
            
            # Điểm càng cao càng tốt: -conflicts - empty_cells
            return -conflicts - empty_cells * 0.5
        
        def select_parents(fitness_scores, num_parents=10, tournament_size=5):
            """Chọn cha mẹ sử dụng phương pháp chọn lọc kiểu giải đấu (tournament selection)"""
            parents = []
            
            for _ in range(num_parents):
                # Chọn ngẫu nhiên tournament_size cá thể để tổ chức cuộc thi
                tournament = random.sample(fitness_scores, tournament_size)
                # Chọn cá thể có điểm cao nhất từ cuộc thi
                winner = max(tournament, key=lambda x: x[0])
                parents.append(winner[1])
                
            return parents
        
        def crossover(parent1, parent2):
            """Lai ghép hai cha mẹ để tạo con cái mới, giữ nguyên các giá trị từ bảng ban đầu"""
            original_state = board.get_board_state()
            child = original_state.copy()
            
            # Chỉ lai ghép các ô ban đầu trống
            for i in range(9):
                for j in range(9):
                    if original_state[i][j] == 0:
                        # Kiểm tra tính hợp lệ của các giá trị từ cả hai cha mẹ
                        board.set_board_state(child)
                        
                        p1_value = parent1[i][j]
                        p2_value = parent2[i][j]
                        
                        # Ưu tiên giá trị hợp lệ
                        child[i][j] = p1_value  # Mặc định từ parent1
                        
                        if not board.is_valid_move(i, j, p1_value) and board.is_valid_move(i, j, p2_value):
                            child[i][j] = p2_value  # Dùng giá trị từ parent2 nếu hợp lệ
                        elif random.random() < 0.5:  # 50% cơ hội đổi sang parent2
                            child[i][j] = p2_value
            
            return child
        
        def mutate(state, mutation_rate=0.1):
            """Đột biến một số ô ngẫu nhiên với xác suất mutation_rate"""
            original_state = board.get_board_state()
            mutated = state.copy()
            
            # Chỉ đột biến các ô ban đầu trống
            for i in range(9):
                for j in range(9):
                    if original_state[i][j] == 0 and random.random() < mutation_rate:
                        # Đặt lại bảng trước khi kiểm tra tính hợp lệ
                        board.set_board_state(mutated)
                        # Điền một giá trị hợp lệ khác
                        current_value = mutated[i][j]
                        valid_numbers = [num for num in range(1, 10) 
                                         if num != current_value and board.is_valid_move(i, j, num)]
                        
                        if valid_numbers:
                            mutated[i][j] = random.choice(valid_numbers)
            
            return mutated
        
        def create_new_generation(parents, population_size):
            """Tạo thế hệ mới từ các cha mẹ đã chọn"""
            # Elite selection: giữ lại các cá thể tốt nhất
            new_population = parents[:5].copy()
            
            # Tạo con cái mới cho đến khi đạt đủ kích thước quần thể
            while len(new_population) < population_size:
                # Chọn ngẫu nhiên hai cha mẹ khác nhau
                parent1, parent2 = random.sample(parents, 2)
                
                # Lai ghép
                child = crossover(parent1, parent2)
                
                # Đột biến
                child = mutate(child)
                
                new_population.append(child)
            
            return new_population
        
        # Tham số thuật toán
        population_size = 50
        max_generations = 1000
        stagnation_limit = 50  # Giới hạn số thế hệ không cải thiện
        
        # Lưu trạng thái ban đầu
        original_state = board.get_board_state().copy()
        
        # Tạo quần thể ban đầu
        population = create_initial_population(population_size)
        generation = 0
        best_fitness = float('-inf')
        stagnation_counter = 0
        
        # Theo dõi cá thể tốt nhất qua các thế hệ
        best_individual = None
        
        while generation < max_generations and stagnation_counter < stagnation_limit:
            if self.cancel_flag():
                # Đặt lại bảng về trạng thái ban đầu trước khi thoát
                board.set_board_state(original_state)
                return False
                
            if time.time() - self.start_time > self.timeout:
                # Đặt lại bảng về trạng thái ban đầu trước khi thoát
                board.set_board_state(original_state)
                return False
                
            self.steps += 1
            
            # Đánh giá độ thích nghi
            fitness_scores = [(fitness(state), state) for state in population]
            fitness_scores.sort(reverse=True)
            
            # Theo dõi tiến độ
            current_best_fitness = fitness_scores[0][0]
            current_best_individual = fitness_scores[0][1]
            
            # Thêm trạng thái tốt nhất vào danh sách để hiển thị
            self.states.append(current_best_individual.copy())
            
            # Kiểm tra xem đã tìm được lời giải chưa
            board.set_board_state(current_best_individual)
            if self.count_conflicts(board) == 0 and not board.find_empty():
                # Đã tìm được lời giải
                return True
            
            # Kiểm tra sự cải thiện
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            
            # Chọn cha mẹ
            parents = select_parents(fitness_scores, num_parents=15, tournament_size=5)
            
            # Tạo thế hệ mới
            population = create_new_generation(parents, population_size)
            
            generation += 1
        
        # Đặt lại bảng thành cá thể tốt nhất tìm được
        if best_individual is not None:
            board.set_board_state(best_individual)
            
            # Kiểm tra một lần cuối xem có phải là lời giải hoàn chỉnh không
            if self.count_conflicts(board) == 0 and not board.find_empty():
                return True
        
        # Đặt lại bảng về trạng thái ban đầu nếu không tìm được lời giải
        board.set_board_state(original_state)
        return False

    def and_or_graph_search(self, board):
        """Solve Sudoku using AND-OR Graph Search algorithm, handling multiple sub-problems
        in a deterministic environment where:
        - OR nodes: different ways to fill an empty cell
        - AND nodes: all empty cells must be filled
        """
        # Lưu trữ memoization để tránh tính toán lại các trạng thái đã thăm
        memo = {}
        
        def get_state_key(state):
            return tuple(map(tuple, state))
        
        def find_all_empty_positions(state):
            """Tìm tất cả các vị trí trống trong bảng Sudoku"""
            empty_positions = []
            for i in range(9):
                for j in range(9):
                    if state[i][j] == 0:
                        empty_positions.append((i, j))
            return empty_positions
            
        def or_search(state, goal_test):
            """Xử lý nút OR: tìm một trong các cách để điền vào một ô trống cụ thể"""
            if self.cancel_flag():
                return False, None
            if time.time() - self.start_time > self.timeout:
                return False, None
            
            state_key = get_state_key(state)
            
            # Kiểm tra nếu trạng thái đã được tính toán trước đó
            if state_key in memo:
                return memo[state_key]
            
            self.steps += 1
            self.states.append(state.copy())
            
            # Kiểm tra nếu đã giải quyết được bài toán
            if goal_test(state):
                return True, []
            
            empty_pos = board.find_empty()
            if not empty_pos:
                return True, []  # Không còn ô trống nào
            
            # Xử lý nút OR: chọn một giá trị cho ô trống hiện tại
            row, col = empty_pos
            
            for num in range(1, 10):
                board.set_board_state(state)
                if board.is_valid_move(row, col, num):
                    # Tạo trạng thái mới với giá trị đã điền
                    new_state = state.copy()
                    new_state[row][col] = num
                    
                    # Đệ quy để giải tất cả các ô trống còn lại (AND node)
                    result, sub_plan = and_search(new_state, goal_test)
                    
                    if result:
                        # Tìm thấy lời giải
                        plan = [("Fill", row, col, num)]
                        if sub_plan:
                            plan.extend(sub_plan)
                        memo[state_key] = (True, plan)
                        return True, plan
            
            # Không tìm thấy lời giải
            memo[state_key] = (False, None)
            return False, None
            
        def and_search(state, goal_test):
            """Xử lý nút AND: giải tất cả các ô trống còn lại"""
            if self.cancel_flag():
                return False, None
            if time.time() - self.start_time > self.timeout:
                return False, None
                
            state_key = get_state_key(state)
            
            # Kiểm tra nếu trạng thái đã được tính toán trước đó
            if state_key in memo:
                return memo[state_key]
            
            # Kiểm tra nếu đã giải quyết được bài toán
            if goal_test(state):
                return True, []
            
            empty_pos = board.find_empty()
            if not empty_pos:
                return True, []  # Không còn ô trống nào
            
            # Đệ quy để giải OR node (chọn giá trị cho ô trống)
            result, plan = or_search(state, goal_test)
            
            if result:
                memo[state_key] = (True, plan)
                return True, plan
            
            # Không tìm thấy lời giải
            memo[state_key] = (False, None)
            return False, None
            
        def goal_test(state):
            """Kiểm tra xem bảng Sudoku đã được giải hoàn toàn chưa"""
            board.set_board_state(state)
            for i in range(9):
                for j in range(9):
                    if board.get_value(i, j) == 0:
                        return False
                    # Kiểm tra tính hợp lệ
                    value = board.get_value(i, j)
                    board.set_value(i, j, 0)  # Tạm thời xóa giá trị
                    is_valid = board.is_valid_move(i, j, value)
                    board.set_value(i, j, value)  # Đặt lại giá trị
                    if not is_valid:
                        return False
            return True
            
        # Bắt đầu thuật toán AND-OR Search với trạng thái hiện tại
        start_state = board.get_board_state()
        result, plan = and_search(start_state, goal_test)
        
        if result:
            # Áp dụng kế hoạch để tìm ra lời giải
            board.set_board_state(start_state)
            for action in plan:
                action_type, row, col, value = action
                board.set_value(row, col, value)
        
        return result

    def get_heuristic(self, board):
        # Count the number of empty cells as a heuristic
        empty_count = 0
        for i in range(9):
            for j in range(9):
                if board.get_value(i, j) == 0:
                    empty_count += 1
        return empty_count

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

    def ac3_solver(self, board):
        """Solve Sudoku using AC-3 algorithm"""
        self.steps = 0
        self.start_state = board.get_board_state()
        self.states = [self.start_state.copy()]
        
        start_time = time.time()
        result = ac3(board)
        end_time = time.time()
        
        if result:
            self.target_state = board.get_board_state()
            metrics = {
                "steps": self.steps,
                "time": end_time - start_time,
                "complexity": "O(n²d³)",
                "start_state": self.start_state,
                "target_state": self.target_state,
                "states": self.states
            }
            self.export_to_excel(metrics)
            return metrics
        return None

    def forward_checking_solver(self, board):
        """Solve Sudoku using Forward Checking"""
        self.steps = 0
        self.start_state = board.get_board_state()
        self.states = [self.start_state.copy()]
        
        start_time = time.time()
        # Use forward checking with backtracking
        pos = board.find_empty()
        if pos:
            row, col = pos
            for value in range(1, 10):
                if forward_checking(board, (row, col), value):
                    board.set_value(row, col, value)
                    self.states.append(board.get_board_state().copy())
                    if self.forward_checking_solver(board):
                        end_time = time.time()
                        self.target_state = board.get_board_state()
                        metrics = {
                            "steps": self.steps,
                            "time": end_time - start_time,
                            "complexity": "O(d²n)",
                            "start_state": self.start_state,
                            "target_state": self.target_state,
                            "states": self.states
                        }
                        self.export_to_excel(metrics)
                        return metrics
                    board.set_value(row, col, 0)
                    self.states.append(board.get_board_state().copy())
        else:
            end_time = time.time()
            self.target_state = board.get_board_state()
            metrics = {
                "steps": self.steps,
                "time": end_time - start_time,
                "complexity": "O(d²n)",
                "start_state": self.start_state,
                "target_state": self.target_state,
                "states": self.states
            }
            self.export_to_excel(metrics)
            return metrics
        return None

    def backtracking_solver(self, board):
        """Solve Sudoku using Backtracking with Forward Checking"""
        self.steps = 0
        self.start_state = board.get_board_state()
        self.states = [self.start_state.copy()]
        
        start_time = time.time()
        result = backtracking_search(board)
        end_time = time.time()
        
        if result:
            self.target_state = board.get_board_state()
            metrics = {
                "steps": self.steps,
                "time": end_time - start_time,
                "complexity": "O(d^n)",
                "start_state": self.start_state,
                "target_state": self.target_state,
                "states": self.states
            }
            self.export_to_excel(metrics)
            return metrics
        return None

    def q_learning_solver(self, board):
        """Solve Sudoku using Q-Learning"""
        self.steps = 0
        self.start_state = board.get_board_state()
        self.states = [self.start_state.copy()]
        
        start_time = time.time()
        
        # Reset rewards tracking
        total_reward = 0
        
        # Modified solve method to track more data
        steps = 0
        while steps < 1000:  # Max steps
            current_pos = board.find_empty()
            if not current_pos:
                break  # Puzzle solved
                
            state_key = self.q_learning.get_state_key(board)
            valid_actions = self.q_learning.get_valid_actions(board, current_pos)
            
            if not valid_actions:
                break  # No valid moves
                
            # Choose and take action
            action = self.q_learning.choose_action(state_key, valid_actions)
            if action is None:
                break
                
            # Apply action
            row, col = current_pos
            board.set_value(row, col, action)
            
            # Get reward and next state
            reward = self.q_learning.get_reward(board)
            next_state_key = self.q_learning.get_state_key(board)
            
            # Update Q-table
            self.q_learning.update(state_key, action, reward, next_state_key)
            
            # Track total reward
            total_reward += reward
            
            # Store board state for visualization
            self.states.append(board.get_board_state().copy())
            
            # If move leads to invalid state, undo it
            if reward < 0:
                board.set_value(row, col, 0)
                
            self.steps += 1
            steps += 1
            
            if self.cancel_flag():
                return False
            if time.time() - self.start_time > self.timeout:
                return False
        
        result = not board.find_empty()  # True if solved
        end_time = time.time()
        
        if result:
            self.target_state = board.get_board_state()
            metrics = {
                "steps": self.steps,
                "time": end_time - start_time,
                "complexity": "O(n * m)",  # n: states, m: actions
                "start_state": self.start_state,
                "target_state": self.target_state,
                "states": self.states,
                "total_reward": total_reward  # Add total reward to metrics
            }
            self.export_to_excel(metrics)
            return metrics
        return None

    def partial_observation_search(self, board):
        """Solve Sudoku using Partial Observation Search"""
        # Initialize observations and hidden cells
        self.observations = {}
        visible_prob = 0.7  # Probability of a cell being visible
        self.hidden_cells = set()
        
        # Make initial observation - some cells are hidden
        initial_state = board.get_board_state()
        for i in range(9):
            for j in range(9):
                if initial_state[i][j] != 0 and random.random() > visible_prob:
                    self.hidden_cells.add((i, j))
        
        self.states = [initial_state.copy()]
        
        def make_observation(state):
            """Return the state with hidden cells obscured"""
            obs = state.copy()
            for i, j in self.hidden_cells:
                if state[i][j] != 0:
                    obs[i][j] = 0  # Hide this cell
            return obs
        
        def get_observation_probability(state, observation):
            """Calculate probability of observation given state"""
            # In this simplified model, observation is deterministic based on hidden cells
            for i in range(9):
                for j in range(9):
                    if (i, j) not in self.hidden_cells and state[i][j] != observation[i][j]:
                        return 0.0
            return 1.0
        
        def update_belief(belief, action, observation):
            """Update belief state based on action and observation"""
            new_belief = {}
            total_prob = 0.0
            
            for state, prob in belief.items():
                if action:
                    # Apply action to state
                    row, col, value = action
                    new_state = np.array(state)
                    new_state[row][col] = value
                    new_state_tuple = tuple(map(tuple, new_state))
                else:
                    new_state_tuple = state
                
                # Calculate observation probability
                o_prob = get_observation_probability(new_state_tuple, observation)
                # Nếu prob = 0 thì new_state không thể tạo được môi trường quan sát nên sẽ loại
                if o_prob > 0.0:
                    new_belief[new_state_tuple] = prob * o_prob
                    total_prob += prob * o_prob
            
            # Normalize belief
            if total_prob > 0.0:
                for state in new_belief:
                    new_belief[state] /= total_prob
            
            return new_belief
        
        def is_board_solved(board_state):
            """Check if the Sudoku board is solved"""
            # Check if all cells are filled
            for i in range(9):
                for j in range(9):
                    if board_state[i][j] == 0:
                        return False
                        
            # Check rows
            for row in board_state:
                if sorted(row) != list(range(1, 10)):
                    return False
                    
            # Check columns
            for j in range(9):
                col = [board_state[i][j] for i in range(9)]
                if sorted(col) != list(range(1, 10)):
                    return False
                    
            # Check boxes
            for box_i in range(3):
                for box_j in range(3):
                    box = [board_state[box_i*3 + i][box_j*3 + j] 
                          for i in range(3) for j in range(3)]
                    if sorted(box) != list(range(1, 10)):
                        return False
                        
            return True
        
        def search_with_partial_observation(board, max_steps=100):
            """Main search algorithm with partial observability"""
            self.steps = 0
            
            # Initial belief state - only one state with probability 1.0
            belief = {tuple(map(tuple, initial_state)): 1.0}
            
            # Store initial observation
            observation = make_observation(initial_state)
            self.observations[0] = observation
            
            while self.steps < max_steps:
                if self.cancel_flag():
                    return False
                if time.time() - self.start_time > self.timeout:
                    return False
                
                # Get most likely state from belief
                most_likely_state = max(belief, key=belief.get)
                board.set_board_state(np.array(most_likely_state))
                
                # Find empty cell in observation
                empty_cell = None
                for i in range(9):
                    for j in range(9):
                        if observation[i][j] == 0:
                            empty_cell = (i, j)
                            break
                    if empty_cell:
                        break
                
                if not empty_cell:
                    # If no empty cells in observation, try to reveal a hidden cell
                    if self.hidden_cells:
                        empty_cell = random.choice(list(self.hidden_cells))
                        # Reveal this cell
                        self.hidden_cells.remove(empty_cell)
                        observation = make_observation(np.array(most_likely_state))
                        self.observations[self.steps] = observation.copy()
                    else:
                        # No more hidden cells, and no empty cells - check if solution is valid
                        board_state = board.get_board_state()
                        if is_board_solved(board_state):
                            return True
                        else:
                            return False
                
                if empty_cell:
                    row, col = empty_cell
                    # Try to place a valid number
                    valid_actions = []
                    for num in range(1, 10):
                        if board.is_valid_move(row, col, num):
                            valid_actions.append((row, col, num))
                    
                    if valid_actions:
                        # Choose a random valid action
                        action = random.choice(valid_actions)
                        row, col, value = action
                        
                        # Apply action and update belief
                        board.set_value(row, col, value)
                        new_state = board.get_board_state()
                        self.states.append(new_state.copy())
                        
                        # Make new observation after action
                        observation = make_observation(new_state)
                        self.observations[self.steps + 1] = observation.copy()
                        
                        # Update belief based on observation
                        belief = update_belief(belief, action, observation)
                    else:
                        # No valid actions for this cell in the most likely state
                        # This is a failure path, we need to backtrack
                        if len(self.states) > 1:
                            self.states.pop()  # Remove last state
                            prev_state = self.states[-1]
                            board.set_board_state(prev_state)
                            observation = make_observation(prev_state)
                            # Clear belief and start with previous state
                            belief = {tuple(map(tuple, prev_state)): 1.0}
                        else:
                            return False
                
                self.steps += 1
            
            # Check if solution is valid after max steps
            board_state = board.get_board_state()
            return is_board_solved(board_state)
        
        return search_with_partial_observation(board) 