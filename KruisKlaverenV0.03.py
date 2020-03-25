import tkinter as tk
import numpy as np
import logging
from logger import MyLogger
import os

#Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
#sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)

logger=MyLogger("LOG", logging.INFO)

class KruisGrid(np.ndarray):
    def __new__(cls, numTables:int, tableSize:int = 4):
        numPlayers=numTables*4
        numRounds=(numPlayers-1)//3
        grid=np.zeros((numRounds,numTables,tableSize),dtype=int)
        #fill first round compleet:
        #grid[0]=np.array(np.arange(1,numPlayers+1)).reshape(numTables,4)

        #fill first round, only table 1:
        grid[0][0]=range(1,tableSize+1)
        grid[0][1][0]=tableSize+1

        #get blocked
        numBlocks=numPlayers-(1+numRounds*3)
        blocked=(1+numPlayers//2-1)%numPlayers+1 if numBlocks==1 else 0
        #grid[0][2][0]=blocked

        for y in range(1,numRounds) :
            for x in range(0,numTables) :
                if x<tableSize :
                    grid[y][x][0]=x+1
                    if y-1==x:
                        grid[y][x][1]=tableSize+1
                if y>tableSize and x!=y:
                    grid[y][x][0]=x+1
        return grid.view(cls)


        #obj = np.asarray(input_array).view(cls)
        #return obj



    def __init__(self,*args,**kwargs):
        try:
            self.numRounds,self.numTables,self.tableSize=self.shape
            self.numPlayers=numTables*self.tableSize
            self.blocks={}
            self.scores={}
            numBlocks=self.numPlayers-(1+self.numRounds*3)
            if numBlocks :
                for n in range(1,self.numPlayers+1) :
                    if numBlocks == 1 :
                        blocked_player = (n+self.numPlayers//2-1)%self.numPlayers+1
                        self.blocks[n] = [blocked_player]
                        """
                        if n <= self.tableSize :
                            self.scores[blocked_player]=0
                        elif n < (1+self.numPlayers//2) :
                            self.scores[n]=0
                            self.scores[blocked_player]=0
                        """
                    else:
                        self.blocks[n]=[(n+3)%self.numPlayers+1,(n+self.numPlayers-5)%self.numPlayers+1] #plus four and minus four
            if not len(self.scores) :
                for i in range(6,self.numPlayers+1):
                    self.scores[i]=0
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

    def process(self):
        total=0
        for i,(n,score) in enumerate(self.scores.items()):
            if i==1:
                score-=1
            if i:
                denominator = (self.numTables)**(i)
                total+=100*score/denominator
        return total


    def reorder(self):
        for y in range(self.numRounds) :
            for x in range(self.numTables) :
                grid[y][x].sort()
                count=0
                for i in range(self.tableSize) :
                    if grid[y][x][i]!=0 :
                        grid[y][x][count]=grid[y][x][i]
                        count+=1
                while count < self.tableSize:
                    grid[y][x][count]=0
                    count+=1

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#create a new grid
#input number of tables
def createGrid(numTables:int) :
    numPlayers=numTables*4
    numRounds=(numPlayers-1)//3
    grid=np.zeros((numRounds,numTables,4),dtype=int)
    #fill first round compleet:
    #grid[0]=np.array(np.arange(1,numPlayers+1)).reshape(numTables,4)

    #fill first round, only table 1:
    grid[0][0]=range(1,5)
    grid[0][1][0]=5

    #get blocked
    numBlocks=numPlayers-(1+numRounds*3)
    blocked=(1+numPlayers//2-1)%numPlayers+1 if numBlocks==1 else 0
    #grid[0][2][0]=blocked

    for y in range(1,numRounds) :
        for x in range(0,numTables) :
            if x<4 :
                grid[y][x][0]=x+1
                if y-1==x:
                    grid[y][x][1]=5
            if y>4 and x!=y:
                grid[y][x][0]=x+1
    return Grid(grid)

#need to check if all combos are present / available
com_logger=MyLogger("Combo Check", logging.INFO)
def check_combo() :
    global grid, combo_logger
    for n in range(1,grid.numPlayers) :
        for m in range(n+1,grid.numPlayers+1) :
            if not (n in grid.blocks and m in grid.blocks[n]):
                if not any((n in grid[y][x] or possible(y,x,n)) and (m in grid[y][x] or possible(y,x,m)) for y in range(grid.numRounds) for x in range(grid.numTables)):
                    com_logger.debug("Combo {} and {} not possible!".format(n,m))
                    return False
    #com_logger.debug("All combo's are possible")
    return True

#check if player can be placed.
pos_logger=MyLogger("Possibility Check", logging.INFO)
def possible(y,x,n) :
    global grid,pos_logger

    #check if table isn't full:
    if all(grid[y][x]) :
        pos_logger.debug("table full")
        return False
    #check if new player is blocked by player in team
    pos_logger.debug("blocks: {}".format(grid.blocks))
    pos_logger.debug("table: {}".format(grid[y][x]))
    if n in grid.blocks and any((player in grid.blocks[n]) for player in grid[y][x]):
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
    maxlevel=1
    count+=1
    if count == 1:
        logger = MyLogger("SOLVE", logging.INFO)
    logger.debug("START SOLVE: {}".format(count))
    level=int(np.log10(count))
    if level > maxlevel :
        level=maxlevel
    if not count%(10**level):
        cls()
        print("count: {} - level: {}".format(count,level))
        print(grid.scores)
        print("{} %".format(grid.process()))
        grid.reorder()
        print(grid)
    numRounds,numTables,tableSize=grid.shape
    numPlayers=numTables*tableSize
    for n in range(6,grid.numPlayers+1) :
        logger.debug("n: {}".format(n))
        if not all(any(n in grid[y][x] for x in range(numTables)) for y in range(numRounds)):
            for y in range(numRounds) :
                logger.debug('round: {}'.format(y))
                if not any(n in grid[y][x] for x in range(numTables)) :
                    logger.debug('empty round')
                    #player n is not placed this round:
                    if not (y and (grid[y]==grid[y-1]).all()):
                        for x in range(numTables) :
                            logger.debug('table: {}'.format(x))
                            if not (x and (grid[y][x]==grid[y][x-1]).all()):
                                if possible(y, x, n) :
                                    if y==0 :
                                        logger.debug('score {} : {}'.format(n,x))
                                        grid.scores[n]=x
                                    #add player:
                                    for i,player in enumerate(grid[y][x]) :
                                        if not player:
                                            grid[y][x][i]=n
                                            break
                                    logger.debug('SOLVE NEXT LEVEL')
                                    if not (check_combo() and solve()):
                                    #reset
                                        logger.debug("reset")
                                        for i,player in enumerate(grid[y][x]) :
                                            if player==n:
                                                grid[y][x][i]=0
                                    else:
                                        logger.debug('return True 1')
                                        return True
                            else:
                                logger.info("SKIPPING table {} for {}".format(x,n))
                    else:
                        logger.info("SKIPPING round {} for {}".format(y,n))
                    logger.debug('return False 1')
                    return False
        else:
            if not grid.scores[n] :
                grid.scores[n]=grid.numTables-1
            logger.debug("{} is done!".format(n))
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
grid=KruisGrid(numTables)

print(grid.scores)
print("{} %".format(grid.process()))
print(grid)

count=0

if solve() :
    print("whoooot!")
    print(grid)
else :
    print("NO SOLUTION!")
