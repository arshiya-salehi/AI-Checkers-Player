import sys
import math
import random
import copy
from random import randint
from BoardClasses import Move
from BoardClasses import Board

class MCTSNode:
    def __init__(self, board, parent=None, move=None, color=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.color = color
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self._get_moves()
        
    def _get_moves(self):
        if self.color is None:
            return []
        moves = self.board.get_all_possible_moves(self.color)
        # Flatten the moves list
        return [(i, j, move) for i, moves_list in enumerate(moves) 
                for j, move in enumerate(moves_list)]

    def ucb1(self, c=1.414):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

class StudentAI():
    
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)  # Initialize the board here
        self.board.initialize_game()      # Initialize game state
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        
        # MCTS parameters
        self.simulation_limit = 1000  # Number of MCTS iterations
        self.simulation_depth = 50    # Maximum depth for random playouts
        
        # Weights for different heuristic components
        self.KING_WEIGHT = 15
        self.PIECE_WEIGHT = 10
        self.CENTER_CONTROL_WEIGHT = 4
        self.BACK_ROW_WEIGHT = 6
        self.ADVANCEMENT_WEIGHT = 3
        self.PROTECTION_WEIGHT = 5
        self.MOBILITY_WEIGHT = 4
        
    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        # Initialize MCTS root node
        root = MCTSNode(copy.deepcopy(self.board), color=self.color)
        
        # Run MCTS for simulation_limit iterations
        for _ in range(self.simulation_limit):
            node = self._select(root)
            child = self._expand(node)
            if child is not None:
                result = self._simulate(child)
                self._backpropagate(child, result)

        # Choose best move based on most visited child
        best_child = max(root.children, key=lambda c: c.visits)
        best_move = best_child.move[2]  # Get the actual move
        
        self.board.make_move(best_move, self.color)
        return best_move

    def _select(self, node):
        while node.untried_moves == [] and node.children != []:
            node = max(node.children, key=lambda n: n.ucb1())
        return node

    def _expand(self, node):
        if node.untried_moves:  # if we can expand
            i, j, move = random.choice(node.untried_moves)
            node.untried_moves.remove((i, j, move))
            
            # Create new board state
            new_board = copy.deepcopy(node.board)
            new_board.make_move(move, node.color)
            
            # Create new child node
            child = MCTSNode(
                new_board,
                parent=node,
                move=(i, j, move),
                color=self.opponent[node.color]
            )
            node.children.append(child)
            return child
        return None

    def _simulate(self, node):
        board = copy.deepcopy(node.board)
        current_color = node.color
        depth = 0
        
        while depth < self.simulation_depth:
            if board.is_win(current_color) != 0:
                break
                
            moves = board.get_all_possible_moves(current_color)
            if not moves:
                break
                
            # Use heuristic evaluation to guide playouts
            if random.random() < 0.8:  # 80% chance to use heuristic
                best_score = float('-inf')
                best_move = None
                
                for move_list in moves:
                    for move in move_list:
                        temp_board = copy.deepcopy(board)
                        temp_board.make_move(move, current_color)
                        score = self.heuristic_evaluation(temp_board)
                        
                        if score > best_score:
                            best_score = score
                            best_move = move
                
                if best_move:
                    board.make_move(best_move, current_color)
            else:  # 20% chance for random move
                move_list = random.choice(moves)
                move = random.choice(move_list)
                board.make_move(move, current_color)
            
            current_color = self.opponent[current_color]
            depth += 1
        
        # Return 1 for win, 0 for loss/draw
        result = board.is_win(self.opponent[node.color])
        return 1 if result == self.color else 0

    def _backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def heuristic_evaluation(self, board):
        """
        Complex heuristic function that evaluates board state using multiple factors
        """
        score = 0
        
        # Material count and king count (base evaluation)
        my_pieces = self.count_pieces(board, self.color)
        opponent_pieces = self.count_pieces(board, self.opponent[self.color])
        my_kings = self.count_kings(board, self.color)
        opponent_kings = self.count_kings(board, self.opponent[self.color])
        
        score += (my_pieces - opponent_pieces) * self.PIECE_WEIGHT
        score += (my_kings - opponent_kings) * self.KING_WEIGHT
        
        # Board control evaluation
        center_control = self.evaluate_center_control(board)
        score += center_control * self.CENTER_CONTROL_WEIGHT
        
        # Back row protection (king creation prevention)
        back_row = self.evaluate_back_row(board)
        score += back_row * self.BACK_ROW_WEIGHT
        
        # Piece advancement
        advancement = self.evaluate_advancement(board)
        score += advancement * self.ADVANCEMENT_WEIGHT
        
        # Piece protection and structure
        protection = self.evaluate_protection(board)
        score += protection * self.PROTECTION_WEIGHT
        
        # Mobility (number of possible moves)
        mobility = self.evaluate_mobility(board)
        score += mobility * self.MOBILITY_WEIGHT
        
        return score
    
    def evaluate_center_control(self, board):
        """Evaluate control of the center squares"""
        center_score = 0
        # Calculate center squares based on board dimensions
        center_rows = [self.row//2 - 1, self.row//2]
        center_cols = [self.col//2 - 1, self.col//2]
        center_squares = [(r,c) for r in center_rows for c in center_cols]
        
        for row, col in center_squares:
            checker = board.board[row][col]
            if checker != 0:
                if checker.color == self.color:
                    center_score += 1
                else:
                    center_score -= 1
        
        return center_score
    
    def evaluate_back_row(self, board):
        """Evaluate control and protection of back row"""
        score = 0
        back_row = 0 if self.color == 2 else self.row - 1
        
        for col in range(self.col):
            checker = board.board[back_row][col]
            if checker != 0:
                if checker.color == self.color:
                    score += 1
                else:
                    score -= 2  # Penalize opponent pieces in our back row
        
        return score
    
    def evaluate_advancement(self, board):
        """Evaluate piece advancement towards opponent's side"""
        score = 0
        direction = 1 if self.color == 1 else -1
        
        for row in range(self.row):
            for col in range(self.col):
                checker = board.board[row][col]
                if checker != 0 and checker.color == self.color:
                    if not checker.is_king:  # Regular piece
                        if self.color == 1:
                            score += row * 0.1  # Reward advancing towards opponent
                        else:
                            score += (self.row-1-row) * 0.1
        
        return score
    
    def evaluate_protection(self, board):
        """Evaluate piece protection and structure"""
        score = 0
        
        for row in range(self.row):
            for col in range(self.col):
                checker = board.board[row][col]
                if checker != 0:
                    if checker.color == self.color:
                        if self.is_protected(board, row, col):
                            score += 1
                        if self.is_vulnerable(board, row, col):
                            score -= 1
        
        return score
    
    def evaluate_mobility(self, board):
        """Evaluate the number of possible moves"""
        my_moves = len(board.get_all_possible_moves(self.color))
        opponent_moves = len(board.get_all_possible_moves(self.opponent[self.color]))
        return my_moves - opponent_moves
    
    def is_protected(self, board, row, col):
        """Check if a piece is protected by friendly pieces"""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        protected = False
        
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < self.row and 0 <= new_col < self.col:
                checker = board.board[new_row][new_col]
                if checker != 0:
                    if checker.color == self.color:
                        protected = True
                        break
        
        return protected
    
    def is_vulnerable(self, board, row, col):
        """Check if a piece can be captured"""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            jump_row, jump_col = row + 2*dx, col + 2*dy
            
            if (0 <= jump_row < self.row and 0 <= jump_col < self.col and 
                0 <= new_row < self.row and 0 <= new_col < self.col):
                if board.board[jump_row][jump_col] == 0:
                    checker = board.board[new_row][new_col]
                    if checker != 0:
                        if checker.color != self.color:
                            return True
        
        return False

    def count_pieces(self, board, color):
        """Count total number of pieces of given color"""
        count = 0
        for row in range(self.row):
            for col in range(self.col):
                checker = board.board[row][col]
                if checker != 0 and checker.color == color:
                    count += 1
        return count

    def count_kings(self, board, color):
        """Count number of kings of given color"""
        count = 0
        for row in range(self.row):
            for col in range(self.col):
                checker = board.board[row][col]
                if checker != 0 and checker.color == color and checker.is_king:
                    count += 1
        return count

    