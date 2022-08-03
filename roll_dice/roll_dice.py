import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import random
import numpy as np
import seaborn as sns


import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use("Qt5Agg")

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)        

class MainWindow(QMainWindow):

    def __init__(self):
        """MainWindow constructor."""
        super(MainWindow, self).__init__()
        self.create_ui()
        self.setGeometry(50, 200, 1700, 550)

        self.show()
    def create_ui(self):
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setGeometry(450,100,800,200)
        self.xdata = list(range(1, 13))
        self.ydata = [0] * 12    
                
    def roll_dice(self):

        die_1 = random.randrange(1, 7)
        die_2 = random.randrange(1, 7)
        dice_sum = die_1 + die_2
        
        self.ydata[dice_sum - 1] += 1 
        self.canvas.axes.cla() 
        colors_list = ['Red','Orange', 'Blue', 'Purple']
        self.canvas.axes.bar(self.xdata, self.ydata)
        self.canvas.draw()

        if die_1 == 1:
            pass
        elif die_1 == 2:
            pass
        elif die_1 == 3:
            pass
        elif die_1 == 4:
            pass
        elif die_1 == 5:
            pass
        elif die_1 == 6:
            pass

        if die_2 == 1:
            pass
        elif die_2 == 2:
            pass
        elif die_2 == 3:
            pass
        elif die_2 == 4:
            pass
        elif die_2 == 5:
            pass
        elif die_2 == 6:
            pass       
               
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
