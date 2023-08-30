# PythonKruisJassen
Generator for creating groups of 4 people where no one plays another player more than once

First attempts were to slow (one attempt to find a solution took more than 3 days for 5 poules) and no solutions could be found for 5 poules per round. Old code still available in the folder V0.1
trying to switch to a new way of solving this problem:
- waveform collapse with backtracing

# V0.2.0.2:
done: light refractoring
start of recursive solving in schedule.
- TODO:
    save/copy state,
    get list of candidates for poule
    try every candidate, collapse schedule and try next solve
    load previous state
    no candidates -> return False

# V0.2.0.1:
total restart of building up code:
(new) features:
- list of players
each player tracks already coupled/blocked players

- poule
list of player(nrs) who will play against eachother
list of candidates, player(nrs) who can still participate in this poule (not blocked by players already in this poule)

- playround
list of poules

- schedule
list of playrounds
added function to fill first round

- main functions
add new player to a poule


    



