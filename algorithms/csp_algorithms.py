import copy
from collections import deque

def ac3(board, steps_counter=None, states=None):
    """AC-3 algorithm for constraint propagation"""
    def get_arcs():
        arcs = []
        # Add row constraints
        for i in range(9):
            for j in range(9):
                for k in range(j + 1, 9):
                    arcs.append(((i, j), (i, k)))
                    arcs.append(((i, k), (i, j)))
        
        # Add column constraints
        for j in range(9):
            for i in range(9):
                for k in range(i + 1, 9):
                    arcs.append(((i, j), (k, j)))
                    arcs.append(((k, j), (i, j)))
        
        # Add box constraints
        for box_i in range(3):
            for box_j in range(3):
                cells = [(i + box_i * 3, j + box_j * 3) 
                        for i in range(3) for j in range(3)]
                for i, cell1 in enumerate(cells):
                    for cell2 in cells[i + 1:]:
                        arcs.append((cell1, cell2))
                        arcs.append((cell2, cell1))
        return arcs

    def revise(domains, xi, xj):
        revised = False
        if board.get_value(*xi) != 0 or board.get_value(*xj) != 0:
            return False
        
        for x in domains[xi][:]: # [:] được dùng để tạo bản sao
            # If no value in xj's domain satisfies the constraint
            if all(x == y for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised

    # Initialize domains
    domains = {}
    for i in range(9):
        for j in range(9):
            if board.get_value(i, j) == 0:
                domains[(i, j)] = list(range(1, 10))
            else:
                domains[(i, j)] = [board.get_value(i, j)]

    # Get all arcs
    queue = deque(get_arcs())
    
    # Process all arcs
    step_count = 0
    while queue:
        (xi, xj) = queue.popleft()
        step_count += 1
        if steps_counter is not None:
            steps_counter[0] = step_count
            
        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False
            for xk in [(r, c) for r, c in domains.keys() if (r == xi[0] or c == xi[1] or (r//3 == xi[0]//3 and c//3 == xi[1]//3)) and (r, c) != xi]:
                queue.append((xk, xi))
    
    # Update board with reduced domains where possible
    changes_made = False
    for (i, j), domain in domains.items():
        if len(domain) == 1 and board.get_value(i, j) == 0:
            board.set_value(i, j, domain[0])
            changes_made = True
            step_count += 1
            if steps_counter is not None:
                steps_counter[0] = step_count
            if states is not None:
                states.append(board.get_board_state().copy())
    
    return True

def forward_checking(board, var, value, steps_counter=None):
    """Forward checking for constraint propagation"""
    if steps_counter is not None:
        steps_counter[0] += 1
        
    row, col = var
    
    # Check row
    for j in range(9):
        if j != col and board.get_value(row, j) == value:
            return False
            
    # Check column
    for i in range(9):
        if i != row and board.get_value(i, col) == value:
            return False
            
    # Check box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i != row or j != col) and board.get_value(i, j) == value:
                return False
                
    return True

def backtracking_search(board, steps_counter=None, states=None):
    """Backtracking search with forward checking"""
    def backtrack(assignment):
        if len(assignment) == 81:  # All variables assigned
            return True
            
        # Select unassigned variable
        var = None
        for i in range(9):
            for j in range(9):
                if board.get_value(i, j) == 0:
                    var = (i, j)
                    break
            if var:
                break
                
        if not var:
            return True
            
        # Try each value in the domain
        for value in range(1, 10):
            if steps_counter is not None:
                steps_counter[0] += 1
                
            if board.is_valid_move(*var, value):
                # If value is consistent with constraints
                if forward_checking(board, var, value, steps_counter):
                    board.set_value(*var, value)
                    assignment.append(var)
                    
                    # Save state for visualization
                    if states is not None:
                        states.append(board.get_board_state().copy())
                        
                    result = backtrack(assignment)
                    if result:
                        return True
                    # If no solution found, backtrack
                    board.set_value(*var, 0)
                    assignment.pop()
                    
                    # Save state after backtracking
                    if states is not None:
                        states.append(board.get_board_state().copy())
                    
        return False
        
    return backtrack([]) 