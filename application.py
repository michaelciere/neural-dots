import numpy as np
from math import *

from state import State
from play import Engine

#from keras.models import Model
#from keras.models import model_from_json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, request, render_template, url_for
app = application = Flask(__name__)


def render_board(state):
    # render board as html

    def dot(x,y):
        dot = '<rect x=%d, y=%d, width=8, height=8, style=fill:gray></rect>' \
              % (x, y)
        return dot
    
    def hline(x,y):
        
        hline = '<rect x=%d, y=%d, width=65, height=8, style=fill:lightblue></rect>' % (x, y)
        return hline

    #vline = '<rect width=8, height=65, style=fill:lightblue><\rect>'

    height, width = 5, 5
    
    buffer = []
        
    ## do the top line
    for i in range(width):
        line = ((i, height), (i+1, height))

        x = (8+65)*i
        y = (8+65)*0
        buffer.append(dot(x,y))
        buffer.append(hline(x+8,y))
        # if line in self.lines:
        #     buffer.append("+--")
        # else:
        #     buffer.append("+  ")

    svg = '<div><svg>' + '\n'.join(buffer) + '</svg></div>'
    return svg
        
    # ## and now do alternating vertical/horizontal passes
    # for j in range(self.height-1, -1, -1):
    #     ## vertical:
    #     for i in range(self.width+1):
    #         line = ((i, j), (i, j+1))
    #         if line in self.lines:
    #             buffer.append("|")
    #         else:
    #             buffer.append(" ")
    #         if (i,j) in self.squares:
    #             buffer.append("%s " % self.squares[(i,j)])
    #         else:
    #             buffer.append("  ")


    #     ## horizontal
    #     for i in range(self.width):
    #         line = ((i, j), (i+1, j))
    #         if line in self.lines:
    #             buffer.append("+--")
    #         else:
    #             buffer.append("+  ")


    #     return ''.join(buffer)


def parse_moves(move_str):

    char2hcoord = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
    char2vcoord = {'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1, 'f': 0}

    moves = [move_str[i*3:i*3+3] for i in range(len(move_str) / 3)]

    moves_ = []
    for move in moves:
        if move[0] == 'h':
            point = (char2hcoord[move[2]],
                     char2vcoord[move[1]])
            move = (point, (point[0]+1, point[1]))
            moves_.append(move)
        elif move[0] == 'v':
            point = (char2hcoord[move[2]],
                     char2vcoord[move[1]])
            move = ((point[0], point[1]-1), point)
            moves_.append(move)

    return moves_

state = State()
engine = Engine()
player = 1
# page = open("play.html").read()


@app.route('/')
def play():
    return '<pre>' + state.__str__() + '</pre>'


#    return render_template('play.html')

# @app.route('/', methods=['POST'])
# def start(player):

#     state = State()
#     player = player

#     return 'State initialized'

    #while state.board.player != player \
    #      and not state.board.isGameOver():
    #    #comp_move = engine.make_move(state)
    #    comp_move, value = #engine.treesearch(state, seconds=5)
    #    state.board.play(comp_move)

    #return #render_template('play.html',
    #                       board=state.__str__(),
    #                       player = state.board.player)

    
@app.route('/', methods=['POST'])
def play_move():
    text = request.form['text']
    try:
        move = parse_moves(text)[0]
        if state.board.validMove(move):
            state.board.play(move)
    except Exception:
        return 0
    return 1


if __name__ == '__main__':

    application.debug = True
    application.run()

    
