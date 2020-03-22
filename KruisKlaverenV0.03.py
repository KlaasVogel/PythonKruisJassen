import tkinter as tk
import numpy as np
import sys
import logging
from logger import MyLogger
from math import ceil
import os

#Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
#sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)

logger=MyLogger("LOG", logging.DEBUG)

class Grid(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __init__(self,*args,**kwargs):
        try:
            self.numRounds,self.numTables,self.tableSize=self.shape
            self.numPlayers=numTables*self.tableSize
            self.blocks={}
            numBlocks=self.numPlayers-(1+self.numRounds*3)
            if numBlocks :
                for n in range(1,self.numPlayers+1) :
                    if numBlocks == 1 :
                        self.blocks[n]=[(n+self.numPlayers//2-1)%self.numPlayers+1]
                    else:
                        self.blocks[n]=[(n+3)%self.numPlayers+1,(n+self.numPlayers-5)%self.numPlayers+1] #plus four and minus four
        except Exception as e:
            print('ERROR bij het maken van Grid')
            print(e)
            self.numRounds=0
            self.numTables=0
            self.tableSize=0
            self.numPlayers=0
        finally:
            print('rounds: {}'.format(self.numRounds))
            print('tables: {}'.format(self.numTables))
            print('tablesize: {}'.format(self.tableSize))
            print('players: {}'.format(self.numPlayers))

    def __array_finalize__(self, obj):
        if obj is None: return
        self.info = getattr(obj, 'info', None)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#create a new grid
#input number of tables
def createGrid(numTables:int) :
    numPlayers=numTables*4
    numRounds=(numPlayers-1)//3
    grid=np.zeros((numRounds,numTables,4),dtype=int)
    #fill first round
    grid[0]=np.array(np.arange(1,numPlayers+1)).reshape(numTables,4)
    #get blocked
    numBlocks=numPlayers-(1+numRounds*3)
    blocked=(1+numPlayers//2-1)%numPlayers+1 if numBlocks==1 else 0

    for y in range(1,numRounds) :
        for x in range(numTables) :
            if x<4 :
                grid[y][x][0]=x+1
    return Grid(grid)

#need to check if all combos are present / available
combo_logger=MyLogger("Possibility Check", logging.DEBUG)
def check_combo() :
    global grid, combo_logger


#check if player can be placed.
pos_logger=MyLogger("Possibility Check", logging.INFO)
def possible(y,x,n) :
    global grid,pos_logger

    #check if table isn't full:
    if all(grid[y][x]) :
        pos_logger.debug("table full")
        return False
    #check if new player is blocked by player in team
    if any(player in grid.blocks[n] for player in grid[y][x]):
        pos_logger.debug("player {} blocked by".format(n))
        return False
    #check if player isn't  already playing in this round:
    if any(n in table for table in grid[y]) :
        pos_logger.debug('player {} is already playing this round'.format(n))
        return False
    #check if combo exist in grid:
    for round in grid :
        for table in round :
            if n in table:
                if any(player and player is not n and player in grid[y][x] for player in table) :
                    pos_logger.debug("player {} is already playing against player on table: {}-{}".format(n,y,x))
                    return False
    return True

def solve():
    global grid, count, logger
    count+=1
    if count == 1:
        logger = MyLogger("SOLVE", logging.INFO)
    logger.debug("START SOLVE: {}".format(count))
    level=int(np.log10(count))
    if level > 3 :
        level=3
    if not count%(10**level):
        cls()
        print("count: {} - level: {}".format(count,level))
        print(grid)
    numRounds,numTables,tableSize=grid.shape
    numPlayers=numTables*tableSize
    for n in range(1,numPlayers+1) :
        logger.debug("n: {}".format(n))
        for y in range(1,numRounds) :
            logger.debug('round: {}'.format(y))
            if not any(n in grid[y][x] for x in range(numTables)) :
                logger.debug('empty round')
                #player n is not placed this round:
                for x in range(numTables) :
                    logger.debug('table: {}'.format(x))
                    if possible(y, x, n) :
                        #add player:
                        for i,player in enumerate(grid[y][x]) :
                            if not player:
                                grid[y][x][i]=n
                                break
                        logger.debug('SOLVE NEXT LEVEL')
                        if not solve() :
                        #reset
                            logger.debug("reset")
                            for i,player in enumerate(grid[y][x]) :
                                if player==n:
                                    grid[y][x][i]=0
                        else:
                            logger.debug('return True 1')
                            return True
                logger.debug('return False 1')
                return False
    logger.debug('RETURN FINAL TRUE')
    return True


#function to create nice gradient of colors for players
def colorPicker(min,max,value):
  values=[154,100,255]
  schema=[[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]]
  kleuren=["#","#"]
  kwintiel=ceil(5*value/(max-min+1))
  tussenwaarde=5*(value)/(max-min+1)-kwintiel+1
  for x in range(2):
    for i in range(3):
      startKleur = values[2] if (schema[kwintiel-1][i]) else values[x]
      eindKleur = values[2] if (schema[kwintiel][i]) else values[x]
      kleuren[x]+=hex(int(startKleur+tussenwaarde*(eindKleur-startKleur)))[2:]
  return kleuren


numTables=5
grid=createGrid(numTables)
print('test - numblocks {}'.format(grid.blocks))
print(grid)
count=0


if solve() :
    print("whoooot!")
    print(grid)
else :
    print("NO SOLUTION!")
