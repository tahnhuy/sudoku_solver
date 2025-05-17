import pygame
import os
from utils.constants import *
import threading
import time
import copy
import pandas as pd
import numpy as np

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
        self.error_message = None
        self.solve_cancelled = False
        self.board_state_before_solve = None
        
        # Specialized visualization for certain algorithm types
        self.show_qtable = False
        self.show_observations = False
        self.qtable_data = {}
        
        # Calculate board position to center it
        self.board_x = (WINDOW_WIDTH - PANEL_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
        self.board_y = BOARD_PADDING
        
        # Right panel position
        self.panel_x = WINDOW_WIDTH - PANEL_WIDTH
        
        # Shift solve button and difficulty selector to the left for better balance
        solve_x = self.board_x + (BOARD_SIZE * CELL_SIZE - SOLVE_BUTTON_WIDTH) // 2 + 120
        self.solve_button = pygame.Rect(
            solve_x,
            self.board_y + BOARD_SIZE * CELL_SIZE + SOLVE_BUTTON_MARGIN,
            SOLVE_BUTTON_WIDTH,
            SOLVE_BUTTON_HEIGHT
        )
        
        # Calculate y position for control buttons (below Solve button)
        self.control_buttons_y = self.solve_button.bottom + 15
        # Calculate total width of all control buttons and margins
        total_control_width = 5 * CONTROL_BUTTON_WIDTH + 4 * 10
        self.control_buttons_x = self.board_x + (BOARD_SIZE * CELL_SIZE - total_control_width) // 2

        # Create Reset, Export, Random, Compare, and New Game buttons (centered below Solve)
        self.reset_button = pygame.Rect(
            self.control_buttons_x,
            self.control_buttons_y,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )
        self.export_button = pygame.Rect(
            self.control_buttons_x + (CONTROL_BUTTON_WIDTH + 10),
            self.control_buttons_y,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )
        self.random_button = pygame.Rect(
            self.control_buttons_x + 2 * (CONTROL_BUTTON_WIDTH + 10),
            self.control_buttons_y,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )
        self.compare_button = pygame.Rect(
            self.control_buttons_x + 3 * (CONTROL_BUTTON_WIDTH + 10),
            self.control_buttons_y,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )
        self.new_game_button = pygame.Rect(
            self.control_buttons_x + 4 * (CONTROL_BUTTON_WIDTH + 10),
            self.control_buttons_y,
            CONTROL_BUTTON_WIDTH,
            CONTROL_BUTTON_HEIGHT
        )

        self.solve_thread = None
        self.solve_result = None
        self.solve_start_time = None
        self.solve_in_progress = False

        # Difficulty selection
        self.difficulties = list(DIFFICULTY_LEVELS.keys())
        self.selected_difficulty = self.difficulties[0]
        # Difficulty buttons (will be positioned in draw)
        self.difficulty_buttons = []

    def draw_board(self, board):
        # Draw board background
        board_rect = pygame.Rect(
            self.board_x - BOARD_PADDING,
            self.board_y - BOARD_PADDING,
            BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING,
            BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
        )
        pygame.draw.rect(self.screen, WHITE, board_rect)
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
                    color = RED if board.is_original(i, j) else BLACK
                    number = self.button_font.render(str(board.get_value(i, j)), True, color)
                    x = self.board_x + j * CELL_SIZE + (CELL_SIZE - number.get_width()) // 2
                    y = self.board_y + i * CELL_SIZE + (CELL_SIZE - number.get_height()) // 2
                    self.screen.blit(number, (x, y))
                    
        # Draw control buttons (with rounded corners)
        pygame.draw.rect(self.screen, LIGHT_BLUE, self.reset_button, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, self.reset_button, 1, border_radius=12)
        reset_text = self.button_font.render("Reset", True, BLACK)
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)
        
        pygame.draw.rect(self.screen, GREEN, self.export_button, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, self.export_button, 1, border_radius=12)
        export_text = self.button_font.render("Export", True, BLACK)
        export_rect = export_text.get_rect(center=self.export_button.center)
        self.screen.blit(export_text, export_rect)
        
        pygame.draw.rect(self.screen, PURPLE, self.random_button, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, self.random_button, 1, border_radius=12)
        random_text = self.button_font.render("Random", True, BLACK)
        random_rect = random_text.get_rect(center=self.random_button.center)
        self.screen.blit(random_text, random_rect)
        
        pygame.draw.rect(self.screen, (100, 200, 255), self.compare_button, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, self.compare_button, 1, border_radius=12)
        compare_text = self.button_font.render("Compare", True, BLACK)
        compare_rect = compare_text.get_rect(center=self.compare_button.center)
        self.screen.blit(compare_text, compare_rect)

        pygame.draw.rect(self.screen, ORANGE, self.new_game_button, border_radius=12)
        pygame.draw.rect(self.screen, BLACK, self.new_game_button, 1, border_radius=12)
        new_game_text = self.button_font.render("New Game", True, BLACK)
        new_game_rect = new_game_text.get_rect(center=self.new_game_button.center)
        self.screen.blit(new_game_text, new_game_rect)

    def draw_difficulty_selector(self):
        # Draw horizontal difficulty selection box to the left of the Solve button, no label
        btn_w = 80
        btn_h = 36
        spacing = 16
        total_btns = len(self.difficulties)
        box_width = total_btns * btn_w + (total_btns - 1) * spacing + 16
        box_height = btn_h + 16
        # Đặt khung độ khó sát hơn với nút Solve (giảm khoảng cách)
        box_x = self.solve_button.left - box_width - 10
        box_y = self.solve_button.centery - box_height // 2
        pygame.draw.rect(self.screen, LIGHT_GRAY, (box_x, box_y, box_width, box_height), border_radius=12)
        pygame.draw.rect(self.screen, BLACK, (box_x, box_y, box_width, box_height), 2, border_radius=12)
        # Draw buttons horizontally, no label
        self.difficulty_buttons = []
        for i, diff in enumerate(self.difficulties):
            btn_rect = pygame.Rect(
                box_x + 8 + i * (btn_w + spacing),
                box_y + 8,
                btn_w,
                btn_h
            )
            color = GREEN if diff == self.selected_difficulty else WHITE
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, btn_rect, 1, border_radius=8)
            text = self.button_font.render(diff, True, BLACK)
            text_rect = text.get_rect(center=btn_rect.center)
            self.screen.blit(text, text_rect)
            self.difficulty_buttons.append((btn_rect, diff))

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
        pygame.draw.rect(self.screen, GRAY, shadow_rect, border_radius=15)
        
        pygame.draw.rect(self.screen, GREEN, self.solve_button, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, self.solve_button, 2, border_radius=15)
        
        solve_text = self.solve_font.render("Solve", True, WHITE)
        solve_rect = solve_text.get_rect(center=self.solve_button.center)
        self.screen.blit(solve_text, solve_rect)

    def draw_metrics(self):
        if self.metrics:
            # Draw metrics background below control buttons
            metrics_rect = pygame.Rect(
                self.board_x - BOARD_PADDING,
                self.control_buttons_y + CONTROL_BUTTON_HEIGHT + 20,
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
        elif self.error_message:
            # Draw error message background below control buttons
            metrics_rect = pygame.Rect(
                self.board_x - BOARD_PADDING,
                self.control_buttons_y + CONTROL_BUTTON_HEIGHT + 20,
                BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING,
                METRICS_HEIGHT
            )
            pygame.draw.rect(self.screen, LIGHT_GRAY, metrics_rect)
            pygame.draw.rect(self.screen, BLACK, metrics_rect, 1)
            error_text = self.error_font.render(self.error_message, True, RED)
            error_rect = error_text.get_rect(center=metrics_rect.center)
            self.screen.blit(error_text, error_rect)

    def draw(self, board, algorithm_manager):
        self.screen.fill(WHITE)
        self.draw_board(board)
        self.draw_difficulty_selector()
        self.draw_algorithm_buttons()
        
        # Đổi màu nút Solve thành màu xanh lá
        button_color = GREEN
        pygame.draw.rect(self.screen, button_color, self.solve_button, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, self.solve_button, 1, border_radius=15)
        solve_text = "Cancel" if self.solve_in_progress else "Solve"
        text = self.solve_font.render(solve_text, True, WHITE)
        text_rect = text.get_rect(center=self.solve_button.center)
        self.screen.blit(text, text_rect)
        
        # Draw metrics if available
        if self.metrics:
            self.draw_metrics()
            
        # Draw specialized visualizations if selected
        # Đã xóa visualization cho nhóm môi trường phức tạp
        if self.selected_algorithm:
            if self.selected_algorithm == "Q-Learning":
                self.draw_reinforcement_learning_visualization(board, algorithm_manager)
        
        # Draw error message if any
        if self.error_message:
            self.draw_error_message()
        
        pygame.display.flip()

    def draw_reinforcement_learning_visualization(self, board, algorithm_manager):
        """Draw special visualization for Reinforcement Learning algorithms"""
        if not self.metrics:
            return
            
        # Create visualization area below the board and metrics
        vis_rect = pygame.Rect(
            self.board_x,
            self.control_buttons_y + CONTROL_BUTTON_HEIGHT + METRICS_HEIGHT + 40,
            BOARD_SIZE * CELL_SIZE,
            120
        )
        pygame.draw.rect(self.screen, (220, 255, 240), vis_rect)
        pygame.draw.rect(self.screen, BLACK, vis_rect, 1)
        
        title = self.button_font.render("Reinforcement Learning Visualization", True, BLACK)
        self.screen.blit(title, (vis_rect.centerx - title.get_width() // 2, vis_rect.top + 5))
        
        if self.selected_algorithm == "Q-Learning" and hasattr(algorithm_manager, 'q_learning'):
            # Draw Q-Learning visualization
            q_text = self.metrics_font.render("Q-Learning", True, BLACK)
            self.screen.blit(q_text, (vis_rect.left + 10, vis_rect.top + 35))
            
            # Show toggle button for Q-table
            q_button = pygame.Rect(vis_rect.left + 10, vis_rect.top + 65, 150, 30)
            pygame.draw.rect(self.screen, LIGHT_BLUE if self.show_qtable else LIGHT_GRAY, q_button, border_radius=5)
            pygame.draw.rect(self.screen, BLACK, q_button, 1, border_radius=5)
            
            button_text = self.button_font.render("Show Q-Table" if not self.show_qtable else "Hide Q-Table", True, BLACK)
            self.screen.blit(button_text, (q_button.centerx - button_text.get_width() // 2, 
                                        q_button.centery - button_text.get_height() // 2))
            
            # Show additional metrics
            if hasattr(algorithm_manager.q_learning, 'epsilon'):
                epsilon_text = self.metrics_font.render(f"Exploration rate: {algorithm_manager.q_learning.epsilon:.2f}", True, BLACK)
                self.screen.blit(epsilon_text, (vis_rect.left + 170, vis_rect.top + 35))
                
            reward_text = self.metrics_font.render(f"Total reward: {self.metrics.get('total_reward', 'N/A')}", True, BLACK)
            self.screen.blit(reward_text, (vis_rect.left + 170, vis_rect.top + 65))
            
            # If showing Q-table, draw popup with Q-table values
            if self.show_qtable:
                self.draw_qtable_popup(algorithm_manager.q_learning.q_table)

    def draw_qtable_popup(self, q_table):
        """Draw Q-table popup with selected values"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Q-table box
        box_width, box_height = 700, 500
        box_rect = pygame.Rect(
            (WINDOW_WIDTH - box_width) // 2,
            (WINDOW_HEIGHT - box_height) // 2,
            box_width,
            box_height
        )
        pygame.draw.rect(self.screen, WHITE, box_rect, border_radius=10)
        pygame.draw.rect(self.screen, DARK_BLUE, box_rect, 2, border_radius=10)
        
        # Title
        title = self.title_font.render("Q-Learning Table", True, DARK_BLUE)
        title_rect = title.get_rect(centerx=box_rect.centerx, top=box_rect.top + 10)
        self.screen.blit(title, title_rect)
        
        # Table content area
        table_rect = pygame.Rect(
            box_rect.left + 20,
            title_rect.bottom + 20,
            box_width - 40,
            box_height - title_rect.height - 90
        )
        pygame.draw.rect(self.screen, LIGHT_GRAY, table_rect, border_radius=5)
        
        # Display Q-table values (showing only a sample for visualization)
        if q_table:
            # Header
            header_y = table_rect.top + 10
            header_x = table_rect.left + 10
            header = self.button_font.render("State", True, BLACK)
            self.screen.blit(header, (header_x, header_y))
            
            for i in range(1, 10):
                action_text = self.button_font.render(f"Action {i}", True, BLACK)
                self.screen.blit(action_text, (header_x + 150 + (i-1)*50, header_y))
            
            # Q-values (limited to 10 states for display)
            y_offset = header_y + 30
            count = 0
            max_states_to_show = 10
            
            for state, actions in q_table.items():
                if count >= max_states_to_show:
                    break
                    
                # Format state for display
                state_text = f"State {count+1}"
                state_label = self.metrics_font.render(state_text, True, BLACK)
                self.screen.blit(state_label, (header_x, y_offset))
                
                # Display Q-values for each action
                for i in range(1, 10):
                    q_value = actions.get(i, 0.0)
                    value_color = GREEN if q_value > 0 else RED if q_value < 0 else BLACK
                    value_text = self.metrics_font.render(f"{q_value:.1f}", True, value_color)
                    self.screen.blit(value_text, (header_x + 150 + (i-1)*50, y_offset))
                
                y_offset += 30
                count += 1
            
            # Show message if many states exist
            if len(q_table) > max_states_to_show:
                more_text = self.metrics_font.render(f"+ {len(q_table) - max_states_to_show} more states...", True, GRAY)
                self.screen.blit(more_text, (header_x, y_offset + 10))
        else:
            # No Q-table data
            no_data = self.button_font.render("No Q-table data available", True, GRAY)
            no_data_rect = no_data.get_rect(center=table_rect.center)
            self.screen.blit(no_data, no_data_rect)
        
        # Close button
        close_button = pygame.Rect(
            box_rect.centerx - 50,
            box_rect.bottom - 50,
            100,
            30
        )
        pygame.draw.rect(self.screen, LIGHT_BLUE, close_button, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, close_button, 1, border_radius=5)
        
        close_text = self.button_font.render("Close", True, BLACK)
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)
        
        # Store button position for click handling
        self.qtable_close_button = close_button

    def draw_error_message(self):
        """Draw error message popup"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Error message box
        box_width, box_height = 400, 200
        box_rect = pygame.Rect(
            (WINDOW_WIDTH - box_width) // 2,
            (WINDOW_HEIGHT - box_height) // 2,
            box_width,
            box_height
        )
        pygame.draw.rect(self.screen, WHITE, box_rect, border_radius=15)
        pygame.draw.rect(self.screen, RED, box_rect, 2, border_radius=15)
        
        # Error message text
        error_text = self.error_font.render("Error", True, RED)
        error_rect = error_text.get_rect(centerx=box_rect.centerx, top=box_rect.top + 20)
        self.screen.blit(error_text, error_rect)
        
        # Error message content
        message_text = self.button_font.render(self.error_message, True, BLACK)
        message_rect = message_text.get_rect(centerx=box_rect.centerx, top=error_rect.bottom + 20)
        self.screen.blit(message_text, message_rect)
        
        # OK button
        ok_button = pygame.Rect(
            box_rect.centerx - 50,
            box_rect.bottom - 60,
            100,
            40
        )
        pygame.draw.rect(self.screen, LIGHT_BLUE, ok_button, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, ok_button, 1, border_radius=10)
        
        ok_text = self.button_font.render("OK", True, BLACK)
        ok_rect = ok_text.get_rect(center=ok_button.center)
        self.screen.blit(ok_text, ok_rect)

    def show_export_popup(self, message, ok_only=False):
        # Simple popup: vẽ lên màn hình và chờ OK hoặc Yes/No
        popup_width, popup_height = 400, 180
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, LIGHT_GRAY, popup_rect, border_radius=16)
        pygame.draw.rect(self.screen, BLACK, popup_rect, 2, border_radius=16)
        # Word wrap message
        def wrap_text(text, font, max_width):
            words = text.split(' ')
            lines = []
            current_line = ''
            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return lines
        lines = wrap_text(message, self.button_font, popup_width - 40)
        for i, line in enumerate(lines):
            text = self.button_font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(popup_x + popup_width//2, popup_y + 40 + i*30))
            self.screen.blit(text, text_rect)
        if ok_only:
            ok_rect = pygame.Rect(popup_x + (popup_width-100)//2, popup_y + 110, 100, 40)
            pygame.draw.rect(self.screen, GREEN, ok_rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, ok_rect, 2, border_radius=10)
            ok_text = self.button_font.render("OK", True, BLACK)
            self.screen.blit(ok_text, ok_text.get_rect(center=ok_rect.center))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ok_rect.collidepoint(event.pos):
                            self.solve_cancelled = True
                            waiting = False
            return True
        # Yes/No buttons như cũ
        yes_rect = pygame.Rect(popup_x + 60, popup_y + 110, 100, 40)
        no_rect = pygame.Rect(popup_x + 240, popup_y + 110, 100, 40)
        pygame.draw.rect(self.screen, GREEN, yes_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, yes_rect, 2, border_radius=10)
        pygame.draw.rect(self.screen, RED, no_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, no_rect, 2, border_radius=10)
        yes_text = self.button_font.render("Yes", True, BLACK)
        no_text = self.button_font.render("No", True, BLACK)
        self.screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        self.screen.blit(no_text, no_text.get_rect(center=no_rect.center))
        pygame.display.flip()
        waiting = True
        result = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(event.pos):
                        result = True
                        waiting = False
                    elif no_rect.collidepoint(event.pos):
                        result = False
                        waiting = False
        if not result:
            self.solve_cancelled = True
        return result

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

        # Check if click is on export button
        if self.export_button.collidepoint(x, y) and self.metrics:
            file_path = os.path.join(os.getcwd(), 'sudoku_solution.xlsx')
            if os.path.exists(file_path):
                confirm = self.show_export_popup("File already exists. Overwrite?", ok_only=True)
                if not confirm:
                    return
            else:
                confirm = self.show_export_popup("Do you want to export the file?", ok_only=True)
                if not confirm:
                    return
            algorithm_manager.export_to_excel(self.metrics)
            self.show_export_popup("Excel file exported!", ok_only=True)
            return

        # Check if click is on random button
        if self.random_button.collidepoint(x, y):
            board.new_game("Random")
            self.metrics = None
            self.selected_cell = None
            return

        # Check if click is on compare button
        if self.compare_button.collidepoint(x, y):
            # Lưu trạng thái hiện tại của bảng
            board_state = copy.deepcopy(board.get_board_state())
            results = []
            for algo_name in algorithm_manager.algorithms.keys():
                # Reset board về trạng thái ban đầu
                board.set_board_state(board_state)
                # Reset các biến trạng thái
                algorithm_manager.steps = 0
                algorithm_manager.states = [board_state.copy()]
                algorithm_manager.start_time = None
                try:
                    start = time.time()
                    metrics = algorithm_manager.solve(board, algo_name, timeout=SOLVE_TIMEOUT)
                    elapsed = time.time() - start
                    found = metrics is not None
                    steps = metrics['steps'] if found else '-'
                    complexity = metrics['complexity'] if found else '-'
                except Exception as e:
                    found = False
                    elapsed = '-'
                    steps = '-'
                    complexity = '-'
                results.append({
                    'Algorithm': algo_name,
                    'Found': 'Yes' if found else 'No',
                    'Time (s)': f"{elapsed:.2f}" if isinstance(elapsed, float) else elapsed,
                    'Steps': steps,
                    'Complexity': complexity
                })
            # Xuất ra file compare.xlsx
            df = pd.DataFrame(results)
            df.to_excel('compare.xlsx', index=False)
            self.show_export_popup("Comparison exported to compare.xlsx!", ok_only=True)
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
            if not self.solve_in_progress:
                self.solve_result = None
                self.solve_in_progress = True
                self.solve_start_time = time.time()
                self.solve_cancelled = False
                self.board_state_before_solve = copy.deepcopy(board.get_board_state())
                def run_solve():
                    self.solve_result = algorithm_manager.solve(board, self.selected_algorithm, timeout=SOLVE_TIMEOUT, cancel_flag=lambda: self.solve_cancelled)
                    self.solve_in_progress = False
                self.solve_thread = threading.Thread(target=run_solve)
                self.solve_thread.start()
                # Wait for result or timeout
                while self.solve_in_progress:
                    pygame.event.pump()
                    if time.time() - self.solve_start_time > SOLVE_TIMEOUT:
                        self.show_export_popup("No solution found (timeout or unsolvable).", ok_only=True)
                        if self.solve_cancelled and self.board_state_before_solve is not None:
                            board.set_board_state(self.board_state_before_solve)
                        break  # Thoát khỏi vòng lặp chờ, trả quyền điều khiển cho giao diện
                    time.sleep(0.01)
                self.metrics = self.solve_result
                self.solve_cancelled = False
                if self.metrics is None:
                    self.show_export_popup("No solution found (timeout or unsolvable).", ok_only=True)
                    if self.solve_cancelled and self.board_state_before_solve is not None:
                        board.set_board_state(self.board_state_before_solve)
                    self.error_message = None
                else:
                    self.error_message = None
                # Đảm bảo không còn thread giải nào chạy
                self.solve_thread = None
                self.solve_in_progress = False

        # Check for specialized visualization buttons
        if self.selected_algorithm in ["AND-OR Graph Search", "Q-Learning", "Partial Observation Search"] and self.metrics:
            vis_rect = pygame.Rect(
                self.board_x,
                self.control_buttons_y + CONTROL_BUTTON_HEIGHT + METRICS_HEIGHT + 40,
                BOARD_SIZE * CELL_SIZE,
                120
            )
            
            if vis_rect.collidepoint(x, y):
                if self.selected_algorithm == "Q-Learning":
                    q_button = pygame.Rect(vis_rect.left + 10, vis_rect.top + 65, 150, 30)
                    if q_button.collidepoint(x, y):
                        self.show_qtable = not self.show_qtable
                elif self.selected_algorithm == "Partial Observation Search":
                    obs_button = pygame.Rect(vis_rect.left + 170, vis_rect.top + 65, 200, 30)
                    if obs_button.collidepoint(x, y):
                        self.show_observations = not self.show_observations
        
        # Check for Q-table close button
        if self.show_qtable and hasattr(self, 'qtable_close_button'):
            if self.qtable_close_button.collidepoint(x, y):
                self.show_qtable = False
                
        # Check for Observations close button
        if self.show_observations and hasattr(self, 'observations_close_button'):
            if self.observations_close_button.collidepoint(x, y):
                self.show_observations = False

        # Check if click is on difficulty buttons
        for btn_rect, diff in self.difficulty_buttons:
            if btn_rect.collidepoint(x, y):
                self.selected_difficulty = diff
                board.new_game(diff)
                self.metrics = None
                self.selected_cell = None
                return

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

    def draw_observations_popup(self, observations):
        """Draw observations popup for Partial Observation Search"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Observations box
        box_width, box_height = 700, 500
        box_rect = pygame.Rect(
            (WINDOW_WIDTH - box_width) // 2,
            (WINDOW_HEIGHT - box_height) // 2,
            box_width,
            box_height
        )
        pygame.draw.rect(self.screen, WHITE, box_rect, border_radius=10)
        pygame.draw.rect(self.screen, DARK_BLUE, box_rect, 2, border_radius=10)
        
        # Title
        title = self.title_font.render("Partial Observations", True, DARK_BLUE)
        title_rect = title.get_rect(centerx=box_rect.centerx, top=box_rect.top + 10)
        self.screen.blit(title, title_rect)
        
        # Content area
        content_rect = pygame.Rect(
            box_rect.left + 20,
            title_rect.bottom + 20,
            box_width - 40,
            box_height - title_rect.height - 90
        )
        pygame.draw.rect(self.screen, LIGHT_GRAY, content_rect, border_radius=5)
        
        if observations and isinstance(observations, dict) and len(observations) > 0:
            # Header
            header_y = content_rect.top + 10
            header_x = content_rect.left + 10
            header = self.button_font.render("Step", True, BLACK)
            self.screen.blit(header, (header_x, header_y))
            
            obs_header = self.button_font.render("Visible Cells", True, BLACK)
            self.screen.blit(obs_header, (header_x + 100, header_y))
            
            # Display observations (show up to 15 steps)
            y_offset = header_y + 30
            count = 0
            max_steps_to_show = 15
            
            # Sort observations by step number
            sorted_observations = sorted(observations.items())
            
            for step, obs in sorted_observations:
                if count >= max_steps_to_show:
                    break
                    
                # Format step number
                step_text = f"Step {step}"
                step_label = self.metrics_font.render(step_text, True, BLACK)
                self.screen.blit(step_label, (header_x, y_offset))
                
                # Count visible and total cells
                visible_count = sum(1 for i in range(9) for j in range(9) if obs[i][j] != 0)
                total_cells = 81
                
                # Display visible cells count
                visible_text = f"{visible_count}/{total_cells} cells"
                visible_label = self.metrics_font.render(visible_text, True, DARK_BLUE)
                self.screen.blit(visible_label, (header_x + 100, y_offset))
                
                y_offset += 25
                count += 1
            
            # Show message if many steps exist
            if len(observations) > max_steps_to_show:
                more_text = self.metrics_font.render(f"+ {len(observations) - max_steps_to_show} more steps...", True, GRAY)
                self.screen.blit(more_text, (header_x, y_offset + 10))
        else:
            # No observations data
            no_data = self.button_font.render("No observations data available", True, GRAY)
            no_data_rect = no_data.get_rect(center=content_rect.center)
            self.screen.blit(no_data, no_data_rect)
        
        # Close button
        close_button = pygame.Rect(
            box_rect.centerx - 50,
            box_rect.bottom - 50,
            100,
            30
        )
        pygame.draw.rect(self.screen, LIGHT_BLUE, close_button, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, close_button, 1, border_radius=5)
        
        close_text = self.button_font.render("Close", True, BLACK)
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)
        
        # Store button position for click handling
        self.observations_close_button = close_button 