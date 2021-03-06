#!/usr/bin/env python

"""
Implements a dots-and boxes board.
"""

import types

class DotsBoard:
    def __init__(self, width=5, height=5):
        """
        Initializes a rectangular gameboard.
        width and height are interpreted as number of boxes, not dots
        """
        self.width, self.height = width, height
        assert 2 <= self.width and 2 <= self.height,\
               "Game can't be played on this board's dimension."
        self.lines = set() # moves that have been played (by either player)
        self.squares = {} # captured squares
        self.scores = {0: 0, 1: 0}
        self.player = 0 # whose turn it is

    def createPosition(self, lines, player, score0, score1):
        self.player = player
        for move in lines:
            self.lines.add(move)
        self.scores[0] = score0
        self.scores[1] = score1
        
    def isGameOver(self):
        """Returns true if no more moves can be made.
        The maximum number of lines drawn is
        w * (h+1) + h * (w+1) = 2*w*h + w + h
        """
        w, h = self.width, self.height
        return len(self.lines) == 2*w*h + h + w

    def validMove(self, move):
        if (self._isGoodCoord(move[0]) \
            and self._isGoodCoord(move[1])):
            return True
        return False

    def validSquare(self, square):
        x1, y1 = square
        if x1 + 1 <= self.width and y1 + 1 <= self.height:
            return True
        else:
            return False
    
    def square2lines(self, square):
        """
        returns the four lines that make up a square.
        A square is represented by the coordinates of
        its lower left corner
        """
        x1, y1 = square
        lines = [((x1,y1),(x1+1,y1)),
                 ((x1,y1),(x1,y1+1)),
                 ((x1+1,y1),(x1+1,y1+1)),
                 ((x1,y1+1),(x1+1,y1+1))]

        return lines
        
    def capturedSquares(self, move):
        """
        Returns a list of the the lower left
        corners of the squares captured by a move. (at most two)
        """
        assert self.validMove(move)
        (x1, y1), (x2, y2) = move
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y1, y2
            
        captured_squares = []
        if self._isHorizontal(move):
            # check squares above and below line
            square_below = (x1, y1 - 1)
            square_above = (x1, y1)
            if (self.validSquare(square_below) \
                and all(line in self.lines
                        for line in self.square2lines(square_below))):
                captured_squares.append(square_below)
            if (self.validSquare(square_above) \
                and all(line in self.lines
                        for line in self.square2lines(square_above))):
                captured_squares.append(square_above)
        else:
            # check squares to the left and to the right of line
            square_left = (x1 - 1, y1)
            square_right = (x1, y1)
            if (self.validSquare(square_left) \
                and all(line in self.lines
                        for line in self.square2lines(square_left))):
                captured_squares.append(square_left)
            if (self.validSquare(square_right) \
                and all(line in self.lines
                        for line in self.square2lines(square_right))):
                captured_squares.append(square_right)

        return captured_squares

    def _isHorizontal(self, move):
        "Return true if the move is in horizontal orientation."
        return abs(move[0][0] - move[1][0]) == 1

    def _isVertical(self, move):
        "Return true if the move is in vertical orientation."
        return not self.isHorizontal(self, move)
    
    def play(self, move):
        """Place a particular move on the board.  If any wackiness
        occurs, raise an AssertionError.  Returns a list of
        bottom-left corners of squares captured after a move."""
        assert (self._isGoodCoord(move[0]) and
                self._isGoodCoord(move[1])),\
                "Bad coordinates, out of bounds of the board."
        move = self._makeMove(move[0], move[1])
        assert(not move in self.lines),\
                   "Bad move, line already occupied."
        self.lines.add(move)
        ## Check if a square is completed.
        square_corners = self.capturedSquares(move)
        if len(square_corners) > 0:
            for corner in square_corners:
                self.squares[corner] = self.player
                self.scores[self.player] += 1
        else:
            self._switchPlayer()
        return square_corners

    def _makeMove(self, move0, move1):
        assert self.validMove((move0, move1))
        if move0[0] > move1[0] or move0[1] > move1[1]:
            return (move1, move0)
        else:
            return (move0, move1)
    
    def _switchPlayer(self):
        self.player = (self.player + 1) % 2

    def __str__(self):
        """Return a nice string representation of the board."""
        buffer = []
        
        ## do the top line
        for i in range(self.width):
            line = ((i, self.height), (i+1, self.height))
            if line in self.lines:
                buffer.append("+--")
            else: buffer.append("+  ")
        buffer.append("+\n")

        ## and now do alternating vertical/horizontal passes
        for j in range(self.height-1, -1, -1):
            ## vertical:
            for i in range(self.width+1):
                line = ((i, j), (i, j+1))
                if line in self.lines:
                    buffer.append("|")
                else:
                    buffer.append(" ")
                if (i,j) in self.squares:
                    buffer.append("%s " % self.squares[(i,j)])
                else:
                    buffer.append("  ")
            buffer.append("\n")

            ## horizontal
            for i in range(self.width):
                line = ((i, j), (i+1, j))
                if line in self.lines:
                    buffer.append("+--")
                else: buffer.append("+  ")
            buffer.append("+\n")

        return ''.join(buffer)

    def _isGoodCoord(self, coord):
        """Returns true if the given coordinate is good.
        A coordinate is "good" if it's within the boundaries of the
        game board, and if the coordinates are integers."""
        return (0 <= coord[0] <= self.width+1
                and 0 <= coord[1] <= self.height+1
                and type(coord[0]) is int
                and type(coord[1]) is int)
    

def _test(width, height):
    """A small driver to make sure that the board works.  It's not
    safe to use this test function in production, because it uses
    input()."""
    board = DotsBoard(width, height)
    turn = 1
    scores = [0, 0]
    while not board.isGameOver():
        print "Turn %d (Player %s)" % (turn, board.player)
        print board
        move = input("Move? ")
        squares_completed = board.play(move)
        if squares_completed:
            print "Square completed."
            scores[self.player] += len(squares_completed)
        turn = turn + 1
        print "\n"
    print "Game over!"
    print "Final board position:"
    print board
    print
    print "Final score:\n\tPlayer 0: %s\n\tPlayer 1: %s" % \
          (scores[0], scores[1])



if __name__ == "__main__":
    """If we're provided arguments, try using them as the
    width/height of the game board."""
    import sys
    if len(sys.argv[1:]) == 2:
        _test(int(sys.argv[1]), int(sys.argv[2]))
    elif len(sys.argv[1:]) == 1:
        _test(int(sys.argv[1]), int(sys.argv[1]))
    else:
        _test(5, 5)

    
