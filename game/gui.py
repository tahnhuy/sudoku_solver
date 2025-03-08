import pygame
from utils.constants import *

class GUI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.category_font = pygame.font.Font(None, CATEGORY_FONT_SIZE)
        self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        self.metrics_font = pygame.font.Font(None, METRICS_FONT_SIZE)
        self.solve_font = pygame.font.Font(None, SOLVE_BUTTON_FONT_SIZE)
        self.error_font = pygame.font.Font(None, ERROR_FONT_SIZE)
        
        self.selected_cell = None
        self.selected_algorithm = None
        self.metrics = None
        self.scroll_y = 0
        self.max_scroll = 0
        self.dragging_scroll = False
        
        # Calculate board position to center it
        self.board_x = (WINDOW_WIDTH - PANEL_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
        self.board_y = BOARD_PADDING
        
        # Right panel position
        self.panel_x = WINDOW_WIDTH - PANEL_WIDTH
        
        # Create solve button under the Sudoku board
        self.solve_button = pygame.Rect(
            self.board_x + (BOARD_SIZE * CELL_SIZE - SOLVE_BUTTON_WIDTH) // 2,
            self.board_y + BOARD_SIZE * CELL_SIZE + SOLVE_BUTTON_MARGIN,
            SOLVE_BUTTON_WIDTH,
            SOLVE_BUTTON_HEIGHT
        )
        
        # Create Reset and New Game buttons
        self.reset_button = pygame.Rect(
            self.board_x,
            self.board_y + BOARD_SIZE * CELL_SIZE + SOLVE_BUTTON_MARGIN,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )
        
        self.new_game_button = pygame.Rect(
            self.board_x + BOARD_SIZE * CELL_SIZE - CONTROL_BUTTON_WIDTH,
            self.board_y + BOARD_SIZE * CELL_SIZE + SOLVE_BUTTON_MARGIN,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )

    def draw_board(self, board):
        # Draw board background
        board_rect = pygame.Rect(
            self.board_x - BOARD_PADDING,
            self.board_y - BOARD_PADDING,
            BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING,
            BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
        )
        pygame.draw.rect(self.screen, LIGHT_GRAY, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 2)

        # Draw the grid
        for i in range(BOARD_SIZE + 1):
            line_width = 3 if i % 3 == 0 else 1
            # Vertical lines
            pygame.draw.line(self.screen, BLACK,
                           (self.board_x + i * CELL_SIZE, self.board_y),
                           (self.board_x + i * CELL_SIZE, self.board_y + BOARD_SIZE * CELL_SIZE),
                           line_width)
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK,
                           (self.board_x, self.board_y + i * CELL_SIZE),
                           (self.board_x + BOARD_SIZE * CELL_SIZE, self.board_y + i * CELL_SIZE),
                           line_width)

        # Draw numbers and highlight selected cell
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell_rect = pygame.Rect(
                    self.board_x + j * CELL_SIZE,
                    self.board_y + i * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                # Highlight selected cell
                if self.selected_cell == (i, j):
                    pygame.draw.rect(self.screen, LIGHT_BLUE, cell_rect)
                
                if board.get_value(i, j) != 0:
                    color = DARK_BLUE if board.is_original(i, j) else BLACK
                    number = self.button_font.render(str(board.get_value(i, j)), True, color)
                    x = self.board_x + j * CELL_SIZE + (CELL_SIZE - number.get_width()) // 2
                    y = self.board_y + i * CELL_SIZE + (CELL_SIZE - number.get_height()) // 2
                    self.screen.blit(number, (x, y))
                    
        # Draw control buttons
        # Reset button
        pygame.draw.rect(self.screen, LIGHT_BLUE, self.reset_button)
        pygame.draw.rect(self.screen, BLACK, self.reset_button, 1)
        reset_text = self.button_font.render("Reset", True, BLACK)
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)
        
        # New Game button
        pygame.draw.rect(self.screen, ORANGE, self.new_game_button)
        pygame.draw.rect(self.screen, BLACK, self.new_game_button, 1)
        new_game_text = self.button_font.render("New Game", True, BLACK)
        new_game_rect = new_game_text.get_rect(center=self.new_game_button.center)
        self.screen.blit(new_game_text, new_game_rect)

    def draw_algorithm_buttons(self):
        # Draw right panel background
        panel_rect = pygame.Rect(self.panel_x, 0, PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, panel_rect)
        pygame.draw.line(self.screen, BLACK, (self.panel_x, 0), (self.panel_x, WINDOW_HEIGHT), 2)

        # Draw title
        title = self.title_font.render("Algorithm Selection", True, BLACK)
        title_x = self.panel_x + (PANEL_WIDTH - title.get_width()) // 2
        self.screen.blit(title, (title_x, PANEL_TOP_PADDING))

        # Create a surface for the scrollable content
        content_height = 0
        for category, algorithms in ALGORITHMS.items():
            content_height += (CATEGORY_PADDING * 2 + CATEGORY_TITLE_HEIGHT + 
                             len(algorithms) * (BUTTON_HEIGHT + BUTTON_PADDING))

        self.max_scroll = max(0, content_height - ALGO_PANEL_HEIGHT)
        
        # Create subsurface for clipping
        algo_panel_rect = pygame.Rect(
            self.panel_x,
            PANEL_TOP_PADDING + title.get_height() + 10,
            PANEL_WIDTH - SCROLL_BAR_WIDTH - SCROLL_PADDING,
            ALGO_PANEL_HEIGHT
        )
        
        # Draw scrollable content
        y_offset = -self.scroll_y
        for category, algorithms in ALGORITHMS.items():
            if (y_offset + CATEGORY_TITLE_HEIGHT > -ALGO_PANEL_HEIGHT and 
                y_offset < ALGO_PANEL_HEIGHT):
                # Draw category background
                category_height = (CATEGORY_TITLE_HEIGHT + CATEGORY_PADDING + 
                                (BUTTON_HEIGHT + BUTTON_PADDING) * len(algorithms))
                category_rect = pygame.Rect(
                    self.panel_x + PANEL_PADDING // 2,
                    algo_panel_rect.top + y_offset,
                    PANEL_WIDTH - PANEL_PADDING - SCROLL_BAR_WIDTH - SCROLL_PADDING,
                    category_height
                )
                
                # Only draw if category is visible
                if (category_rect.bottom > algo_panel_rect.top and 
                    category_rect.top < algo_panel_rect.bottom):
                    pygame.draw.rect(self.screen, CATEGORY_COLORS[category], category_rect)
                    pygame.draw.rect(self.screen, GRAY, category_rect, 1)

                    # Draw category name
                    category_text = self.category_font.render(category, True, BLACK)
                    text_rect = category_text.get_rect(
                        centerx=category_rect.centerx,
                        top=category_rect.top + CATEGORY_PADDING // 2
                    )
                    if text_rect.bottom > algo_panel_rect.top and text_rect.top < algo_panel_rect.bottom:
                        self.screen.blit(category_text, text_rect)

            y_offset += CATEGORY_PADDING + CATEGORY_TITLE_HEIGHT

            # Draw algorithm buttons
            for algorithm in algorithms:
                if y_offset > -BUTTON_HEIGHT and y_offset < ALGO_PANEL_HEIGHT:
                    button_rect = pygame.Rect(
                        self.panel_x + PANEL_PADDING,
                        algo_panel_rect.top + y_offset,
                        BUTTON_WIDTH,
                        BUTTON_HEIGHT
                    )
                    
                    if button_rect.bottom > algo_panel_rect.top and button_rect.top < algo_panel_rect.bottom:
                        color = LIGHT_BLUE if algorithm == self.selected_algorithm else WHITE
                        pygame.draw.rect(self.screen, color, button_rect)
                        pygame.draw.rect(self.screen, BLACK, button_rect, 1)
                        
                        text = self.button_font.render(algorithm, True, BLACK)
                        text_rect = text.get_rect(center=button_rect.center)
                        self.screen.blit(text, text_rect)

                y_offset += BUTTON_HEIGHT + BUTTON_PADDING
            y_offset += CATEGORY_PADDING

        # Draw scroll bar
        scroll_bar_rect = pygame.Rect(
            self.panel_x + PANEL_WIDTH - SCROLL_BAR_WIDTH - SCROLL_PADDING,
            algo_panel_rect.top,
            SCROLL_BAR_WIDTH,
            ALGO_PANEL_HEIGHT
        )
        pygame.draw.rect(self.screen, SCROLL_BAR_COLOR, scroll_bar_rect)

        if self.max_scroll > 0:
            thumb_height = max(30, ALGO_PANEL_HEIGHT * ALGO_PANEL_HEIGHT / content_height)
            thumb_pos = (self.scroll_y / self.max_scroll) * (ALGO_PANEL_HEIGHT - thumb_height)
            thumb_rect = pygame.Rect(
                scroll_bar_rect.x,
                scroll_bar_rect.y + thumb_pos,
                SCROLL_BAR_WIDTH,
                thumb_height
            )
            pygame.draw.rect(self.screen, SCROLL_THUMB_COLOR, thumb_rect)

        # Draw solve button with shadow effect
        shadow_offset = 3
        shadow_rect = self.solve_button.copy()
        shadow_rect.move_ip(shadow_offset, shadow_offset)
        pygame.draw.rect(self.screen, GRAY, shadow_rect)
        
        color = GREEN if self.selected_algorithm else GRAY
        pygame.draw.rect(self.screen, color, self.solve_button)
        pygame.draw.rect(self.screen, BLACK, self.solve_button, 2)
        
        solve_text = self.solve_font.render("Solve", True, BLACK)
        solve_rect = solve_text.get_rect(center=self.solve_button.center)
        self.screen.blit(solve_text, solve_rect)

    def draw_metrics(self):
        if self.metrics:
            # Draw metrics background
            metrics_rect = pygame.Rect(
                self.board_x - BOARD_PADDING,
                self.solve_button.bottom + METRICS_TOP_PADDING,
                BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING,
                METRICS_HEIGHT
            )
            pygame.draw.rect(self.screen, LIGHT_GRAY, metrics_rect)
            pygame.draw.rect(self.screen, BLACK, metrics_rect, 1)

            metrics_x = metrics_rect.left + 20
            y_offset = metrics_rect.top + 15
            
            metrics_list = [
                f"Steps: {self.metrics['steps']}",
                f"Time: {self.metrics['time']:.2f}s",
                f"Complexity: {self.metrics['complexity']}",
            ]
            
            for metric in metrics_list:
                text = self.metrics_font.render(metric, True, BLACK)
                self.screen.blit(text, (metrics_x, y_offset))
                y_offset += 30

    def draw(self, board, algorithm_manager):
        self.screen.fill(WHITE)
        self.draw_board(board)
        self.draw_algorithm_buttons()
        self.draw_metrics()
        pygame.display.flip()

    def handle_click(self, x, y, board, algorithm_manager):
        # Check if click is on the board
        board_rect = pygame.Rect(
            self.board_x,
            self.board_y,
            BOARD_SIZE * CELL_SIZE,
            BOARD_SIZE * CELL_SIZE
        )
        
        if board_rect.collidepoint(x, y):
            col = (x - self.board_x) // CELL_SIZE
            row = (y - self.board_y) // CELL_SIZE
            self.selected_cell = (row, col)
            return

        # Check if click is on reset button
        if self.reset_button.collidepoint(x, y):
            board.reset_to_initial()
            self.metrics = None
            return
            
        # Check if click is on new game button
        if self.new_game_button.collidepoint(x, y):
            board.new_game()
            self.metrics = None
            self.selected_cell = None
            return

        # Check if click is on scroll bar
        scroll_bar_rect = pygame.Rect(
            self.panel_x + PANEL_WIDTH - SCROLL_BAR_WIDTH - SCROLL_PADDING,
            PANEL_TOP_PADDING + self.title_font.get_height() + 10,
            SCROLL_BAR_WIDTH,
            ALGO_PANEL_HEIGHT
        )
        
        if scroll_bar_rect.collidepoint(x, y):
            self.dragging_scroll = True
            return

        # Check if click is on algorithm buttons
        if (x >= self.panel_x and x < self.panel_x + PANEL_WIDTH - SCROLL_BAR_WIDTH - SCROLL_PADDING):
            algo_panel_top = PANEL_TOP_PADDING + self.title_font.get_height() + 10
            if y >= algo_panel_top and y < algo_panel_top + ALGO_PANEL_HEIGHT:
                y_with_scroll = y - algo_panel_top + self.scroll_y
                y_offset = 0
                
                for category, algorithms in ALGORITHMS.items():
                    y_offset += CATEGORY_PADDING + CATEGORY_TITLE_HEIGHT
                    
                    for algorithm in algorithms:
                        button_rect = pygame.Rect(
                            self.panel_x + PANEL_PADDING,
                            algo_panel_top + y_offset - self.scroll_y,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT
                        )
                        if button_rect.collidepoint(x, y):
                            self.selected_algorithm = algorithm
                            return
                        y_offset += BUTTON_HEIGHT + BUTTON_PADDING
                        
                    y_offset += CATEGORY_PADDING

        # Check if click is on solve button
        if self.solve_button.collidepoint(x, y) and self.selected_algorithm:
            self.metrics = algorithm_manager.solve(board, self.selected_algorithm)

    def handle_scroll(self, y_offset):
        if self.dragging_scroll:
            scroll_ratio = y_offset / (ALGO_PANEL_HEIGHT - 30)  # 30 is min thumb height
            self.scroll_y = max(0, min(self.max_scroll, int(scroll_ratio * self.max_scroll)))

    def handle_mouse_up(self):
        self.dragging_scroll = False

    def handle_mouse_wheel(self, y):
        self.scroll_y = max(0, min(self.max_scroll, self.scroll_y - y * 20))

    def get_selected_cell(self):
        return self.selected_cell 