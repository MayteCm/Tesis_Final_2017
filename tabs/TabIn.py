# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author: 
"""
#imports native
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QHBoxLayout)
from PyQt5.QtGui import (QPixmap)

class TabIn(QHBoxLayout):
    
    def __init__(self):      
        super().__init__()
        self.initUI()
            
    def initUI(self):
        pixmap = QPixmap("./tabs/landing.png")
        logo_ana = QtWidgets.QLabel()
        logo_ana.setPixmap(pixmap)
        self.addWidget(logo_ana)