import numpy as np
import logging
from logger import MyLogger
import os

#Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
#sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class KruisGrid(np.ndarray):
    def __new__(cls, numTables:int, tableSize:int = 4):
        #calculate the dimensions of the new array and make one with numpy
        numPlayers=numTables*tableSize
        numRounds=(numPlayers-1)//(tableSize-1)
        grid=np.zeros((numRounds,numTables,tableSize),dtype=int)

        #FILL matrix with first round
        #fill first round compleet:
        #grid[0]=np.array(np.arange(1,numPlayers+1)).reshape(numTables,4)

        #fill first round, only table 1:
        grid[0][0]=range(1,tableSize+1)
        grid[0][1][0]=tableSize+1

        for y in range(1,numRounds) :
            for x in range(0,numTables) :
                if x<tableSize :
                    grid[y][x][0]=x+1
                    if y-1==x:
                        grid[y][x][1]=tableSize+1
                if y>tableSize and x!=y:
                    grid[y][x][0]=x+1
        return grid.view(cls)

    def __init__(self,*args,**kwargs):
        try:
            self.logger={}
            for name in ["MAIN","POSSIBILITY","SOLVER","COMBO","OUTPUT"] :
                self.logger[name]=MyLogger(name, logging.INFO)
            self.numRounds,self.numTables,self.tableSize=self.shape
            self.numPlayers=self.numTables*self.tableSize
            self.blocks={}
            self.scores={}
            self.count=0
            self.show_function=self.show_default
            numBlocks=self.numPlayers-(1+self.numRounds*3)
            if numBlocks :
                for n in range(1,self.numPlayers+1) :
                    if numBlocks == 1 :
                        blocked_player = (n+self.numPlayers//2-1)%self.numPlayers+1
                        self.blocks[n] = [blocked_player]
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

    def check_combo(self):
        logger=self.logger["COMBO"]
        for n in range(1,self.numPlayers) :
            for m in range(n+1,self.numPlayers+1) :
                if not (n in self.blocks and m in self.blocks[n]):
                    if any(all((n in self[y][x] and not self.possible(y,x,m)) or (m in self[y][x] and not self.possible(y,x,n)) for x in range(self.numTables)) for y in range(self.numRounds)) :
                        logger.debug("Combo {} and {} not possible!".format(n,m))
                        return False
        return True

    def possible(self,y,x,n) :
        logger=self.logger["POSSIBILITY"]
        #check if table isn't full:
        if all(self[y][x]) :
            logger.debug("table full")
            return False
        #check if new player is blocked by player in team
        logger.debug("blocks: {}".format(self.blocks))
        logger.debug("table: {}".format(self[y][x]))
        if n in self.blocks and any((player in self.blocks[n]) for player in self[y][x]):
            logger.debug("player {} blocked by".format(n))
            return False
        #check if player isn't  already playing in this round:
        if any(n in table for table in self[y]) :
            logger.debug('player {} is already playing this round'.format(n))
            return False
        #check if combo exist in self:
        for round in self :
            for table in round :
                if n in table:
                    if any(player and player is not n and player in self[y][x] for player in table) :
                        logger.debug("player {} is already playing against player on table: {}-{}".format(n,y,x))
                        return False
        return True

    def procent(self):
        logger=self.logger["OUTPUT"]
        total=0
        logger.info(self.scores)
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
                self[y][x].sort()
                count=0
                for i in range(self.tableSize) :
                    if self[y][x][i]!=0 :
                        self[y][x][count]=self[y][x][i]
                        count+=1
                while count < self.tableSize:
                    self[y][x][count]=0
                    count+=1

    def show_default(self, count, percentage, grid):
        level=int(np.log10(count)) if count else 0
        maxlevel=1
        if level > maxlevel :
            level=maxlevel
        if not count%(30**level):
            cls()
            print("self.count: {} - level: {}".format(count,level))
            print("{} %".format(percentage))
            self.reorder()
            print(grid)

    def show(self):
        self.show_function(self.count,self.procent(),self)

    def solve(self):
        logger=self.logger["MAIN"]
        self.count+=1
        logger.debug("START SOLVE: {}".format(self.count))
        self.show()
        for n in range(6,self.numPlayers+1) :
            logger.debug("n: {}".format(n))
            if not all(any(n in self[y][x] for x in range(self.numTables)) for y in range(self.numRounds)):
                for y in range(self.numRounds) :
                    logger.debug('round: {}'.format(y))
                    if not any(n in self[y][x] for x in range(self.numTables)) :
                        logger.debug('empty round')
                        #player n is not placed this round:
                        if not (y and (self[y]==self[y-1]).all()):
                            for x in range(self.numTables) :
                                logger.debug('table: {}'.format(x))
                                if not (x and (self[y][x]==self[y][x-1]).all()):
                                    if self.possible(y, x, n) :
                                        if y==0 :
                                            logger.debug('score {} : {}'.format(n,x))
                                            self.scores[n]=x
                                        #add player:
                                        for i,player in enumerate(self[y][x]) :
                                            if not player:
                                                self[y][x][i]=n
                                                break
                                        logger.debug('SOLVE NEXT LEVEL')
                                        if not (self.check_combo() and self.solve()):
                                        #reset
                                            logger.debug("reset")
                                            for i,player in enumerate(self[y][x]) :
                                                if player==n:
                                                    self[y][x][i]=0
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
                if not self.scores[n] :
                    self.scores[n]=self.numTables-1
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

grid=KruisGrid(5)
grid.show()
if grid.solve():
    print('whoot!')
print('end')


"""
if solve() :
    print("whoooot!")
    print(self)
else :
    print("NO SOLUTION!")
"""
