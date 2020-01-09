"""This script is used to parse raw chess game data(pgn file) to csv file. 
Please note that in raw pgn files, there are more information 
about the game like 'Round' and 'Source', I ommited them in the output csv file"""
import os
import chess.pgn
import pandas as pd

game_data = pd.DataFrame()
"""I will use Kasparov's games to demonstrate"""
player = "Fischer"
"""Your computer will have different path, take the path in my computer for example"""
games_names = os.listdir("/home/sparkle/Chess/" + player)
for name in games_names:
    with open("/home/sparkle/Chess/" + player + "/" + name) as pgn:
        game = chess.pgn.read_game(pgn)

        color = "White" if player in game.headers['White'] else "Black"
        opponent_color = 'White' if color == 'Black' else 'Black'
        opponent = game.headers[opponent_color]
        """because there are a lot of pgn files can't be read properly, we need a lot of try catch phrase"""
        try:
            player_Elo = game.headers[color + 'Elo']
        except:
            player_Elo = None

        try:
            opponent_Elo = game.headers[opponent_color + 'Elo']
        except:
            opponent_Elo = None
        
        try:
            site = game.headers['Site']
        except:
            site = None

        try:
            date = game.headers['Date']
        except:
            date = None
        
        try:
            event = game.headers['Event']
        except:
            event = None

        try:
            lines = str(game.mainline_moves())
        except:
            lines = None
        """I can't find build-in function to calculate move counts of the game, so I implement one myself. 
        However, unlike the convention that after white and black eack makes one move, move count += 1, 
        for each player makes one move, move count +=1, that means my move count will be roughly twice the convention move count.
        For example, 1. e4, e5 will be counted as one move in convention standard, my standard will count it as two moves. """
        if game.mainline_moves():
            moves = 0
            for move in game.mainline_moves():
                moves += 1
        else:
            moves = None

        try:
            if (color == 'White' and game.headers['Result'] == '1-0') or (color == 'Black' and game.headers['Result'] == '0-1'):
                result = 'Win' 
            elif game.headers['Result'] == '1/2-1/2':
                result = 'Draw'
            else:
                result = 'Lose'
        except:
            result = None

        game_info = {'player': [player], 
        'color': [color], 
        'opponent': [opponent], 
        'player_Elo':[player_Elo],
        'opponent_Elo': [opponent_Elo],
        'result': [result],
        'event': [event],
        'site': [site],
        'date': [date],
        'lines': [lines],
        'moves': [moves],
        'file_name': [name]}

        game_data = game_data.append(pd.DataFrame(game_info))
game_data.to_csv(player + '.csv', index = False)

# import io
# with open("/home/sparkle/Chess/Nakamura/Zugic,-I._vs_Nakamura,-H._2007.09.27.pgn") as pgn:
#     game = chess.pgn.read_game(pgn)
#     board = game.board()
#     x = str(game.mainline_moves())
#     y = io.StringIO(x)
#     game_1 = chess.pgn.read_game(y)
#     board_1 = game_1.board()
#     print(game_1)
    # for move in game.mainline_moves():
    #     board.push(move)
    #     print(game.mainline_moves())
       