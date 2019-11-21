from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGroupBox, QSlider, QLabel, QVBoxLayout, QHBoxLayout, \
    QPushButton, QFormLayout, QGridLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor
from random import random
import numpy as np
from numpy import sin, cos, pi
from enum import Enum
import sys
import pyqtgraph
from pyqtgraph import PlotWidget, plot

class main(QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)

        # Setup GUI central widget and give title
        # Central widget in the workspace where smaller
        # sections and widgets can be laid out
        self.setWindowTitle("GFR Live Data GUI")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Create vertically stacking subsections of main window.
        verticalSections = QVBoxLayout()

        # Add stuff to vertical stacking subsection
        title = QLabel("Hello World from PyQt", self)
        title.setAlignment(QtCore.Qt.AlignLeft)
        verticalSections.addWidget(title)

        # Create horizontal format subsection within vertical stacking subsection
        horizontalSections = QHBoxLayout()
        verticalSections.addLayout(horizontalSections)

        # Add stuff to left side of horizontal subsection
        programDescription = QLabel("This tells you what the program does which is currently precisely nothing...")
        horizontalSections.addWidget(programDescription)

        # Add Graph to right side of horizontal subsection
        graph = pyqtgraph.PlotWidget()
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        graph.plot(hour, temperature)
        horizontalSections.addWidget(graph)

        centralWidget.setLayout(verticalSections)
        # gridLayout.addWidget(title, 0, 0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = main()
    mainWin.show()
    sys.exit( app.exec_() )
