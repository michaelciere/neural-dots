#!/usr/bin/env python

import numpy as np
import urllib2

from state import State

from load_expert_moves import ExpertGames

def mirror_and_rotate(position, move):
    # there are 8 rotations and reflections
    all_versions = [0] * 8

    all_versions[0] = position
    all_versions[1] = np.rot90(position, k=1)
    all_versions[2] = np.rot90(position, k=2)
    all_versions[3] = np.rot90(position, k=3)
    
    all_versions[4] = np.flip(position, axis=0)
    all_versions[5] = np.flip(position, axis=1)
    all_versions[6] = np.rot90(np.flip(position, axis=0), k=1)
    all_versions[7] = np.rot90(np.flip(position, axis=1), k=1)

    x, y = move
    all_moves = [(x, y),
                 (9 - y, x),
                 (9 - x, 9 - y),
                 (y, 9 - x),
                 (9 - x, y),
                 (x, 9 - y),
                 (9 - y, 9 - x),
                 (y, x)]
                     
    return zip(all_versions, all_moves)

def load_from_file(n=None):
    move_action_pairs = []
    with open('data/expert_moves.dat', 'r') as f:
        lines = f.read().splitlines()
        if n is None or n>len(lines):
            n = len(lines)
        idxs = np.random.randint(len(lines), size = n)
        for idx in idxs:
            position, move0, move1 = lines[idx].split(' ')
            position = np.array(list(position), dtype = np.uint8).reshape((10,10,3))
            move = (int(move0), int(move1))
            move_action_pairs.append((position, move))
    return move_action_pairs

def save_to_file(pos_move_pairs):

    with open('data/expert_moves_augmented.dat', 'w') as f:
        for position, move in pos_move_pairs:
            f.write(''.join(map(str, position.flatten())))
            f.write(' %d %d\n' % (move[0], move[1]))




if __name__ == '__main__':

    print 'loading data...'
    pos_move_pairs = load_from_file(n=1000000)
    print 'finished loading data'
    print 'start augmenting'
    
    pos_move_pairs_aug = []

    for i, (pos, move) in enumerate(pos_move_pairs):
        if i % 5000 == 0:
            print i
        pos_move_pairs_aug.extend(mirror_and_rotate(pos, move))

    print len(pos_move_pairs_aug)

    save_to_file(pos_move_pairs_aug)
    
    # pos, move = load_from_file(n=1)[0]
    # print pos[:,:,0]
    # pos_aug, moves_aug = mirror_and_rotate(pos, move)

    # for pos, move in zip(pos_aug, moves_aug):
    #     state = State()
    #     state.deserialize(pos)
    #     move = state.unrotate_move(move)
    #     print state
    #     print move, '\n'
        


