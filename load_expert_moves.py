#!/usr/bin/env python

import numpy as np
import urllib2

from state import State

class ExpertGames:

    def __init__(self):

        pass


    def extract(self, game_str, p0=True, p1=True):
        lines = game_str.splitlines()
        assert lines[1][6:9] == '"5"'
        p0name = lines[3].split('"')[1]
        p1name = lines[5].split('"')[1]
        #print p0name, 'vs.', p1name

        try:
            game_str = lines[9]
        except IndexError:
            # game over before any moves were played
            return None
        turns = game_str.split(';')[1:]

        move_action_pairs = []
        
        state = State()
        for turn in turns:
            moves = state.convert_lg_turn(turn)
            for move in moves:
                if (state.board.player == 0 and p0 is True) \
                   or (state.board.player == 1 and p1 is True):
                    position = state.serialize()
                    move_ = state.rotate_move(move)
                    move_action_pairs.append((position, move_))
                
                state.board.play(move)
            
        return move_action_pairs

    def save_to_file(self, move_action_pairs):
        
        with open('data/expert_moves.dat', 'w') as f:    
            for position, move in move_action_pairs:
                f.write(''.join(map(str, position.flatten())))
                f.write(' %d %d\n' % (move[0], move[1]))

    def load_from_file(self):
        move_action_pairs = []
        with open('data/expert_moves.dat', 'r') as f:
            for row in f.read().splitlines():
                position, move0, move1 = row.split(' ')
                position = np.array(list(position), dtype = np.uint8).reshape((10,10,3))
                move = (int(move0), int(move1))
                move_action_pairs.append((position, move))
        return move_action_pairs

    def get_game_strings(self, txt, n=10000000000):
        lines = txt.splitlines()
        i = 0
        while i*11 < len(lines) and i < n:
            if i+10 > len(lines):
                break
            yield '\n'.join(lines[i*11:i*11+10])
            i += 1


if __name__ == "__main__":
    
    games = ExpertGames()

    move_action_pairs = []
    n_moves = 0
    
    with open('data/p0_expert_games.txt', 'r') as f:
        txt = f.read()
    for i, game_str in enumerate(games.get_game_strings(txt)):
        ma_pairs = games.extract(game_str, p0=True, p1=False)
        if ma_pairs is not None:
            move_action_pairs.extend(ma_pairs)
            n_moves += len(ma_pairs)

        if i % 100 == 0:
            print n_moves, '\t moves'

    with open('data/p1_expert_games.txt', 'r') as f:
        txt2 = f.read()
    for i, game_str in enumerate(games.get_game_strings(txt2)):
        ma_pairs = games.extract(game_str, p0=False, p1=True)
        if ma_pairs is not None:
            move_action_pairs.extend(ma_pairs)
            n_moves += len(ma_pairs)

        if i % 100 == 0:
            print n_moves, '\t moves'
    
            
    games.save_to_file(move_action_pairs)
    move_action_pairs2 = games.load_from_file()
    
    for ma1, ma2 in zip(move_action_pairs, move_action_pairs2):
        assert np.array_equal(ma1[0], ma2[0])
        assert ma1[1] == ma2[1]

