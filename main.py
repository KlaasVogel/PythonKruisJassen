from __future__ import annotations
from dataclasses import dataclass, field
import math

DEFAULT_PLAYERS = 16
DEFAULT_POULE_SIZE = 4


@dataclass
class Player:
    nr: int
    blockedPlayers: list[Player] = field(default_factory=list)

class Players(list[Player]):
    def __init__(self, num_players):
        [self.append(Player(nr+1)) for nr in range(num_players)]

@dataclass
class Poule:
    size: int
    candidates: list[int]
    players: list[int] = field(default_factory=list)

    def __post_init__(self):
        [self.players.append(0) for _ in range(self.size)]


class PlayRound(list[Poule]):
    def __init__(self, players: Players, poule_size: int):
        num_poules_per_round = int(len(players)/poule_size)
        player_nrs = list([player.nr for player in players])
        [self.append(Poule(poule_size, player_nrs)) for _ in range(num_poules_per_round)]


def add_player_to_poule(new_player: int, poule: Poule, players: Players):
    """add player to poule
    check if possible
    add player_nr to list of players
    get list of existing players in poule
    couple/block players in Players
    remove new player from candidates
    clean candidates if poule is full
    """
    if all(poule.players):
        raise Exception("Poule is already full")
    if new_player not in poule.candidates:
        raise Exception("Player is not a candidate")
    for idx,playernr in enumerate(poule.players):
        if playernr:
            players[playernr-1].blockedPlayers.append(new_player)
            players[new_player-1].blockedPlayers.append(playernr)
            continue
        poule.players[idx] = new_player
        poule.candidates.remove(new_player)
        break
    if all(poule.players):
        poule.candidates = []


class WrongAmountOfPlayerException(Exception):
    ...

class Schedule(list[PlayRound]):
    def __init__(self, players: Players, poule_size: int):
        if len(players) % poule_size:
            raise WrongAmountOfPlayerException()
        max_rounds = math.floor((len(players)-1)/(poule_size-1))
        [self.append(PlayRound(players, poule_size)) for _ in range(max_rounds)]
        print(self)

    def fill_first_row(self, players: Players):
        player_nr = 0
        for poule in self[0]:
            while not all(poule.players):
                player_nr+=1
                add_player_to_poule(player_nr, poule, players)
        print(self)


def MainSolver(num_players: int = DEFAULT_PLAYERS, poule_size: int = DEFAULT_POULE_SIZE):
    main_players = Players(num_players)
    main_schedule = Schedule(main_players, poule_size)
    main_schedule.fill_first_row(main_players)


if __name__ == "__main__":
    MainSolver()
