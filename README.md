# Neural Dots - A neural network that plays dots and boxes

This repository contains all the scripts that were used to create the dots-and-boxes web app [available here](http://dots-and-boxes.eu-central-1.elasticbeanstalk.com/).

If this is no longer online by the time you are reading this, you can run the app locally by running
```
export FLASK_APP=application.py
flask run
```
and then pointing your web browser at 127.0.0.1:5000


# How it works

A convolutional neural net was trained to predict the moves played by experts in 5x5 dots-and-boxes games played on [www.littlegolem.net](www.littlegolem.net), where 'expert' is defined as 'anyone who ever played in the first league of the championship'. There are roughly 800,000 positions in the database.

Unlike chess or Go, the moves (i.e. the lines between dots) are not arranged in a normal grid, but in a diagonal grid. Since a convolutional neural net needs a rectangular grid of inputs, the diagonal move grids were transformed by first rotating 45 degrees and then padding the corners with zeros. Possibly there is a better way that requires less zero-padding, but this works well enough, at least for 5x5 games.

The result is a neural net that takes a position as input and then outputs a probability distribution over all legal moves. During the first 25 moves of a game, the bot simply draws a move from this distribution. After move 25, it uses a short phase of Monte Carlo Tree Search. The exact MCTS algorithm is the same one that was used for AlphaGo, described on page 7 of [the Nature paper](https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf).


# I keep losing. How do I beat this thing?

It is pretty easy to beat if you know some basic dots and boxes strategy, like the [double-cross and the chain rule](http://gcrhoads.byethost4.com/DotsBoxes/dots_strategy.html?i=1).
