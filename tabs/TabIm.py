# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author: 
"""
#imports native
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog)
from PyQt5.QtGui import (QPixmap)
import os

class TabIm(QVBoxLayout):
    
    def selectFolder(self):
        self.nombre_video = ''
        fileName = QFileDialog.getExistingDirectory(None, "Selecciona una carpeta")
        if fileName:
            self.nombre_video = fileName
            self.showImages()
            
    def showImages(self):
        count = 0
        print(os.listdir(self.nombre_video))
        self.container = QHBoxLayout()
        for i in os.listdir(self.nombre_video):
            if i.find('.png') != -1 and count < 3:
                count += 1
                logo = QtWidgets.QLabel()
                logo.setMaximumHeight(400)
                logo.setMaximumWidth(500)
                logo.setScaledContents(True)
                logo.setPixmap(QPixmap(self.nombre_video+"/"+i))
                logo.show()
                self.container.addWidget(logo)
                
        self.addLayout(self.container)
        
    def __init__(self):      
        super().__init__()
        self.initUI()
            
    def initUI(self):
        
        self.nombre_video = ''
    
        self.container = QHBoxLayout()
        
        buttonBlue = QPushButton('Abrir resultados')
        buttonBlue.clicked.connect(self.selectFolder)
                
        self.addWidget(buttonBlue)