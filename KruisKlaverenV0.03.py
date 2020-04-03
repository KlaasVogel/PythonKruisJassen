import numpy as np
import logging
from logger import MyLogger
import os
import time

#Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
#sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)

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
            self.timers={}
            self.count=0
            self.start_time=0
            self.show_function=self.show_default
            numBlocks=self.numPlayers-(1+self.numRounds*3)
            if numBlocks :
                for n in range(1,self.numPlayers+1) :
                    if numBlocks == 1 :
                        blocked_player = (n+self.numPlayers//2-1)%self.numPlayers+1
                        self.blocks[n] = [blocked_player]
                    else:
                        self.blocks[n]=[(n+3)%self.numPlayers+1,(n+self.numPlayers-5)%self.numPlayers+1] #plus four and minus four
            self.resetScores(self.tableSize+2)
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

    def check_combos(self,m):
        logger=self.logger["COMBO"]
        mask1=np.any(np.isin(self,m),axis=2)
        if np.all(np.any(mask1,axis=1)) :
            logger.debug("{} is playing in every round".format(m))
            for n in range(1,m) :
                if m not in self.blocks or n not in self.blocks[m] :
                    logger.debug("{} is not blocked by {}".format(n,m))
                    mask2=np.any(np.isin(self,n),axis=2)
                    if not np.any(np.logical_and(mask1,mask2)):
                        logger.debug("NO COMBO's FOR {} and {}".format(n,m))
                        return False
        """
        for n in range(1,self.numPlayers) :
            mask1=np.any(np.isin(self,n),axis=2)
            if np.any(mask1) :
                for m in range(n+1,self.numPlayers+1) :
                    mask2=np.any(np.isin(self,m),axis=2)
                    if np.any(mask2) :
                        if not np.any(np.logical_and(mask1,mask2)):
                            logger.debug("NO COMBO's FOR {} and {}".format(n,m))
                            return False
        """
        logger.debug("return True")
        return True

    def possible(self,y,x,n) :
        logger=self.logger["POSSIBILITY"]
        logger.debug("CHECKING {} for table {} in round {}".format(n,x,y))
        #check if table isn't full:
        if all(self[y][x]) :
            logger.debug("table full")
            return False
        #check if new player is blocked by player in team
        #logger.debug("blocks: {}".format(self.blocks))
        #logger.debug("table: {}".format(self[y][x]))
        if n in self.blocks and any((player in self.blocks[n]) for player in self[y][x]):
            logger.debug("player {} blocked".format(n))
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
        logger.debug(self.scores)
        denominator=1/100
        for n in self.scores:
            for round in self.scores[n] :
                if np.any(round) :
                    i=0
                    for x in round :
                        if x==2:
                            nominator=i
                        if x :
                            i+=1
                    denominator=denominator*i
                    total=total+nominator/denominator
        elaps_time=time.time()*1000-self.start_time
        elaps_minute=int(elaps_time//60000)
        estime_minute=int(elaps_time//(600*total) if total else 100000)
        return [total, elaps_minute, estime_minute]

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

    def resetScores(self,trigger):
        if trigger<=self.numPlayers:
            for i in range(trigger,self.numPlayers+1) :
                self.scores[i]=[]
                for j in range(self.numRounds) :
                    self.scores[i].append([])
                    for k in range(self.numTables) :
                        self.scores[i][j].append(0)

    def show_default(self, count, process, grid):
        cls()
        print("self.count: {}".format(count))
        print("{} %".format(process[0]))
        print("Time running: {} minutes --- time remaining: {} minutes".format(process[1],process[2]))
        self.reorder()
        print(grid)
        for n in self.timers:
            print("{} : {}".format(n,print_time(time.time()*1000-self.timers[n])))

    def show(self, force=False):
        level=int(np.log10(self.count)) if self.count else 0
        maxlevel=2
        if level > maxlevel :
            level=maxlevel
        if force or not self.count%(20**level):
            self.show_function(self.count,self.procent(),self)

    def solve(self):
        logger=self.logger["MAIN"]
        if not self.start_time :
            self.start_time=time.time()*1000
        self.count+=1
        logger.debug("START SOLVE: {}".format(self.count))
        self.show()
        for n in range(6,self.numPlayers+1) :
            logger.debug("n: {}".format(n))
            if not all(any(n in self[y][x] for x in range(self.numTables)) for y in range(self.numRounds)):
                for y in range(self.numRounds) :
                    logger.debug('round: {}'.format(y))
                    #check if player n is not placed this round:
                    if not any(n in self[y][x] for x in range(self.numTables)) :
                        logger.debug('empty round')
                        #check if round isn't the same as previous round
                        if not (y and (self[y]==self[y-1]).all()):
                            for x in range(self.numTables) :
                                logger.debug('table: {}'.format(x))
                                #check if table isn't the same as previous table
                                if not (x and (self[y][x]==self[y][x-1]).all()):
                                    logger.debug("table is unique!")
                                    if self.possible(y, x, n) :
                                        self.scores[n][y][x]=2
                                        for i in range(x+1,self.numTables):
                                            self.scores[n][y][i] = 0 if (self[y][i]==self[y][i-1]).all() else 1
                                        #add player:
                                        logger.debug("ADDING {} to table: {} in round {}".format(n,x,y))
                                        for i,player in enumerate(self[y][x]) :
                                            if not player:
                                                self[y][x][i]=n
                                                break
                                        self.timers[n]=time.time()*1000
                                        logger.debug('SOLVE NEXT LEVEL')
                                        if not (self.check_combos(n) and self.solve()):
                                        #reset
                                            logger.debug(" ---- RESET -------")
                                            for i,player in enumerate(self[y][x]) :
                                                if player==n:
                                                    self[y][x][i]=0
                                            self.scores[n][y][x]=1
                                            self.resetScores(n+1)
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
                logger.debug("{} is done!".format(n))
        self.show(True)
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
print(grid.scores)

if grid.solve():
    print('whoot!')
print('end')
