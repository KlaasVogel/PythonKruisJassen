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
def createGrid(numTables:int):
    global grid
    numPlayers=numTables*4
    numRounds=(numPlayers-1)//3
    if (numPlayers-1)%3 :
        numRounds-=1
    grid=np.zeros((numRounds,numPlayers),dtype=int)
    print("players: {} , rounds: {}".format(numPlayers,numRounds))


def possible(y,x,n):
    global grid
    numRounds,numPlayers=grid.shape
    for i in range(numPlayers):
        if grid[y][i] == n :
            return False
    x0=(x//4)*4
    table=grid[y,x0:x0+4]
    for i in range(numRounds):
        for j in range(numPlayers//4):
            test=grid[i,j*4:(j*4)+4]
            if n in test:
                if any((player and player in table for player in test)):
                    return False
    return True


def solve():
    global grid
    numRounds,numPlayers=grid.shape
    for y in range(numRounds):
        for x in range(numPlayers):
            if grid[y][x] == 0 :
                for n in range(1,numPlayers+1) :
                    if possible(y, x, n) :
                        grid[y][x] = n
                        if not (x-3)%4:
                            print(grid)
                        solve()
                        grid[y][x] = 0
                return
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
