import numpy as np
import random

class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.q_table = {}  # State-action value table
        self.lr = learning_rate  # Learning rate
        self.gamma = discount_factor  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        
    def get_state_key(self, board):
        """Convert board state to a hashable key"""
        return tuple(map(tuple, board.get_board_state()))
        
    def get_valid_actions(self, board, pos):
        """Get list of valid values for a position"""
        if not pos:
            return []
        row, col = pos
        return [num for num in range(1, 10) if board.is_valid_move(row, col, num)]
        
    def get_reward(self, board):
        """Calculate reward based on number of filled cells and conflicts"""
        filled_cells = sum(1 for i in range(9) for j in range(9) 
                         if board.get_value(i, j) != 0)
        conflicts = sum(1 for i in range(9) for j in range(9)
                       for num in range(1, 10)
                       if board.get_value(i, j) == num
                       and not board.is_valid_move(i, j, num))
        return filled_cells - (conflicts * 2)
        
    def choose_action(self, state_key, valid_actions):
        """Choose action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return random.choice(valid_actions) if valid_actions else None
            
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in range(1, 10)}
            
        q_values = self.q_table[state_key]
        max_q = max(q_values[action] for action in valid_actions) if valid_actions else -float('inf')
        best_actions = [action for action in valid_actions if q_values[action] == max_q]
        return random.choice(best_actions) if best_actions else None
        
    def update(self, state, action, reward, next_state):
        """Update Q-value using Q-learning update rule"""
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in range(1, 10)}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in range(1, 10)}
            
        # Get maximum Q-value for next state
        next_max = max(self.q_table[next_state].values())
        
        # Update Q-value
        self.q_table[state][action] = (1 - self.lr) * self.q_table[state][action] + \
                                     self.lr * (reward + self.gamma * next_max)
                                     
    def solve(self, board, max_steps=1000):
        """Solve Sudoku using Q-learning"""
        steps = 0
        while steps < max_steps:
            current_pos = board.find_empty()
            if not current_pos:
                return True  # Puzzle solved
                
            state_key = self.get_state_key(board)
            valid_actions = self.get_valid_actions(board, current_pos)
            
            if not valid_actions:
                return False  # No valid moves
                
            # Choose and take action
            action = self.choose_action(state_key, valid_actions)
            if action is None:
                return False
                
            # Apply action
            row, col = current_pos
            board.set_value(row, col, action)
            
            # Get reward and next state
            reward = self.get_reward(board)
            next_state_key = self.get_state_key(board)
            
            # Update Q-table
            self.update(state_key, action, reward, next_state_key)
            
            # If move leads to invalid state, undo it
            if reward < 0:
                board.set_value(row, col, 0)
                
            steps += 1
            
        return False  # Max steps reached 