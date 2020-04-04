import tkinter as tk
from KruisKlaveren import KruisGrid

grid=[]

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

class MainApp(tk.Tk):
    def __init__(self):
        self.root = tk.Tk.__init__(self)
        self.main=MainFrame(self)
        self.main.pack(side=tk.LEFT)
        self.keuzes=KeuzeFrame(self, self.main.reset)
        self.keuzes.pack(side=tk.TOP)

class KeuzeFrame(tk.Frame):
    def __init__(self,parent,set_function):
        tk.Frame.__init__(self,parent)
        self.keuze=tk.IntVar()
        self.keuzeArray=[4,5,6,7,8]
        self.keuzeMenu=tk.OptionMenu(self,self.keuze,*self.keuzeArray,command=set_function)
        self.keuzeMenu.pack()


class MainFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.frame=tk.LabelFrame(self,text="Tafels")
        self.grid=[]
        self.running=False
        self.rondeLabel=tk.Label(self.frame,text="ronde:")
        self.rondeLabel.grid(column=0,row=0)
        self.rondenummers=[]

    def reset(self,grid):
        #check if data exist in grid, if so reset data and frames
        if len(self.grid):
            self.grid.stop()
            #need code for resetingen frames, need frames first.



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
