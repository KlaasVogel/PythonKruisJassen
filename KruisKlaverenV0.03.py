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

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#create a new grid
#input number of tables
def createGrid(numTables:int) :
    global grid
    numPlayers=numTables*4
    numRounds=(numPlayers-1)//3
    grid=np.zeros((numRounds,numTables,4),dtype=int)
    #fill first round
    grid[0]=np.array(np.arange(1,numPlayers+1)).reshape(numTables,4)
    #get blocked
    numBlocks=numPlayers-(1+numRounds*3)
    blocked=(1+numPlayers//2-1)%numPlayers+1 if numBlocks==1 else 0
    """
    for i in range(1,5):
        if i < numRounds :
            for y in range(1,numRounds):
                grid[y][i-1][0]=i
    """
    for y in range(1,numRounds) :
        for x in range(numTables) :
            if x<4 :
                grid[y][x][0]=x+1
                if blocked and y==x:
                    grid[y][x][2]=blocked
            elif y>=4 :
                grid[y][x][2]=blocked


def possible(y,x,n) :
    global grid
    numRounds,numTables,tableSize=grid.shape
    numPlayers=numTables*tableSize

    blocked=[]
    numBlocks=numPlayers-(1+numRounds*3)
    if numBlocks :
        if numBlocks == 1 :
            blocked=[(n+numPlayers//2-1)%numPlayers+1]
        else:
            blocked.append((n+3)%numPlayers+1) #plus four
            blocked.append((n+numPlayers-5)%numPlayers+1) #minus four
    #check if table isn't full:
    if all(grid[y][x]) :
        return False
    #check if new player has highest number or blocked player in team
    if any(player in blocked for player in grid[y][x]):
        return False
    #check if player isn't  already playing in this round:
    if any(n in table for table in grid[y]) :
        return False
    #check if combo exist in gird:
    for round in grid :
        for table in round :
            if n in table:
                if any(player in grid[y][x] for player in table) :
                    return False
    return True

def solve():
    global grid, count
    numRounds,numTables,tableSize=grid.shape
    numPlayers=numTables*tableSize
    for y in range(1,numRounds) :
        for n in range(1,numPlayers+1) :
            if not any(n in grid[y][x] for x in range(numTables)) :
                #player n is not placed this round:
                for x in range(numTables) :
                    if possible(y, x, n) :
                        #add player:
                        for i,player in enumerate(grid[y][x]) :
                            if not player:
                                grid[y][x][i]=n
                                count+=1
                                if not count%2000 or (y+3 > numRounds and not n%(numPlayers-1)) or n==numPlayers:
                                    cls()
                                    print(grid)
                                break
                        if not solve():
                            #reset
                            for i,player in enumerate(grid[y][x]) :
                                if player==n:
                                    grid[y][x][i]=0
                        else:
                            return True
                return False
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
createGrid(numTables)
count=0
solve()
print("whoooot!")
print(grid)




"""
class MainApp(tk.Tk):
  def __init__(self):
    self.root = tk.Tk.__init__(self)
    #self.keuzes=KeuzeFrame(self, side=tk.TOP)





if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
"""
