import numpy as np
import random
from utils.constants import BOARD_SIZE, DIFFICULTY_LEVELS

class SudokuBoard:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.original_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.initial_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.difficulty = "Easy"
        self.generate_puzzle()

    def generate_puzzle(self):
        # Generate a solved board
        self.generate_solved_board()
        
        # Create a puzzle by removing numbers
        self.create_puzzle_from_solution()
        
        # Save the initial state
        self.initial_board = self.board.copy()
        self.original_board = self.board.copy()

    def generate_solved_board(self):
        """Generate a completely solved Sudoku board"""
        # Start with an empty board
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        
        # Use backtracking to fill the board
        self._solve_board()
        
    def _solve_board(self):
        """Use backtracking to solve the board"""
        empty = self.find_empty()
        if not empty:
            return True
            
        row, col = empty
        # Shuffle numbers for randomness
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                
                if self._solve_board():
                    return True
                    
                self.board[row][col] = 0
                
        return False

    def create_puzzle_from_solution(self):
        """Create a puzzle by removing numbers from a solved board"""
        # Start with a solved board
        solution = self.board.copy()
        
        # Determine how many cells to keep based on difficulty
        cells_to_keep = DIFFICULTY_LEVELS.get(self.difficulty, 25)
        
        # Create a list of all positions
        positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        random.shuffle(positions)
        
        # Keep only a subset of cells
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(cells_to_keep):
            if i < len(positions):
                row, col = positions[i]
                self.board[row][col] = solution[row][col]
        
        # Save the original board
        self.original_board = self.board.copy()

    def reset_to_initial(self):
        """Reset the board to its initial state"""
        self.board = self.initial_board.copy()

    def new_game(self, difficulty=None):
        """Start a new game with a different puzzle"""
        if difficulty == "Random":
            # Generate a random number of cells to keep (between 20 and 35)
            cells_to_keep = random.randint(20, 35)
            
            # Generate a solved board
            self.generate_solved_board()
            solution = self.board.copy()
            
            # Create a list of all positions
            positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
            random.shuffle(positions)
            
            # Keep only a random subset of cells
            self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
            for i in range(cells_to_keep):
                if i < len(positions):
                    row, col = positions[i]
                    self.board[row][col] = solution[row][col]
            
            # Save the initial state
            self.initial_board = self.board.copy()
            self.original_board = self.board.copy()
        elif difficulty:
            self.difficulty = difficulty
            self.generate_puzzle()
        else:
            # Clear the board for manual input
            self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
            self.original_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
            self.initial_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    def is_valid_move(self, row, col, num):
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in self.board[:, col]:
            return False

        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        box = self.board[box_row:box_row + 3, box_col:box_col + 3]
        if num in box:
            return False

        return True

    def find_empty(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def set_value(self, row, col, value):
        if self.original_board[row][col] == 0:
            if value == 0 or self.is_valid_move(row, col, value):
                self.board[row][col] = value

    def get_value(self, row, col):
        return self.board[row][col]

    def is_original(self, row, col):
        return self.original_board[row][col] != 0

    def is_complete(self):
        return 0 not in self.board

    def get_board_state(self):
        return self.board.copy()

    def set_board_state(self, state):
        self.board = state.copy()

    def is_valid_board(self):
        """Check if the current board state is valid and can be solved"""
        # Check if current state is valid
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] != 0:
                    # Temporarily remove the number to check if it's valid
                    num = self.board[i][j]
                    self.board[i][j] = 0
                    if not self.is_valid_move(i, j, num):
                        self.board[i][j] = num
                        return False
                    self.board[i][j] = num
        
        # Try to solve a copy of the board
        board_copy = self.board.copy()
        result = self._check_solvable()
        self.board = board_copy
        return result
        
    def _check_solvable(self):
        """Check if the current board state can be solved"""
        empty = self.find_empty()
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                
                if self._check_solvable():
                    return True
                    
                self.board[row][col] = 0
                
        return False 