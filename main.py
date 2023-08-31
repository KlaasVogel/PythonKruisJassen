from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import Callable
import logging
import math
import os

DEFAULT_PLAYERS = 20
DEFAULT_POULE_SIZE = 4

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
log = logging.getLogger()
log.info("Hello World")

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
            log.debug("Ohoh Poule is already full")
            return
        if new_player not in self.candidates:
            log.debug(f"ohoh - {new_player} - {self.candidates}")
            raise Exception("Player is not a candidate")
        for idx,playernr in enumerate(self.player_nrs):
            if playernr:
                if playernr != new_player:
                    players.block_pair(playernr, new_player)
                continue
            self.player_nrs[idx] = new_player
            self.candidates.remove(new_player)
            self.update_blocks(players[new_player-1])
            break

    def update_blocks(self, player: Player):
        #remove blocked players if player is in poule
        if player.nr in self.player_nrs:
            for blocked_player in player.blockedPlayers:
                if blocked_player in self.candidates:
                    self.candidates.remove(blocked_player)
        #remove player from candidates if any of blocked player in poule
        if player.nr in self.candidates and any([i for i in player.blockedPlayers if i in self.player_nrs]):
            self.candidates.remove(player.nr)


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
    
    def update_candidate(self, player_nr: int):
        [poule.candidates.remove(player_nr) for poule in self if player_nr in poule.candidates]

class WrongAmountOfPlayerException(Exception):
    ...

@dataclass
class Schedule:
    num_players: int
    poule_size: int
    output: Callable = None
    players: Players = field(default_factory=list)
    rounds: list[PlayRound] = field(default_factory=list)

    def __post_init__(self):
        if self.output == None:
            self.output = self.print_schedule
        if self.num_players % self.poule_size:
            raise WrongAmountOfPlayerException()
        self.players = Players(self.num_players)
        max_rounds = math.floor((self.num_players-1)/(self.poule_size-1))
        [self.rounds.append(PlayRound(x+1, self.players, self.poule_size)) for x in range(max_rounds)]
        first_round = self.init_first_row()
        self.init_blocks(first_round)
        self.fix_players_to_tables(first_round)
    
    @staticmethod
    def print_schedule(schedule: Schedule):
        def print_player(player: int, playerwidth) -> str:
            if not player:
                return "".ljust(playerwidth)
            return str(player).rjust(playerwidth)
        def print_poule(poule: Poule, playerwidth) -> str:
            playernrs = [print_player(nr, playerwidth) for nr in poule.player_nrs]
            return ", ".join(playernrs)

        maxplayerwidth = len(str(schedule.num_players))
        maxpoulewidth = maxplayerwidth*schedule.poule_size + 2*(schedule.poule_size-1)
        os.system('cls')
        for round in schedule.rounds:
            poulenames = [f"poule {poule.id}".ljust(maxpoulewidth) for poule in round]
            print("  ".join(poulenames))
            pouleplayers = [print_poule(poule, maxplayerwidth) for poule in round]
            print("  ".join(pouleplayers))

    def init_first_row(self) -> PlayRound:
        player_nr = 0
        for poule in self.rounds[0]:
            while not all(poule.player_nrs):
                player_nr+=1
                poule.add_player(player_nr, self.players)
        return self.rounds[0]
    
    def init_blocks(self, first_round: PlayRound):
        block_pairs = (self.num_players-1)%(self.poule_size-1)
        if block_pairs == 1:
            log.debug(f"creating blocks: {block_pairs}")
            if self.poule_size%2:
                log.warning("odd number of players in round. not implemented yet")
                return
            poule_halve = int(self.poule_size/2)
            for idp, poule in enumerate(first_round):
                for idx in range(poule_halve):
                    player1 = poule.player_nrs[idx]
                    poule2 = first_round[idp-idx-1]
                    player2 = poule2.player_nrs[-1-idx]
                    log.info(f"{player1} -> {player2}")
                    self.players.block_pair(player1, player2)

                # for player_nr in poule.player_nrs[:poule_halve]:
                    

    def fix_players_to_tables(self, first_round: PlayRound):
        players = first_round[0].player_nrs
        log.debug(players)
        for round in self.rounds[1:]:
            for idx, poule in enumerate(round):
                if idx < len(players):
                    poule.add_player(players[idx], self.players)

    @staticmethod
    def clear_candidates(candidates: list[int], candidate: int) -> list[int]:
        if candidate not in candidates:
            return []
        index = candidates.index(candidate)
        log.debug(f"index {candidate}: {index} - {candidates}")
        return candidates
    

    def solve(self) -> bool:
        self.output(self)
        schedule_copy = self.rounds.copy()
        players_copy = self.players.copy()
        round = self.get_round()
        if round == None:
            return True
        poule = round.get_poule()
        candidates = poule.candidates.copy()
        next_candidate = candidates[0]
        poule.add_player(next_candidate, self.players)
        round.update_candidate(next_candidate)
        self.update(next_candidate)
        if not self.solve():
            ...
        return False
    
    def update(self, candidate: int):
        player = self.players[candidate-1]
        for round in self.rounds:
            for poule in round:
                poule.update_blocks(player)
        log.debug(f"update: {self}")


    def get_round(self) -> PlayRound:
        for round in self.rounds:
            if round.check_full():
                log.debug("round full")
                continue
            return round
        return None


def MainSolver(num_players: int = DEFAULT_PLAYERS, poule_size: int = DEFAULT_POULE_SIZE):
    main_schedule = Schedule(num_players, poule_size)
    main_schedule.solve()

    

if __name__ == "__main__":
    MainSolver()
