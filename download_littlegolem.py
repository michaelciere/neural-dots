#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

# compile list of all playerids who have played in championship league 1

def extract_player_ids(txt):
    players = set()
    player_names = set()
    for line in txt.splitlines():
        if line[:9] == '[YellowId' \
           or line[:6] == '[RedId':
            plid = int(line.split('"')[1])
            players.add(plid)
        elif line[:7] == '[Yellow' \
             or line[:4] == '[Red':
            plname = line.split('"')[1]
            player_names.add(plname)
    return players, player_names

def get_championship_players():

    base_url = 'https://www.littlegolem.net/jsp/tournament/tournament.jsp?trnid=dots.ch.'

    players = set()
    player_names = set()
    for i in range(1,51,1):
        print 'processing championship %d.1.1' % i
        url = base_url + str(i) + '.1.1'
        
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        
        for link in soup.findAll('a', href=True, text='PGN/SGF'):
            SGF_link = link['href']
            
        response = urllib2.urlopen('https://www.littlegolem.net' + SGF_link)
        txt = response.read()
            
        plids, plnames = extract_player_ids(txt)
        player_names.update(plnames)
        players.update(plids)

    return list(players), list(player_names)

    
    
    #     if line[:6] == '[Event' :
    #         # new game, reset flag
    #         take_game = False
    #     elif line[:5] == '[Size':
    #         take_game = True
    #     elif line[:2] == ';b[':
    #         game_strings.append(lines
            
    #         print line



if __name__ == '__main__':

    # get list of top players
    top_plids, top_plnames = get_championship_players()
    print "Top %d Players:" % len(top_plids)
    print top_plnames    


    # extract all games played by top players
    
    with open('data/player_game_list_txt.txt', 'r') as f:
        all_games_txt = f.read()
    lines = all_games_txt.splitlines()
    n_games = (len(lines)-5) / 11

    print '%d games in database' % n_games

    games = [lines[4 + 11*i: 14 + 11*i] for i in range(n_games)]

    top_p0_games = []
    top_p1_games = []
    for game in games:
        if game[1].split('"')[1] != '5':
            # wrong size
            continue
        p0_id = int(game[4].split('"')[1])
        p1_id = int(game[6].split('"')[1])
        if p0_id in top_plids:
            top_p0_games.append(game)
        if p1_id in top_plids:
            top_p1_games.append(game)

    # save to new file
    with open('data/p0_expert_games.txt', 'w') as f:
        for game in top_p0_games:
            f.write('\n'.join(game))
            f.write('\n\n')
    with open('data/p1_expert_games.txt', 'w') as f:
        for game in top_p1_games:
            f.write('\n'.join(game))
            f.write('\n\n')
        

