#!/usr/bin/env python

import numpy as np
from math import *

from board import DotsBoard


class State(object):

    def __init__(self, width=5, height=5):
        # width / height in boxes, not dots
        assert width==5 and height==5
        self.w = width
        self.h = height
        self.board = DotsBoard(width, height)

        self.possible_moves_mask = np.zeros((10,10))
        for i in range(5):
            for j in range(6):
                horiz_move = ((i,j),(i+1,j))
                assert self.board.validMove(horiz_move)
                x,y = self.rotate_move(horiz_move)
                self.possible_moves_mask[x,y] = 1
                vert_move = ((j,i),(j,i+1))
                assert self.board.validMove(vert_move)
                x2,y2 = self.rotate_move(vert_move)
                self.possible_moves_mask[x2,y2] = 1

                
    def __str__(self):
        return self.board.__str__()

    def convert_lg_turn(self, move_str):
        if move_str[0] == 'b':
            player = 0
        elif move_str[0] == 'r':
            player = 1
        else:
            raise ValueError('invalid move')
        
        char2hcoord = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
        char2vcoord = {'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1, 'f': 0}
 
        moves = []        
        offset = 2
        while 1:
            if move_str[offset] == 'h':
                point = (char2hcoord[move_str[offset + 2]],
                         char2vcoord[move_str[offset + 1]])
                move = (point, (point[0]+1, point[1]))
                moves.append(move)
                offset += 3
            elif move_str[offset] == 'v':
                point = (char2hcoord[move_str[offset + 2]],
                         char2vcoord[move_str[offset + 1]])
                move = ((point[0], point[1]-1), point)
                moves.append(move)
                offset += 3
            else:
                break
                
        return moves
                
    def play_lg_turn(self, turn_str):

        moves = self.convert_lg_turn(turn_str)
        for move in moves:
            self.board.play(move)

    def rotate_move(self, move):
        x, y = ((move[0][0] + move[1][0]) / 2.0 - 2.5,
                (move[0][1] + move[1][1]) / 2.0 - 2.5)
        x2, y2 = int(x - y + 4.5), int(x + y + 4.5)
        return x2, y2

    def unrotate_move(self, rot_move):

        x, y = rot_move
        x, y = x - 4.5, y - 4.5
        x, y = (x + y) / 2.0 + 2.5, (y - x) / 2.0 + 2.5
        
        move = ((int(floor(x)), int(floor(y))),
                (int(ceil(x)), int(ceil(y))))

        assert(self.rotate_move(move) == rot_move)
        return move
        
    def serialize(self):
        """
        represent a dots board as a binary tensor
        """
        gstate = np.zeros((10,10, 3), dtype=np.uint8)

        gstate[:,:,1] = self.possible_moves_mask
        for move in self.board.lines:
            x, y = self.rotate_move(move)
            gstate[x,y,0] = 1
            gstate[x,y,1] = 0
        if self.board.player == 1:
            gstate[:,:,2] = 1

        return gstate

    def deserialize(self, gstate):

        player = gstate[0,0,2]

        rotated_moves = zip(*np.where(gstate[:,:,0] == 1))

        moves = [self.unrotate_move(rot_move)
                 for rot_move in rotated_moves]

        self.board = DotsBoard(5,5)
        self.board.createPosition(moves, player, 0,0)
        
        

if __name__ == "__main__":
    
    game_str = ';b[hdb];r[vce];b[hec];r[hbc];b[vdd];r[vac];b[hcd];r[vbb];b[hcc];r[hca];b[hcb];r[veb];b[vdb];r[ved];b[hda];r[hbe];b[hed];r[hce];b[vae];r[hee];b[vab];r[hfa];b[vdf];r[hfe];b[had];r[haa];b[hfb];r[vaf];b[haevbe];r[vbfhfd];b[veevefhea];r[vdaveavaa];b[hbavbavcb];r[vcavccvad];b[hbdvbdvbchachab];r[hbbhdd];b[vdevcdhdevcfhdcvdchebvechfc]'

    turns = game_str.split(';')[1:]
        
    state = State()
    for turn in turns[:5]:
        print state, '\n'
        state.play_lg_turn(turn)
    print state

    print 'score: %d-%d' % (state.board.scores[0], state.board.scores[1])

    ser = state.serialize()
    print ser[:,:,1]

    print '\n'

    state.deserialize(ser)
    print state

    # state = State()
    # for turn in turns:
    #     state.play_lg_turn(turn)
    # all_moves = state.board.lines
    # mask = np.zeros((10,10), dtype=bool)
    # for move in all_moves:
    #     x, y = state.rotate_move(move)
    #     mask[x,y] = True
