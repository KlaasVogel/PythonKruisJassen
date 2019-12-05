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
    self.keuzes=KeuzeFrame(self)


class KeuzeFrame(tk.Frame):
  def __init__(self,parent):
    tk.Frame.__init__(self,parent)
    self.pack()
    self.parent=parent
    self.keuze=tk.IntVar()
    self.keuzeArray=[16,20,24,28,32]
    self.label1=tk.Label(self,textvariable=self.keuze)
    self.label1.pack()


if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
