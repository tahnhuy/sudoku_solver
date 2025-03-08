import pygame
import sys
import random
from game.sudoku_board import SudokuBoard
from game.gui import GUI
from algorithms.algorithm_manager import AlgorithmManager
from utils.constants import *

class SudokuGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()
        
        # Set random seed for reproducibility
        random.seed()
        
        self.board = SudokuBoard()
        self.gui = GUI(self.screen)
        self.algorithm_manager = AlgorithmManager()
        
        self.selected_cell = None
        self.solving = False
        self.show_metrics = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = pygame.mouse.get_pos()
                    self.gui.handle_click(x, y, self.board, self.algorithm_manager)
                    self.selected_cell = self.gui.get_selected_cell()
                elif event.button in [4, 5]:  # Mouse wheel
                    self.gui.handle_mouse_wheel(event.button == 4 and 1 or -1)
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    self.gui.handle_mouse_up()
                
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left button held
                    self.gui.handle_scroll(event.pos[1])
                
            if event.type == pygame.KEYDOWN and not self.solving:
                if self.selected_cell:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                   pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        num = int(event.unicode)
                        row, col = self.selected_cell
                        self.board.set_value(row, col, num)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        row, col = self.selected_cell
                        self.board.set_value(row, col, 0)
                
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            self.screen.fill(WHITE)
            self.gui.draw(self.board, self.algorithm_manager)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SudokuGame()
    game.run() 