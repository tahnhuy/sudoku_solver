# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 139)
SCROLL_BAR_COLOR = (200, 200, 200)
SCROLL_THUMB_COLOR = (160, 160, 160)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 900

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
        "Uniform Cost Search",
        "Iterative Deepening Search"
    ],
    "Informed Search": [
        "A* Search",
        "Best-First Search",
        "IDA* Search"
    ],
    "Local Search": [
        "Simple Hill Climbing",
        "Steepest-Ascent Hill Climbing",
        "Stochastic Hill Climbing",
        "Simulated Annealing",
        "Local Beam Search",
        "Genetic Algorithm"
    ],
    "Complex Environment Search": [
        "AND-OR Graph Search",
        "Partial Observation Search"
    ],
    "Constraint Satisfaction Problem": [
        "AC-3",
        "Forward Checking", 
        "Backtracking"
    ],
    "Reinforcement Learning": [
        "Q-Learning"
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
    "Complex Environment Search": (230, 250, 250),
    "Constraint Satisfaction Problem": (255, 240, 220),
    "Reinforcement Learning": (220, 255, 240)
}

# Timeout for solving algorithms (seconds)
SOLVE_TIMEOUT = 2