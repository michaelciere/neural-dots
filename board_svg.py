#!/usr/bin/env python

from state import State

def render_board(state):
    # render board as html

    state_str = ''.join(['%s%s%s%s' % (line[0][0], line[0][1], line[1][0], line[1][1])
     for line in state.board.lines])
    
    def dot(x,y):
        dot = '<rect x="%d", y="%d", width="8", height="8", style=fill:gray></rect>' \
              % (x, y)
        return dot

    
    def hline(x,y, id_str, played=False, to_move=True):
        state_str_new = state_str + id_str
        if (not played) and to_move:
            line_str = '<a href= "{{url_for("play", player=player,state=%s) }}">' % state_str_new
        else:
            line_str = ''
        
        line_str += '<rect class="line", x="%d", y="%d", width="65", height="8", style="fill:lightblue"></rect>' % (x, y)

        if (not played) and to_move:
            line_str += '</a>'
        
        return line_str

    
    def vline(x,y, id_str, played=False, to_move=True):
        state_str_new = state_str + id_str
        if (not played) and to_move:
            line_str = '<a href= "{{url_for("play", player=player,state=%s) }}">' % state_str_new
        else:
            line_str = ''

        line_str += '<rect class="line", x="%d", y="%d", width="8", height="65", style="fill:lightblue"></rect>' % (x, y)

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
            buffer.append(hline(x+8,y, id_str))
        buffer.append(dot(x+65+8,y))

    # vertical lines
    for j in range(height):
        for i in range(width+1):
            line = ((i, j), (i, j+1))

            x = (65+8)*i
            y = 8 + (8+65)* (height - j - 1)
            id_str = '%d%d%d%d' % (i, j, i, j+1)
            buffer.append(vline(x, y, id_str))

            
    svg = '<div><svg class = "board", width = "374", height = "374">' + '\n'.join(buffer) + '</svg></div>'
    return svg


if __name__ == '__main__':

    state = State()

    move = ((2,2),(3,2))
    state.board.play(move)
    print render_board(state)
