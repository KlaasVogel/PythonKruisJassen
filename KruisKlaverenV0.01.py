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
    self.keuzeArray=[16,20,24,28,32]
    self.keuzeMenu=tk.OptionMenu(self,self.keuze,*self.keuzeArray,command=self.parent.reset)
    self.keuzeMenu.pack()

class Tafels(list):
  def __init__(self,parent,*args,**kwargs):
    self.frame=tk.LabelFrame(parent,text="Tafels")
    self.frame.pack(kwargs)
    self.parent=parent
    self.rondeLabel=tk.Label(self.frame,text="ronde:")
    self.rondeLabel.grid(column=1,row=1)
    self=[]

  def set(self,numSpelers):
    if numSpelers:
      for x in range(int(numSpelers/4)):
         self.append(Tafel(numSpelers))


if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
