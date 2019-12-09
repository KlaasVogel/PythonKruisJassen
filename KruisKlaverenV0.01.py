import tkinter as tk
import sys
import logging
from logger import MyLogger

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)

class MainApp(tk.Tk):
  def __init__(self):
    self.root = tk.Tk.__init__(self)
    self.keuzes=KeuzeFrame(self, side=tk.TOP)
    self.tafels=Tafels(self, side=tk.LEFT)

  def reset(self,nieuwKeuze):
   self.tafels.set(nieuwKeuze)

class KeuzeFrame(tk.Frame):
  def __init__(self,parent,*args,**kwargs):
    tk.Frame.__init__(self,parent)
    self.pack(kwargs)
    self.parent=parent
    self.keuze=tk.IntVar()
    self.keuzeArray=[4,5,6,7,8]
    self.keuzeMenu=tk.OptionMenu(self,self.keuze,*self.keuzeArray,command=self.parent.reset)
    self.keuzeMenu.pack()

class Tafels(list):
  def __init__(self,parent,*args,**kwargs):
    self.frame=tk.LabelFrame(parent,text="Tafels")
    self.frame.pack(kwargs)
    self.parent=parent
    self.rondeLabel=tk.Label(self.frame,text="ronde:")
    self.rondeLabel.grid(column=1,row=1)

  def set(self,numTafels):
    for tafel in self:
      tafel.reset()
    if numTafels:
      for x in range(int(numTafels)):
         self.append(Tafel(self.frame,numTafels,x))

class Tafel:
  def __init__(self,parent,numTafels,tafelNummer):
    self.parent=parent
    self.tafelNummer=tafelNummer
    self.vakjes=[]
    self.opties=[]
    for x in range(int(numTafels)*4):
      self.opties.append(x+1)
    print("set: ", tafelNummer,self.opties)

  def reset(self):
    print("reset: ",self.tafelNummer)

if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
