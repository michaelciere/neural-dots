from state import State


def render_board(state):
    # render board as html

    def dot(x,y):
        dot = '<rect x="%d", y="%d", width="8", height="8", style=fill:gray></rect>' \
              % (x, y)
        return dot
    
    def hline(x,y, id_str):
        hline_str = '<rect class="line", id="%s", x="%d", y="%d", width="65", height="8", style="fill:lightblue; cursor:pointer"></rect>' % (id_str, x, y)
        return hline_str

    def vline(x,y, id_str):
        vline_str = '<rect class="line", id="%s", x="%d", y="%d", width="8", height="65", style="fill:lightblue; cursor:pointer"></rect>' % (id_str, x, y)
        return vline_str
    
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
    print render_board(state)
