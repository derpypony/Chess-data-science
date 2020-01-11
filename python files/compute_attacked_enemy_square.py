import os
import chess.pgn
import pandas as pd
import statistics

def compute_attacked_enemy_square(board, color):
    total_attacked_square = 0
    if color == 'White':
        for location, piece in board.piece_map().items():
            x = sum(board.attacks(location).tolist()[32: 64]) if piece.symbol() in ['Q', 'N', 'B', 'P', 'R'] else 0
            total_attacked_square += x
    else:
        for location, piece in board.piece_map().items():
            x = sum(board.attacks(location).tolist()[0: 32]) if piece.symbol() in ['q', 'n', 'b', 'p', 'r'] else 0
            total_attacked_square += x
    return total_attacked_square
            
player = "Tal"

games_names = os.listdir("/home/sparkle/Chess/Data/Raw_game/" + player)

attacked_enemy_square_data = pd.DataFrame()

for name in games_names:
    with open("/home/sparkle/Chess/Data/Raw_game/" + player + "/" + name) as pgn:
        game = chess.pgn.read_game(pgn)
        board = game.board()
        color = "White" if player in game.headers['White'] else "Black"
        move_num = 0
        
        for move in game.mainline_moves():
            move_num += 1
            board.push(move)
            game_info = {
            'move_num': [move_num], 
            'player': [player], 
            'color': [color], 
            'file_name': [name], 
            'attacked_square_num': [compute_attacked_enemy_square(board, color)]}

            attacked_enemy_square_data = attacked_enemy_square_data.append(pd.DataFrame(game_info))

attacked_enemy_square_data.to_csv(player + '_attacked_square_info.csv', index = False)