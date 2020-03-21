import tkinter as tk
import numpy as np
import sys
import logging
from logger import MyLogger
from math import ceil

#Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
#sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)


#create a new grid
#input number of tables
def createGrid(numTables:int) :
    global grid
    numPlayers=numTables*4
    numRounds=(numPlayers-1)//3
    if (numPlayers-1)%3 :
        numRounds-=2
    grid=np.zeros((numRounds,numTables,4),dtype=int)
    print("players: {} , rounds: {}".format(numPlayers,numRounds))


def possible(y,x,n) :
    global grid
    numRounds,numTables,dummy=grid.shape
    numPlayers=numTables*4
    #check if table isn't full:
    if all(grid[y][x]) :
        return False
    #check if new player has highest number
    if any(player>n for player in grid[y][x]):
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
    global grid
    numRounds,numTables,dummy=grid.shape
    numPlayers=numTables*4
    for y in range(numRounds):
        for x in range(numTables):
            if not all(grid[y][x]):
                for n in range(1,numPlayers+1) :
                    if possible(y, x, n) :
                        #add player:
                        for i,player in enumerate(grid[y][x]) :
                            if not player:
                                grid[y][x][i]=n
                                break
                        solve()
                        #reset
                        for i,player in enumerate(grid[y][x]) :
                            if player==n:
                                grid[y][x][i]=0
                return
            if y==2:
                print(grid)
    print(grid)
    input("more?")


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
solve()




"""
class MainApp(tk.Tk):
  def __init__(self):
    self.root = tk.Tk.__init__(self)
    #self.keuzes=KeuzeFrame(self, side=tk.TOP)





if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
"""
