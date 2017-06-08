# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author: 
"""
#imports native
from PyQt5.QtWidgets import (QHBoxLayout)
from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np

class TabGr(QHBoxLayout):
    
    def __init__(self):      
        super().__init__()
        self.initUI()
            
    def initUI(self):
        
        Contenido_4 = QtWidgets.QHBoxLayout() 
        
        cuadrografica = QtWidgets.QVBoxLayout() 
        tabla = QtWidgets.QVBoxLayout() 
        grafica = pg.PlotWidget(title="GRAFICA")

        x = np.arange(1)

        bg1 = pg.BarGraphItem(x=x,x1=x+1,y1=1,y2=1,  width=0.1, brush=(0, 0, 255))
        bg2 = pg.BarGraphItem(x=x,x1=x+2,y1=2,y2=2,  width=0.1, brush=(0, 255, 0))
        bg3 = pg.BarGraphItem(x=x,x1=x+3,y1=3,y2=3,  width=0.1, brush=(255, 0, 0))
        
        bg4 = pg.BarGraphItem(x=x,x1=x+4,y1=4,y2=4,  width=0.1, brush=(0, 0, 255))
        bg5 = pg.BarGraphItem(x=x,x1=x+5,y1=5,y2=5,  width=0.1, brush=(0, 255, 0))
        bg6 = pg.BarGraphItem(x=x,x1=x+6,y1=6,y2=6,  width=0.1, brush=(255, 0, 0))                
                   
        grafica.addItem(bg1)
        grafica.addItem(bg2)
        grafica.addItem(bg3)
        grafica.addItem(bg4)
        grafica.addItem(bg5)
        grafica.addItem(bg6)
        
        cuadrografica.addWidget(grafica)
        Contenido_4.addLayout(cuadrografica)
        Contenido_4.addLayout(tabla)
        self.addLayout(Contenido_4)