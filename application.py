import numpy as np
from math import *

from state import State
from play import Engine

from keras.models import Model
from keras.models import model_from_json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, request, render_template, url_for
app = application = Flask(__name__)


state = State()
engine = Engine()

@app.route('/')
def play():
    global state
    state = State()
    return render_template('play.html')

@app.route('/', methods=['GET', 'POST'])
def move():
    global state
    move = request.form['move']
    if move[0] == "c":
        # return computer move
#        comp_move = engine.make_move(state)
        seconds = float(move[1:])
        comp_move, _ = engine.treesearch(state, seconds=seconds)
        state.board.play(comp_move)
        move_str = '%d%d%d%d' % \
                   (comp_move[0][0], comp_move[0][1],
                    comp_move[1][0], comp_move[1][1])
        return move_str
    else:    
        try:
            move = ((int(move[0]), int(move[1])),
                    (int(move[2]), int(move[3])))
            if state.board.validMove(move):
                state.board.play(move)
                return "succes"
        except Exception:
            return 'fail'




if __name__ == '__main__':

    application.debug = True
    application.run()

    
