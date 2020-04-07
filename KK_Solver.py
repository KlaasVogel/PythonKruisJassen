import tkinter as tk
from KruisKlaveren import KruisGrid
from math import ceil

grid=[]

#function to create nice gradient of colors for players
def colorPicker(min,max,value):
    try:
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
    except Exception as e:
        print("ERROR in Colorpicker!!!")
        print(e)
        kleuren=["light grey","light grey"]
    finally:
        return kleuren

class MainApp(tk.Tk):
    def __init__(self):
        self.root = tk.Tk.__init__(self)
        self.main=MainFrame(self)
        self.keuzes=KeuzeFrame(self, self.main.reset)
        self.keuzes.pack(fill=tk.X,side=tk.TOP,expand=True)
        self.main.pack(side=tk.TOP)
        self.protocol("WM_DELETE_WINDOW", self.delete_window)

    def delete_window(self):
        print("closing window")
        try:
            self.main.grid.stop()
        except Eception as e:
            print("ERROR closing grid:")
            print(e)
        finally:
            self.destroy()


class KeuzeFrame(tk.Frame):
    def __init__(self,parent,set_function):
        tk.Frame.__init__(self,parent)
        keuzeArray=[4,5,6,7,8]
        label=tk.Label(self,text="Select number of tables:")
        label.pack(side=tk.LEFT)
        self.keuze=tk.IntVar()
        self.keuzeMenu=tk.OptionMenu(self,self.keuze,*keuzeArray,command=set_function)
        self.keuzeMenu.pack(side=tk.RIGHT)
        self.keuze.set(keuzeArray[0])
        set_function(self.keuze.get())

class MainFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.grid=[]
        self.running=False
        self.speed=tk.IntVar()
        self.count=tk.IntVar()
        self.percent=tk.StringVar()
        self.time=tk.StringVar()
        #1st frame inside of mainFrame: (pogressFrame with start and stop buttons)
        progressFrame=tk.LabelFrame(self,text="Progress")
        progressFrame.pack(side=tk.TOP)
        #frames inside of progressframe
        self.startbutton=tk.Button(progressFrame, text="START",bg='dark sea green',height='3',width='6',command=self.start,state=tk.DISABLED)
        self.startbutton.config(activebackground='green2')
        self.startbutton.grid(row=0,column=0,rowspan=3)
        self.stopbutton=tk.Button(progressFrame, text="STOP",height='3',width='6',command=self.stop,state=tk.DISABLED)
        self.stopbutton.config(activebackground='red2')
        self.stopbutton.grid(row=0, column=4, rowspan=3)
        self.progresslabels={}
        self.tablelabels=[]
        self.rounds=[]
        titleFrame=tk.Frame(progressFrame)
        titleFrame.grid(row=0,column=1,columnspan=3)
        self.progresslabels["title"]=[]
        self.progresslabels["title"].append(tk.Label(titleFrame,text="\"Kruisjassen\" Table Arranger:"))
        self.progresslabels["title"].append(tk.Label(titleFrame,text=".."))
        self.progresslabels["title"].append(tk.Label(titleFrame,text="Tables  -"))
        self.progresslabels["title"].append(tk.Label(titleFrame,text=".."))
        self.progresslabels["title"].append(tk.Label(titleFrame,text="Rounds"))
        stateFrame=tk.Frame(progressFrame)
        stateFrame.grid(row=1,column=1)
        self.progresslabels["state"]=[]
        self.progresslabels["state"].append(tk.Label(stateFrame,text="state:"))
        self.progresslabels["state"].append(tk.Label(stateFrame,text="paused",fg='orange'))
        countFrame=tk.Frame(progressFrame)
        countFrame.grid(row=1,column=2)
        self.progresslabels["count"]=[]
        self.progresslabels["count"].append(tk.Label(countFrame,text="Steps:"))
        self.progresslabels["count"].append(tk.Label(countFrame,textvariable=self.count))
        speedFrame=tk.Frame(progressFrame)
        speedFrame.grid(row=1,column=3)
        self.progresslabels["speed"]=[]
        self.progresslabels["speed"].append(tk.Label(speedFrame,text="Speed:"))
        self.progresslabels["speed"].append(tk.Label(speedFrame,textvariable=self.speed))
        self.progresslabels["speed"].append(tk.Label(speedFrame,text="steps/minute"))
        procentFrame=tk.Frame(progressFrame)
        procentFrame.grid(row=2,column=1)
        self.progresslabels["procent"]=[]
        self.progresslabels["procent"].append(tk.Label(procentFrame,text="Progress:"))
        self.progresslabels["procent"].append(tk.Label(procentFrame,textvariable=self.percent))
        timeFrame=tk.Frame(progressFrame)
        timeFrame.grid(row=3,column=0,columnspan=5)
        self.progresslabels["time"]=[]
        self.progresslabels["time"].append(tk.Label(timeFrame,text="Time Remaining:"))
        self.progresslabels["time"].append(tk.Label(timeFrame,textvariable=self.time))
        for key in self.progresslabels:
            for label in self.progresslabels[key]:
                label.pack(side=tk.LEFT)
        #2nd Frame inside of MainFrame (grid)
        self.gridFrame=tk.LabelFrame(self, text="Rounds")
        self.gridFrame.pack(side=tk.TOP,padx=30)

    def build(self):
        self.rounds=[]
        if len(self.grid):
            for x in range(self.grid.numTables):
                self.tablelabels.append(TableLabel(self.gridFrame,"Table No. {}".format(x+1)))
                self.tablelabels[-1].grid(row=0,column=1+x*self.grid.tableSize,columnspan=self.grid.tableSize)
                for z in range(self.grid.tableSize):
                    self.gridFrame.grid_columnconfigure(1+x*self.grid.tableSize+z,weight=1, minsize=20)
            for y in range(self.grid.numRounds):
                self.tablelabels.append(TableLabel(self.gridFrame,"Round {}:".format(y+1)))
                self.tablelabels[-1].grid(row=1+y,column=0)
            for y in range(self.grid.numRounds):
                self.rounds.append([])
                for x in range(self.grid.numTables):
                    self.rounds[y].append([])
                    for z in range(self.grid.tableSize):
                        self.rounds[y][x].append(InnerGrid(self.gridFrame,self.grid.numPlayers))
                        self.rounds[y][x][-1].grid(row=1+y,column=1+x*self.grid.tableSize+z,sticky='we')
                        self.rounds[y][x][-1].update(self.grid[y][x][z])
    def clear(self):
        for round in self.rounds:
            for table in round:
                for player in table:
                    player.clear()
        for label in self.tablelabels:
            label.clear()

    def reset(self,numTables):
        #check if data exist in grid, if so reset data and frames
        if len(self.grid):
            self.grid.stop()
            self.clear()
        self.running=False
        self.grid=KruisGrid(numTables)
        self.progresslabels["title"][1].config(text=self.grid.numTables)
        self.progresslabels["title"][3].config(text=self.grid.numRounds)
        self.startbutton.config(state=tk.NORMAL,bg='pale green',relief=tk.RAISED)
        self.stopbutton.config(state=tk.DISABLED,bg='LightPink3',relief=tk.SUNKEN)
        self.build()

    def start(self):
        self.startbutton.config(state=tk.DISABLED, bg='green2', relief=tk.SUNKEN)
        self.stopbutton.config(state=tk.NORMAL,bg='red3',relief=tk.RAISED)
        self.running=True
        self.grid.start()
        self.show()

    def stop(self):
        self.startbutton.config(state=tk.NORMAL, bg='pale green', relief=tk.RAISED)
        self.stopbutton.config(state=tk.DISABLED,bg='red2',relief=tk.SUNKEN)
        self.running=False
        self.grid.stop()

    def show(self):
        if self.running:
            grid=self.grid.getall()
            for y in range(self.grid.numRounds):
                for x in range(self.grid.numTables):
                    for z in range(self.grid.tableSize):
                        self.rounds[y][x][z].update(grid[y][x][z])
            data=self.grid.progress()
            self.progresslabels["state"][1].config(text="running",fg='green')
            for i,var in enumerate([self.count,self.percent,self.speed,self.time]):
                var.set(data[i])
        else:
            self.progresslabels["state"][1].config(text="paused",fg='orange')

        if not self.grid.done:
            self.after(1000,self.show)

class InnerGrid(tk.Frame):
    def __init__(self, parent, max):
        tk.Frame.__init__(self,parent)
        self.max=max
        self.config(borderwidth=1,relief=tk.SUNKEN)
        self.label=tk.Label(self)
        self.label.pack(fill=tk.X,expand=True)

    def update(self,player):
        if player:
            self.label.config(text="{}".format(player), fg='black', bg=colorPicker(1, self.max, player)[0])
        else:
            self.label.config(text=" ",bg="light grey",fg='light grey')

    def clear(self):
        self.label.pack_forget()
        self.label.destroy()
        self.destroy()


class TableLabel(tk.Frame):
    def __init__(self, parent, name):
        tk.Frame.__init__(self,parent)
        self.label=tk.Label(self,text=name)
        self.label.pack()

    def clear(self):
        self.label.pack_forget()
        self.label.destroy()
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
