import numpy as np
from math import *
import re


from state import State
from play import Engine

from keras.models import Model
from keras.models import model_from_json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, request, render_template, url_for, redirect
app = application = Flask(__name__)

def render_board(state, state_str, player):
    # render board as html

    # if len(state.board.lines) > 0:
    #     state_str = 'l'.join(['%s%s%s%s' % (line[0][0], line[0][1],
    #                                         line[1][0], line[1][1])
    #                           for line in state.board.lines])
    # else:
    #     state_str = None

    player_to_move = 'r' if state.board.player == 0 else 'b'

    if player_to_move == player:
        to_move = True
    else:
        to_move = False
        
    if state_str is not None:
        move_strings = re.split('r|b', state_str)
        last_move = move_strings[-1]
    else:
        move_strings = set()
        last_move = ''

    
    def dot(x,y):
        dot = '<rect x="%d", y="%d", width="8", height="8", style=fill:gray></rect>' \
              % (x, y)
        return dot

    
    def hline(x,y, id_str, played=False, last=False):
        if state_str is None:
            state_str_new = player_to_move + id_str
        else:
            state_str_new = state_str + player_to_move +  id_str

        
        if to_move and (not played):
            line_str = '<a href= "?g=%s">' % state_str_new
        else:
            line_str = ''

        if (not played):
            colour = 'lightblue'
        else:
            if last:
                colour = 'red'
            else:
                colour = 'black'
        
        line_str += '<rect class="line", x="%d", y="%d", width="65", height="8", style="fill:%s"></rect>' % (x, y, colour)

        if (not played) and to_move:
            line_str += '</a>'
        
        return line_str

    
    def vline(x,y, id_str, played=False, last=False):
        if state_str is None:
            state_str_new = player_to_move + id_str
        else:
            state_str_new = state_str + player_to_move +  id_str

        if to_move and (not played):
            line_str = '<a href= "?g=%s">' % state_str_new
        else:
            line_str = ''

        if (not played):
            colour = 'lightblue'
        else:
            if last:
                colour = 'red'
            else:
                colour = 'black'

        line_str += '<rect class="line", x="%d", y="%d", width="8", height="65", style="fill:%s"></rect>' % (x, y, colour)

        if (not played) and to_move:
            line_str += '</a>'

        return line_str
    
    
    height, width = 5, 5
    
    buffer = []

    # horizontal lines and dots
    for j in range(height+1):
        for i in range(width):
            x = (8+65)*i
            y = (8+65)*(height - j)
            buffer.append(dot(x,y))
            id_str = '%d%d%d%d' % (i, j, i+1, j)
            last = False
            if id_str in move_strings:
                played = True
                if id_str == last_move:
                    last = True
            else:
                played = False
            buffer.append(hline(x+8,y, id_str, played, last))
        buffer.append(dot(x+65+8,y))

    # vertical lines
    for j in range(height):
        for i in range(width+1):
            line = ((i, j), (i, j+1))

            x = (65+8)*i
            y = 8 + (8+65)* (height - j - 1)
            id_str = '%d%d%d%d' % (i, j, i, j+1)
            last = False
            if id_str in move_strings:
                played = True
                if id_str == last_move:
                    last = True
            else:
                played = False
            buffer.append(vline(x, y, id_str, played, last))

    # boxes
    for box, plyr in state.board.squares.iteritems():
        if plyr == 0:
            colour = 'red'
        elif plyr == 1:
            colour = 'blue'

        x = 8 + int(box[0]) * (65+8)
        y = 8 + (4 - int(box[1])) * (65+8)
        
        square = '<rect x = "%s", y = "%s", height="65", width="65", style="fill:%s; opacity:0.5"></rect>' % (x,y,colour)

        buffer.append(square)
            
            
    svg = '<div><svg class = "board", width = "374", height = "374">' + '\n'.join(buffer) + '</svg></div>'
    return svg


engine = Engine()

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/play/<player>')
def play(player):

    state_str = request.args.get('g')
    
    state = State()
    if state_str is not None:
        for m in re.split('r|b', state_str)[1:]:
            move = ((int(m[0]), int(m[1])),
                    (int(m[2]), int(m[3])))
            state.board.play(move)
            
    board_html = render_board(state, state_str, player)

    p_to_move = 'Red' if state.board.player == 0 else 'Blue'
    return render_template("play.html", board=board_html,
                           player_to_move = p_to_move,
                           score = '%d-%d' % (state.board.scores[0],
                                              state.board.scores[1]))

@app.route('/play/<player>', methods=['POST'])
def move(player):
    state_str = request.args.get('g')
    state = State()
    if state_str is not None:
        for m in re.split('r|b', state_str)[1:]:
            move = ((int(m[0]), int(m[1])),
                    (int(m[2]), int(m[3])))
            state.board.play(move)

    if state.board.isGameOver():
        return 'finished'
            

    if len(state.board.lines) < 27:
        comp_move = engine.make_move(state)
    else:
        comp_move, _ = engine.treesearch(state, seconds=4)
        
    player_to_move = 'r' if state.board.player == 0 else 'b'
    
    state.board.play(comp_move)
    
    
    move_str = '%s%d%d%d%d' % \
               (player_to_move,
                comp_move[0][0], comp_move[0][1],
                comp_move[1][0], comp_move[1][1])

    return move_str





if __name__ == '__main__':

    application.debug = True
    application.run()

    
