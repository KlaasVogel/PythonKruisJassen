import tkinter as tk
import sys
import logging
from logger import MyLogger
from math import ceil

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)


def colorPicker(min,max,value):
  values=[154,100,255]
  schema=[[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]]
  kleuren=["#","#"]
  #bepaal welk kwintiel
  kwintiel=ceil(5*value/(max-min+1))
  tussenwaarde=5*(value)/(max-min+1)-kwintiel+1
  for x in range(2):
    for i in range(3):
      startKleur = values[2] if (schema[kwintiel-1][i]) else values[x]
      eindKleur = values[2] if (schema[kwintiel][i]) else values[x]
      kleuren[x]+=hex(int(startKleur+tussenwaarde*(eindKleur-startKleur)))[2:]
  #print("{} : {} , {} - {}".format(value,kwintiel,tussenwaarde,kleuren))
  #kleuren=["#ffa9a9","#ff6464"]
  return kleuren


class MainApp(tk.Tk):
  def __init__(self):
    self.root = tk.Tk.__init__(self)
    self.keuzes=KeuzeFrame(self, side=tk.TOP)
    self.tafels=Tafels(self, side=tk.LEFT)

  def reset(self,nieuwKeuze):
   self.tafels.set(nieuwKeuze)

  def analyse(self):
    print("start analyse")


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
         self.append(Tafel(self.frame,numTafels,x,rondes,self.parent.analyse))


class Tafel(list):
  def __init__(self,parent,numTafels,tafelNummer,rondes,call_update):
    self.label=tk.Label(parent, text="Tafel {}".format(tafelNummer+1))
    self.label.grid(row=0,column=int(1+tafelNummer*4),padx=(25,0))
    for rondeNummer in range(rondes):
      self.append(Ronde(parent,numTafels,tafelNummer,rondeNummer,call_update))

  def reset(self):
    for ronde in self:
      ronde.reset()
    self.clear()
    self.label.destroy()


class Ronde(list):
  def __init__(self,parent,numTafels,tafelNummer,rondeNummer,call_update):
    self.parent=parent
    self.tafelNummer=tafelNummer
    self.call_update=call_update
    self.optiesFrame=tk.Frame(self.parent,highlightbackground="black",highlightthickness=1)
    self.optiesFrame.grid(row=rondeNummer+1,column=1 + tafelNummer*4,columnspan=4)
    self.opties=[]
    for y in range(4):
      for x in range(numTafels):
        value=y*numTafels+x+1
        self.opties.append(Optie(self.optiesFrame,numTafels*4,value,self.update))

  def reset(self):
    for optie in self.opties:
      optie.reset()
    self.optiesFrame.destroy()

  def update(self):
    #check if round is full (4 players) and disable rest
    chosen=0
    for optie in self.opties:
      if optie.active and optie.chosen:
        chosen+=1
    if (chosen>=4):
      x=0
      for optie in self.opties:
        if not optie.chosen:
          optie.disable()
        else:
          x+=1
          optie.setFinal(x)
    self.call_update()


class Optie:
  def __init__(self,parent,numSpelers,value,call_update):
    self.parent=parent
    self.value=value
    self.call_update=call_update
    self.chosen=False
    self.active=True
    self.colors=colorPicker(1,numSpelers,value)
    self.textsize='6' if (numSpelers>=7) else '9'
    self.setCoords(numSpelers)
    self.build()

  def build(self):
    if self.active:
      if self.chosen:
        self.widget=tk.Label(self.parent,bg=self.colors[1],bd=1,font=('Helvetica', self.textsize),text="{}".format(self.value))
      else:
        self.widget=tk.Button(self.parent,bg=self.colors[0],bd=1,font=('Helvetica', self.textsize),text="{}".format(self.value),command=self.kiesOptie)
      self.show()

  def reset(self):
    if self.active:
      self.widget.destroy()

  def setCoords(self,total):
    xMax=int((total-total%4)/4)
    x=int((self.value-1)%xMax)
    y=int((self.value-1)/xMax)
    self.coords=[x,y]

  def show(self):
    self.widget.grid(row=self.coords[1],column=self.coords[0],sticky='NESW')

  def setFinal(self, x):
    self.textsize='11'
    self.coords=[x,0]
    self.widget.destroy()
    self.build()

  def disable(self):
    self.active=False
    self.widget.destroy()

  def kiesOptie(self,*args):
    print("kies optie: {}".format(self.value))
    self.chosen=True
    self.widget.destroy()
    self.build()
    self.call_update()


if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
