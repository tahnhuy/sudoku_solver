# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (200, 200, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (240, 240, 240)
SCROLL_BAR_COLOR = (200, 200, 200)
SCROLL_THUMB_COLOR = (160, 160, 160)
ORANGE = (255, 165, 0)

# Window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

# Board dimensions
BOARD_SIZE = 9
CELL_SIZE = 55
BOARD_PADDING = 40

# Button dimensions
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 40
BUTTON_PADDING = 8

# Control buttons dimensions
CONTROL_BUTTON_WIDTH = 120
CONTROL_BUTTON_HEIGHT = 40
CONTROL_BUTTON_MARGIN = 15

# Panel dimensions
PANEL_WIDTH = 350
PANEL_PADDING = 15
CATEGORY_PADDING = 25
PANEL_TOP_PADDING = 20
CATEGORY_TITLE_HEIGHT = 35

# Scroll bar dimensions
SCROLL_BAR_WIDTH = 15
SCROLL_PADDING = 5

# Algorithm panel dimensions
ALGO_PANEL_HEIGHT = 600

# Metrics dimensions
METRICS_HEIGHT = 100
METRICS_TOP_PADDING = 20

# Solve button dimensions
SOLVE_BUTTON_WIDTH = 200
SOLVE_BUTTON_HEIGHT = 50
SOLVE_BUTTON_MARGIN = 20

# Difficulty levels for puzzle generation
DIFFICULTY_LEVELS = {
    "Easy": 30,      # 30 cells filled
    "Medium": 25,    # 25 cells filled
    "Hard": 20       # 20 cells filled
}

# Algorithm categories
ALGORITHMS = {
    "Uninformed Search": [
        "Depth-First Search",
        "Breadth-First Search",
        "Uniform Cost Search"
    ],
    "Informed Search": [
        "A* Search",
        "Best-First Search"
    ],
    "Local Search": [
        "Hill Climbing",
        "Simulated Annealing"
    ],
    "Constraint Satisfaction": [
        "Backtracking",
        "Forward Checking",
        "AC-3"
    ]
}

# Font settings
TITLE_FONT_SIZE = 36
CATEGORY_FONT_SIZE = 28
BUTTON_FONT_SIZE = 24
METRICS_FONT_SIZE = 22
SOLVE_BUTTON_FONT_SIZE = 32
ERROR_FONT_SIZE = 24

# Colors for different algorithm categories
CATEGORY_COLORS = {
    "Uninformed Search": (230, 230, 250),
    "Informed Search": (230, 250, 230),
    "Local Search": (250, 230, 230),
    "Constraint Satisfaction": (230, 250, 250)
} 