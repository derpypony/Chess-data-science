import os
import chess.pgn
import pandas as pd

def compute_sac(piece_in_from_square, piece_in_to_square, color):
    # note that some moves will sac piece but are still not down exchange in the next moves
    # I will still count them as piece sac, Anand-Viswanathan_vs_Van-Der-Wiel-John-T-H_1990.__.__.pgn have a line bxg5
    # which is not in conventional sense, a piece sac, but i will still count it as a piece sac, because the knight died
    # to make room for bishop
    sac_value = 0
    White_dic = {chess.Piece.from_symbol('Q'): 10, 
        chess.Piece.from_symbol('R'): 5,
        chess.Piece.from_symbol('B'): 3.5,
        chess.Piece.from_symbol('N'): 3.5,
        chess.Piece.from_symbol('P'): 1,
        chess.Piece.from_symbol('K'): 100}

    Black_dic = {chess.Piece.from_symbol('q'): 10, 
        chess.Piece.from_symbol('r'): 5,
        chess.Piece.from_symbol('b'): 3.5,
        chess.Piece.from_symbol('n'): 3.5,
        chess.Piece.from_symbol('p'): 1,
        chess.Piece.from_symbol('k'): 100}

    dic = White_dic if color == 'White' else Black_dic
    opponent_dic = White_dic if color == 'Black' else Black_dic
    if not piece_in_to_square:
        sac_value = dic[piece_in_from_square]
    else:
        if dic[piece_in_from_square] > opponent_dic[piece_in_to_square]:
            sac_value = dic[piece_in_from_square] - opponent_dic[piece_in_to_square]
    return sac_value


player = "Tal"

games_names = os.listdir("/home/sparkle/Chess/Data/Raw_game/" + player)

piece_sac_data = pd.DataFrame()

for name in games_names:
    with open("/home/sparkle/Chess/Data/Raw_game/" + player + "/" + name) as pgn:
        game = chess.pgn.read_game(pgn)
        board = game.board()
        move_num = 0
        total_sum = 0
        sac_value = 0
        color = "White" if player in game.headers['White'] else "Black"
        if color == 'White':
            for move in game.mainline_moves():
                move_num += 1
                from_square = move.from_square
                to_square = move.to_square
                piece_in_from_square = board.piece_at(from_square)
                piece_in_to_square = board.piece_at(to_square)
                if move_num % 2 == 0: # black move
                    if to_square == white_last_square:
                        total_sum += sac_value
                else: # white move
                    white_last_square = to_square
                    sac_value = compute_sac(piece_in_from_square, piece_in_to_square, color)
                board.push(move)
        else:
            black_last_square = None
            for move in game.mainline_moves():
                move_num += 1
                from_square = move.from_square
                to_square = move.to_square
                piece_in_from_square = board.piece_at(from_square)
                piece_in_to_square = board.piece_at(to_square)
                if move_num % 2 == 1: # white move
                    if to_square == black_last_square:
                        total_sum += sac_value
                else: # black move
                    black_last_square = to_square
                    sac_value = compute_sac(piece_in_from_square, piece_in_to_square, color)
                board.push(move)
        info_dic = {'player': [player], 'color': [color], 'moves': [move_num], 'total_sac': [total_sum], 'file_name': [name]}
        piece_sac_data = piece_sac_data.append(pd.DataFrame(info_dic))

piece_sac_data.to_csv(player + '_piece_sac_data.csv', index = False)