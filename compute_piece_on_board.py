import os
import chess.pgn
import pandas as pd
import statistics

def count_pieces(piece_map, color, move_num):
    queen = 0
    rook = 0
    knight = 0
    bishop = 0
    pawn = 0
    if color == "White":
        for item in piece_map.items():
            if item[1].symbol() == 'Q':
                queen += 1
            elif item[1].symbol() == 'R':
                rook += 1
            elif item[1].symbol() == 'N':
                knight += 1
            elif item[1].symbol() == 'B':
                bishop += 1
            elif item[1].symbol() == 'P':
                pawn += 1
    else:
        for item in piece_map.items():
            if item[1].symbol() == 'q':
                queen += 1
            elif item[1].symbol() == 'r':
                rook += 1
            elif item[1].symbol() == 'n':
                knight += 1
            elif item[1].symbol() == 'b':
                bishop += 1
            elif item[1].symbol() == 'p':
                pawn += 1
    
    return {'queen': [queen], 'rook': [rook], 'knight': [knight], 'bishop': [bishop], 'pawn': [pawn], 'move_num': move_num}

player = "Morphy"

# Get all the file names from the folder, different computer have different path

games_names = os.listdir("/home/sparkle/Chess/" + player)

piece_info_data = pd.DataFrame()

for name in games_names:

    with open("/home/sparkle/Chess/" + player + "/" + name) as pgn:
        
        try:
            # some game can't be read properly
            game = chess.pgn.read_game(pgn)
            board = game.board()
            color = "White" if player in game.headers['White'] else "Black"

            df = pd.DataFrame()
            move_num = 0

            for move in game.mainline_moves():
                board.push(move)
                move_num += 1
                x = count_pieces(board.piece_map(), color, move_num)
                df = df.append(pd.DataFrame(x))

            df['file_name'] = name
            df['color'] = color
            df['player'] = player
            piece_info_data = piece_info_data.append(df)
        except:
            print(name + " can't be read properly")
        

piece_info_data.to_csv(player + '_piece_info.csv', index = False)