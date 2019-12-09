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
    self.rondeLabel.grid(column=0,row=0)
    self.rondenummers=[]

  def set(self,numTafels):
    for tafel in self:
      tafel.reset()
    self.clear()
    for rondenummer in self.rondenummers:
      rondenummer.destroy()
    self.rondenummers=[]
    if numTafels:
      rondes=int((int(numTafels)*4-1)/3)
      for x in range(rondes):
        self.rondenummers.append(tk.Label(self.frame,text="{}".format(x+1)))
        self.rondenummers[-1].grid(row=x+1,column=0)
      for x in range(int(numTafels)):
         self.append(Tafel(self.frame,numTafels,x,rondes))

class Tafel(list):
  def __init__(self,parent,numTafels,tafelNummer,rondes):
    self.label=tk.Label(parent, text="Tafel {}".format(tafelNummer+1))
    self.label.grid(row=0,column=int(1+tafelNummer*4),padx=(25,0))
    for rondeNummer in range(rondes):
      self.append(Ronde(parent,numTafels,tafelNummer,rondeNummer))

  def reset(self):
    for ronde in self:
      ronde.reset()
    self.clear()
    self.label.destroy()

class Ronde:
  def __init__(self,parent,numTafels,tafelNummer,rondeNummer):
    self.parent=parent
    self.tafelNummer=tafelNummer
    self.optiesFrame=tk.Frame(self.parent,highlightbackground="black",highlightthickness=1)
    self.optiesFrame.grid(row=rondeNummer+1,column=1 + tafelNummer*4,columnspan=4)
    self.vlakken=[]
    self.opties=[]
    for y in range(4):
      for x in range(numTafels):
        value=y*numTafels+x+1
        self.opties.append(tk.Button(self.optiesFrame,name="button{}{}".format(y,x),bd=1,font=('Helvetica', '7'),text="{}".format(value),command=lambda i=value: self.kiesOptie(i)))
        self.opties[-1].grid(row=y,column=x,sticky='NESW')

  def kiesOptie(self,*args):
    print(args)

  def reset(self):
    for optie in self.opties:
      optie.destroy()
    self.optiesFrame.destroy()

if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
