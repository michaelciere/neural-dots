#!/usr/bin/env python
import numpy as np
from math import *

from state import State

from keras.models import Model
from keras.models import model_from_json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask
app = Flask(__name__)


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

    


@app.route("/")
def hello():
    state = State()

    html = '<pre>%s</pre>' \
           % state.__str__()

    html = render_board(state)
    
    return html


if __name__ == '__main__':

    state = State()
    print render_board(state)
