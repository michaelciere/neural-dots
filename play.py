#!/usr/bin/env python
import numpy as np
from math import *

from state import State

from keras.layers import Input, Dense, Conv2D, Flatten, Activation
from keras.models import Model
from keras.models import model_from_json

import time

import copy

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def load_from_file(n=10000000):
    move_action_pairs = []
    with open('data/expert_moves.dat', 'r') as f:
        for row in f.read().splitlines()[:n]:
            position, move0, move1 = row.split(' ')
            position = np.array(list(position), dtype = np.uint8).reshape((10,10,3))
            move = (int(move0), int(move1))
            move_action_pairs.append((position, move))
    return move_action_pairs

def save_model(model):
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")

def load_model():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    
    loaded_model._make_predict_function()
    
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    return loaded_model




class Engine:

    def __init__(self):
        self.model = load_model()

    def make_move(self, state):
        ser = state.serialize()
        move_probs = self.model.predict(ser[np.newaxis,...]).ravel()

        while 1:
            move = np.random.choice(100, p = move_probs)
#             move = np.argmax(move_probs)
            move = (move/10, move%10) # check if this is correct
            move = state.unrotate_move(move)
            if state.board.validMove(move) \
               and not move in state.board.lines:
                break                

        return move
    
    def rollout(self, starting_state):
        
        state_ = copy.deepcopy(starting_state)

        while not state_.board.isGameOver():
            move = self.make_move(state_)
            state_.board.play(move)

        # who won?
        if state_.board.scores[0] > state_.board.scores[1]:
            result = 0
        else:
            result = 1

        return result

    def edges(self, ser):
        # get edges (moves) from curent node (position)
        idxs = np.where(ser[:,:,1].ravel() == 1)
        return idxs[0]

    
    def treesearch(self, starting_state, seconds=10):


        if seconds == 0:
            return self.make_move(starting_state), 0.0
        
        # do a Monte Carlo Tree Search
        ser = starting_state.serialize()
        root = {'player': starting_state.board.player,
                'visit_count': 0, 'action_value': 0.5, 'path': tuple(),
                'children': {}}

        max_depth = 1000
        num_rollouts = 1
        def traverse(node, state_, depth=0):
            if node['visit_count'] == 0:
                # first visit, set player
                node['player'] = state_.board.player
                
            node['visit_count'] += 1
            
            ser = state_.serialize()
            edges = self.edges(ser)
            # check if game is over
            if len(edges) == 0:
                scores = state_.board.scores
                if scores[0] > scores[1]:
                    value = 0.0
                elif scores[0] == scores[1]:
                    value = 0.5
                else:
                    value = 1.0

                node['action_value'] = value

            elif len(node['children']) == 0:
                if depth < max_depth \
                and (node['visit_count'] > 3 or len(node['path'])==0):
                    # expand leaf
                    move_probs = self.model.predict(ser[np.newaxis,...]).ravel()
                    node['prior'] = {edge: move_probs[edge]
                                     for edge in edges}
            
                    for edge in edges:
                        node['children'][edge] = {'player': None,
                                                  'visit_count': 0,
                                                  'action_value': 0.5,
                                                  'path': node['path'] + (edge,),
                                                  'children': {}}
                        
                # evaluate leaf
                value = float(self.rollout(state_))

                action_value = (node['visit_count'] - 1.) \
                            * node['action_value'] \
                            + value
                action_value *= 1. / node['visit_count']
                node['action_value'] = action_value
                
                # update values of parents
                # or maybe just return the value
            else:
                # not a leaf node, traverse further
                c_puct = 1.0 # exploration constant
                u_multiplier = sqrt(log(node['visit_count'])) * c_puct
                u = {i: u_multiplier * node['prior'][i] \
                     / sqrt(0.1 + child['visit_count'])
                     for i, child in node['children'].iteritems()}

                child_values = {i: child['action_value']
                                if node['player'] == 1
                                else (1. - child['action_value'])
                                for i, child in node['children'].iteritems()}
                
                probs = {i: u[i] + child_values[i]
                         for i, child in node['children'].iteritems()}

                move = max(probs, key=probs.get)
                move_ = state_.unrotate_move((move/10, move%10))
                state_.board.play(move_)

                value = traverse(node['children'][move],
                                 state_, depth+1)
                    
                action_value = (node['visit_count'] - 1.) \
                            * node['action_value'] \
                            + value
                action_value *= 1. / node['visit_count']
                node['action_value'] = action_value

            return value

        start = time.clock()
        while (time.clock() - start) < seconds:
            state_ = copy.deepcopy(starting_state)
            traverse(root, state_)
        
        def transform_move(move):
            return starting_state.unrotate_move((move/10, move%10))
            
        # print {transform_move(child_k): child_v['visit_count']
        #        for child_k, child_v in root['children'].iteritems()
        #        if child_v['visit_count'] > 0}
        
        # print root['prior']
        
        visit_counts = {k: child['visit_count']
                        for k, child in root['children'].iteritems()}
        return transform_move(max(visit_counts,
                                  key = visit_counts.get)), root['action_value']
    
    
            #i, child in root['children'].iteritems():
#            print child['visit_count'], child['action_value']
    
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
    

if __name__ == '__main__':

    state = State()
    
    engine = Engine()

    # state = State()
    # print state, '\n'
    # while not state.board.isGameOver():
    #     move, value = engine.treesearch(state, seconds=60)
    #     state.board.play(move)
    #     print state, '\n'
    #     print value
    #     print 'Player %d to play' % state.board.player
    # print state.board.scores

    
    # position, _ = load_from_file(n=1)[0]
    import urllib2
    url = 'https://www.littlegolem.net/servlet/sgf/1488860/game1488860.txt'
    url2 = 'https://www.littlegolem.net/servlet/sgf/1488860/game1488860.txt'
    url3 = 'https://www.littlegolem.net/servlet/sgf/1495378/game1495378.txt'
    response = urllib2.urlopen(url3)
    txt = response.read()
    
    game_str = txt
    print txt

    from load_expert_moves import ExpertGames
    games = ExpertGames()
    position = games.extract(game_str)[25][0]
    
    state = State()
    state.deserialize(position)

#    move = ((5,0), (5,1))
#    state.board.play(move)
    
    print state
    print 'player %d to move' % state.board.player

    def test_mcts():
        move, value = engine.treesearch(state, 30)
        print move, value

    
    

    
    # start = time.clock()
    # for _ in range(100):
    #    state.deserialize(position)
    #    result = engine.rollout(state)
    #    results.append(result)

    # print sum(results) / float(len(results))

    # print 'seconds per rollout: %.2f' % ((time.clock() - start) / 100.)
