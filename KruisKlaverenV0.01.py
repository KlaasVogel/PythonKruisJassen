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
    self.tafels=[]

  def reset(self):
    for tafel in self.tafels:
      tafel.reset()

  def createTables(self):
    pass


class KeuzeFrame(tk.Frame):
  def __init__(self,parent,*args,**kwargs):
    tk.Frame.__init__(self,parent)
    self.pack(kwargs)
    self.parent=parent
    self.keuze=tk.IntVar()
    self.keuzeArray=[16,20,24,28,32]
    self.keuzeMenu=tk.OptionMenu(self,self.keuze,*self.keuzeArray,command=self.parent.reset)
    self.keuzeMenu.pack()

class Tafel(tk.LabelFrame):
  def __init__(self,parent,*args,**kwargs):
    pass

  def reset(self):
    pass




if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
