import numpy as np
from logger import MyLogSet, MyLogger
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
import os
import time
from threading import Thread
import json


class KruisGrid(np.ndarray):
    def __new__(cls, numTables: int, tableSize: int = 4):
        # calculate the dimensions of the new array and make one with numpy
        numPlayers = numTables * tableSize
        numRounds = (numPlayers - 1) // (tableSize - 1)
        grid = np.zeros((numRounds, numTables, tableSize), dtype=int)
        for round in range(0, numRounds):
          grid[round][0][0] = 1
        return grid.view(cls)

    def __init__(self, *args, **kwargs):
      self.logger = MyLogSet(
          "MAIN", "SOLVER", "POSSIBILITY", "COMBO", "OUTPUT", LOG_LEVEL=INFO)
      logger=self.logger["MAIN"]
      self._numRounds, self._numTables, self._tableSize = self.shape
      self._numPlayers = self._numTables * self._tableSize
      self._numBlocks = self._numPlayers - \
          (1 + self._numRounds * (self._tableSize - 1))
      self.running = False
      self.__count = 0
      self.lastcount=0
      self.level=0
      self.solved = False
      self.start_time = 0
      self.lasttime=0
      self.__blocks = {}
      self.states = {}

      # perfect setup all players can play against each other player (once)
      if not self._numBlocks:
        # fill first round:
        self[0] = np.array(np.arange(1, self._numPlayers + 1)
                           ).reshape(self._numTables, self._tableSize)
        # fill first place of all tables with players from round 1, table 1
        for round in range(1, self._numRounds):
          for table in range(1, self._tableSize):
            self[round][table][0] = table + 1
        self.__blocks = {}
        for player in range(1,self._numPlayers + 1):
          self.states[player] = np.zeros((self._numRounds, self._numTables), dtype=int)
      elif self._numBlocks == 1:
        # fill first seat of table 1 and table 2 with 1 and blocked plaer
        blockedPlayer = 1 + self._numPlayers // 2
        for round in range(self._numRounds):
          self[round][0][0] = 1  # player 1 -> #table 1
        for place in range(self._tableSize):
          self[0][0][place]=place+1
        #placing player 2 on tables
        for round in range(1,self._numRounds):
          for table in range(1,self._tableSize):
            if table < self._numTables:
              self[round][table][0]=table+1
            # if table==round:
            #   self[round][table][1]=blockedPlayer
        # if self._tableSize<self._numTables:
        #   self[0][self._tableSize][0]=blockedPlayer
        #   for round in range(self._tableSize,self._numRounds):
        #     self[round][self._tableSize][0]=blockedPlayer

        # if self._numTables>2 :
        #   for round in range(2,self._numRounds):
        #     self[round][2][0]=2
        for player in range(1, blockedPlayer):
          opponent = player + self._numPlayers // 2
          self.__blocks[player] = [opponent]
          self.__blocks[opponent] = [player]
          self.states[player] = np.zeros((self._numRounds, self._numTables), dtype=int)
          self.states[opponent] = np.zeros((self._numRounds, self._numTables), dtype=int)

    def solve(self,lastPlayer=0):
      logger = self.logger["SOLVER"]
      try:
        self.__count += 1
        logger.debug(f" Round {self.__count}")
        if not self.start_time:
            self.start_time = time.time() * 1000
        check=False
        for player in self.states:
          if not lastPlayer or lastPlayer==player:
            check=True
          if check:
            logger.debug(f"- - - ->\n\n")
            logger.debug(f"*** player: {player} *** round: {self.__count} *** LEVEL: {self.level} ***")
            player_mask1 = np.any(np.isin(self, player), axis=2)
            player_mask2 = np.any(player_mask1, axis=1)
            logger.debug(f"mask {player}:\n {player_mask1} - {player_mask2}")
            if not np.all(player_mask2):
                round = np.where(player_mask2 == False)[0][0]
                logger.debug(f"checking round: {round}")
                # check if round isn't the same as previous round
                if not (round and (self[round] == self[round - 1]).all()):
                    # logger.debug("{}".format((self[y]==self[y-1]).all()))
                    for table in range(self._numTables):
                        logger.debug(f'table: {table}')
                        if not (table and (self[round][table] == self[round][table - 1]).all()):
                            logger.debug("table is unique!")
                            if self.possible(round, table, player):
                              lastTable=self.checkTable(round,table, player)
                              self.add_to_grid(round, table, player)
                              self.level+=1
                              logger.debug('SOLVE NEXT LEVEL')
                              if not (self.check_combos(player) and self.solve(player)):
                                  # reset
                                  logger.debug(" ---- RESET -------")
                                  self.remove_from_grid(round, table, player)
                                  self.level-=1
                                  self.resetStates(player)
                                  if lastTable and not self.level:
                                      #self.show(True)
                                      logger.debug('----End of Line -----')
                                      self.stop()
                              else:
                                  return True
                        else:
                            logger.debug(f"SKIPPING table {table} for {player}")
                    else:
                      logger.debug(
                          f"End of Tables: player:{player} - round:{round} - table:{table}")
                else:
                  logger.debug("SKIPPING round {} for {}".format(y, n))
                logger.debug('return False 1')
                return False
            else:
                logger.debug(f"{player} is done!")
          else:
            logger.debug(f"Skipping player {player}")
        # self.save_data()
        logger.debug('RETURN FINAL TRUE')
        self.solved=True
        self.stop()
        return True
      except Exception as e:
        logger.exception(e)
        self.stop()

    def checkTable(self, round, table, player):
      state=True
      for i in range(table + 1, self._numTables):
          if (self[round][i] == self[round][i - 1]).all():
            self.states[player][round][i] = 0
            state=False
          else:
            self.states[player][round][i] = 1
      return state

    def resetStates(self,currentPlayer):
      reset=False
      for player in self.states:
        if player==currentPlayer:
          reset=True
        elif reset:
          self.states[player]=np.zeros((self._numRounds, self._numTables), dtype=int)

    def possible(self,round,table,player) :
        logger=self.logger["POSSIBILITY"]
        logger.debug(f"CHECKING {player} for table {table} in round {round}")
        # check if table isn't full:
        if all(self[round][table]) :
            logger.debug("table full")
            return False
        # check if new player is blocked by player in team
        # logger.debug("blocks: {}".format(self.blocks))
        # logger.debug("table: {}".format(self[y][x]))
        for opponent in self[round][table]:
            if opponent:
                if (opponent in self.__blocks and player in self.__blocks[opponent]):
                    logger.debug(f"player {player} blocked by {opponent}")
                    return False
                elif np.any(np.logical_and(np.any(np.isin(self,opponent),axis=2),np.any(np.isin(self,player),axis=2))) :
                    logger.debug(f"player {player} is already playing against {opponent} on table: {table} in round {round}")
                    return False
        logger.debug("TABLE is possible")
        return True

    def progress(self):
        logger=self.logger["OUTPUT"]
        total=0
        # logger.debug(self.states)
        denominator=1/100
        nominator=0
        for n in self.states:
            for round in self.states[n] :
                if np.any(round) :
                    i=0
                    for x in round :
                        if x==2:
                            nominator=i
                        if x :
                            i+=1
                    denominator=denominator*i
                    total=total+nominator/denominator
        now=time.time()*1000
        elaps_time=now-self.lasttime
        self.lasttime=now
        totaltime=now-self.start_time
        delta_count=self.__count-self.lastcount
        self.lastcount=self.__count
        speed=delta_count*1000/elaps_time if elaps_time else 0
        estimate_time=int(1000*(100-total)*self.__count//(speed*total)) if (speed and total) else 1000000
        estimate_totaltime=(100*totaltime)//total if total else 1000000
        return "".join([f"{self.__count}: ", "{:.5f}%".format(total),print_time(estimate_time),
                f"\nTime running: {print_time(totaltime)} - est. Total Time: {print_time(estimate_totaltime)}\nest. Time Remaining: {print_time(estimate_totaltime-totaltime)}"])

    def add_to_grid(self,round,table,player):
        logger=self.logger["MAIN"]
        logger.debug(f"ADDING {player} to table: {table} in round {round}")
        if player not in self[round][table]:
            for idx,number in enumerate(self[round][table]) :
                if not number:
                    self[round][table][idx]=player
                    self.states[player][round][table]=2
                    logger.debug("Player added")
                    break
            else:
              logger.warning(f"No place for player {player} on table {table} in round {round}")
        else:
          logger.warning(f"Player is already playing on table {table} in round {round}")

    def check_combos(self,player):
        logger=self.logger["COMBO"]
        mask1=np.any(np.isin(self,player),axis=2)
        if np.all(np.any(mask1,axis=1)) :
            logger.debug("player {player} is playing in every round")
            for opponent in self.states:
                if opponent is player:
                  logger.debug("All opponents checked")
                  break
                else:
                   if (player not in self.__blocks or opponent not in self.__blocks[player]):
                    logger.debug(f"{player} is not blocked by {opponent}")
                    mask2=np.any(np.isin(self,opponent),axis=2)
                    if not np.any(np.logical_and(mask1,mask2)):
                        logger.debug(f"NO COMBO's FOR {player} and {opponent}")
                        return False
        logger.debug("NO ERROR")
        return True

    def remove_from_grid(self,round,table,player):
        logger=self.logger["MAIN"]
        logger.debug(f"Removing {player} from table {table} in round {round}")
        for idx,number in enumerate(self[round][table]) :
            if player==number:
                self[round][table][idx]=0
                self.states[player][round][table]=1
                break
        else:
          logger.warning(f"player {player} not present on table {table} in round {round}")

    def start(self):
        self.running=True
        Thread(target=self.solve,daemon=True).start()

    def stop(self):
      self.running=False

    def reorder(self):
        for table in range(self._numTables) :
            for round in range(self._numRounds) :
                self[round][table].sort()

    def show(self, force=False):
        cls()
        # self.reorder()
        print(np.rollaxis(grid,1))
        print(self.progress())
        # print(self.states)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_time(time):
    seconds=int((time//1000)%60)
    minutes=int(((time//1000)//60)%60)
    hours=int((((time//1000)//60)//60)%24)
    days=int((((time//1000)//60)//60)//24)
    string=""
    if days:
        string+="{} days".format(days)
    if hours:
        string+=" {} hours".format(hours)
    if minutes :
        string+=" {} minutes".format(minutes)
    if seconds:
        string+=" {} seconds".format(seconds)
    return string

if __name__ == "__main__":
    grid=KruisGrid(4,3)
    grid.show()
    grid.start()
    while (grid.running and not grid.solved):
        time.sleep(2)
        grid.show(True)
    grid.stop()
    grid.show(True)
