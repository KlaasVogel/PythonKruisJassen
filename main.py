from __future__ import annotations
from dataclasses import dataclass, field, InitVar
import math

DEFAULT_PLAYERS = 16
DEFAULT_POULE_SIZE = 4


@dataclass
class Player:
    nr: int
    blockedPlayers: list[int] = field(default_factory=list)

class Players(list[Player]):
    def __init__(self, num_players):
        [self.append(Player(nr+1)) for nr in range(num_players)]

    def block_pair(self, player1: int, player2: int):
        self[player1-1].blockedPlayers.append(player2)
        self[player2-1].blockedPlayers.append(player1)


@dataclass
class Poule:
    id: tuple[int, int]
    size: InitVar
    candidates: list[int]
    player_nrs: list[int] = field(default_factory=list)

    def __post_init__(self, size: int):
        [self.player_nrs.append(0) for _ in range(size)]

    def check_full(self) -> bool:
        if all(self.player_nrs):
            self.candidates = []
            return True
        return False

    def add_player(self, new_player: int, players: Players):
        """add player to poule
        check if possible
        add player_nr to list of players
        get list of existing players in poule
        couple/block players in Players
        remove new player from candidates
        clean candidates if poule is full
        """
        if self.check_full():
            print("Ohoh Poule is already full")
            return
        if new_player not in self.candidates:
            print(f"ohoh - {new_player} - {self.candidates}")
            raise Exception("Player is not a candidate")
        for idx,playernr in enumerate(self.player_nrs):
            if playernr:
                players.block_pair(playernr, new_player)
                continue
            self.player_nrs[idx] = new_player
            self.update_candidates(players)
            break

    def update_candidates(self, players: Players):
        for playernr in self.player_nrs:
            if not playernr:
                continue
            if playernr in self.candidates:
                self.candidates.remove(playernr)
            for blockedplayer in players[playernr-1].blockedPlayers:
                if blockedplayer in self.candidates:
                    self.candidates.remove(blockedplayer)


class PlayRound(list[Poule]):
    def __init__(self, nr: int, players: Players, poule_size: int):
        num_poules_per_round = int(len(players)/poule_size)
        player_nrs = list([player.nr for player in players])
        [self.append(Poule((nr,x+1), poule_size, player_nrs.copy())) for x in range(num_poules_per_round)]

    def check_full(self):
        return all([poule.check_full() for poule in self])
    
    def get_poule(self) -> Poule:
        min_candidates = 0
        result = None
        for poule in self:
            if poule.check_full():
                continue
            if not min_candidates or min_candidates>len(poule.candidates):
                min_candidates = len(poule.candidates)
                result = poule
        return result

class WrongAmountOfPlayerException(Exception):
    ...

@dataclass
class Schedule(list[PlayRound]):
    num_players: int
    poule_size: int
    players: Players = field(default_factory=list)

    def __post_init__(self):
        if self.num_players % self.poule_size:
            raise WrongAmountOfPlayerException()
        self.players = Players(self.num_players)
        max_rounds = math.floor((self.num_players-1)/(self.poule_size-1))
        [self.append(PlayRound(x+1, self.players, self.poule_size)) for x in range(max_rounds)]
        first_round = self.init_first_row()
        self.init_blocks(first_round)
        self.fix_players_to_tables(first_round)

    def init_first_row(self) -> PlayRound:
        player_nr = 0
        for poule in self[0]:
            while not all(poule.player_nrs):
                player_nr+=1
                poule.add_player(player_nr, self.players)
        return self[0]
    
    def init_blocks(self, first_round: PlayRound):
        block_pairs = (self.num_players-1)%(self.poule_size-1)
        if block_pairs:
            print(f"creating blocks: {block_pairs}")

    def fix_players_to_tables(self, first_round: PlayRound):
        players = first_round[0].player_nrs
        print(players)
        for round in self[1:]:
            for idx, poule in enumerate(round):
                if idx < len(players):
                    poule.add_player(players[idx], self.players)

    def solve(self) -> bool:
        schedule_copy = self.copy()
        players_copy = self.players.copy()
        round = self.get_round()
        if round == None:
            return True
        poule = round.get_poule()
        candidates = poule.candidates.copy()
        
        return False

    def get_round(self) -> PlayRound:
        for round in self:
            if round.check_full():
                print("round full")
                continue
            return round
        return None


def MainSolver(num_players: int = DEFAULT_PLAYERS, poule_size: int = DEFAULT_POULE_SIZE):
    main_schedule = Schedule(num_players, poule_size)
    main_schedule.solve()

    

if __name__ == "__main__":
    MainSolver()
