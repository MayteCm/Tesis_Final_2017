# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author: 
"""
#imports native
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from PyQt5 import QtWidgets
import numpy as np
from PyQt5.QtWidgets import (QPushButton, QTabWidget, QVBoxLayout, QWidget, QFileDialog)
import cv2
    

class TabRe(QVBoxLayout):
    
    def __init__(self):      
        super().__init__()
        self.initUI()

    def initRois(self):
        if self.nombre_video and self.nombre_video != '':
            if self.show == True:
                self.w
                self.removeWidget(self.w)
            
            self.show = True

            pg.setConfigOptions(imageAxisOrder='row-major')
            cap = cv2.VideoCapture(self.nombre_video)#definición de video 
            ret, frame = cap.read()# definición de variable de captura de video
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#definición de la  mascara de escala a grises
            cap.release()# captura 
            
            arr = gray #captura/arreglo en escala de grises
            
            ## create GUI
            w = pg.GraphicsWindow(size=(0,0), border=True)#dimensiones de la pantalla
            self.w = w
            #w.setWindowTitle('Regiones de Interés')#titulo de la pantalla
            self.addWidget(w)
            self.tabs.hide()
            
            w1 = w.addLayout(row=0, col=0)
            
            v1a = w1.addViewBox(row=1, col=0, lockAspect=True, invertY=True)
            v1b = w1.addViewBox(row=2, col=0, lockAspect=True, invertY=True)
            
            img1a = pg.ImageItem(arr)
            img1b = pg.ImageItem()
            
            v1a.addItem(img1a)
            v1b.addItem(img1b)
            
            v1a.disableAutoRange('xy')
            v1b.disableAutoRange('xy')
            
            v1a.autoRange()
            v1b.autoRange()
                    
            #-----------------IZQUIERDA-----------------------
            izquierda = pg.ROI([280,300], [350,80], pen=(2,9))#Color: VERDE
            ## Manijas Horizontales
            izquierda.addScaleHandle([0, 0.5], [1, 0.5])#izquierda
            izquierda.addScaleHandle([1, 0.5], [0, 0.5])#deracha
            ## Manijas Verticales
            izquierda.addScaleHandle([0.5, 0], [0.5, 1])#arriba
            izquierda.addScaleHandle([0.5, 1], [0.5, 0])#abajo
            
            #----------------DERECHA------------------------------
            derecha = pg.ROI([710,300], [350,80],pen=(0,9))#Color: ROJO
            ## Manijas Horizontales
            derecha.addScaleHandle([0, 0.5], [1, 0.5])#izquierda
            derecha.addScaleHandle([1, 0.5], [0, 0.5])#deracha
            ## Manijas Verticales
            derecha.addScaleHandle([0.5, 0], [0.5, 1])#arriba
            derecha.addScaleHandle([0.5, 1], [0.5, 0])#abajo
            
            #-----------------CENTRO------------------------------
            centro = pg.ROI([630,300], [80,80],pen=(1,9))#Color: NARANJA
            ## Manijas Horizontales
            centro.addScaleHandle([0, 0.5], [1, 0.5])#izquierda
            centro.addScaleHandle([1, 0.5], [0, 0.5])#deracha
            ## Manijas Verticales
            centro.addScaleHandle([0.5, 0], [0.5, 1])#arriba
            centro.addScaleHandle([0.5, 1], [0.5, 0])#abajo
            
            #-----------------ABAJO-------------------------------
            abajo = pg.ROI([630,380], [80,300],pen=(5,9))#Color: AZUL
            ## Manijas Horizontales
            abajo.addScaleHandle([0, 0.5], [1, 0.5])#izquierda
            abajo.addScaleHandle([1, 0.5], [0, 0.5])#dercha
            ## Manijas Verticales
            abajo.addScaleHandle([0.5, 0], [0.5, 1])#arriba
            abajo.addScaleHandle([0.5, 1], [0.5, 0])#abajo
            
            #-------------------ARRIBA-----------------------------                
            arriba = pg.ROI([630,-1], [80,300],pen=(7,9))#Color: MORADO
            ## Manijas horizontales
            arriba.addScaleHandle([0, 0.5], [1, 0.5])#izquierda
            arriba.addScaleHandle([1, 0.5], [0, 0.5])#dereacha
            ## Manijas Verticales
            arriba.addScaleHandle([0.5, 0], [0.5, 1])#arriba
            arriba.addScaleHandle([0.5, 1], [0.5, 0])#abajo
            
            rois = []
            
            rois.append(izquierda)
            rois.append(derecha)
            rois.append(centro)
            rois.append(abajo)
            rois.append(arriba)
            
            def update(roi):
                img1b.setImage(roi.getArrayRegion(gray, img1a), levels=(0, arr.max()))
                v1b.autoRange()
                #print(roi.getArraySlice(arr, img1a, returnSlice=False))
            
                coorden=np.zeros((20))
                cont = 0
                for i in range (5):
                    for j in range(2):
                        for k in range(2):
                                coorden[cont]= rois[i].getArraySlice(arr, img1a, returnSlice=False)[0][j][k]       
                                cont = cont+1
                                
            #                    #print(i,'\t', j,'\t', k)
                np.savetxt('./tabs/rois.conf', coorden , delimiter=',')
            
            for roi in rois:
                roi.sigRegionChanged.connect(update)
                v1a.addItem(roi)
        else:
            QtGui.QMessageBox.critical(None, "Alerta","Selecciona un archivo",QtGui.QMessageBox.Ok)
            
    def openFile(self):
        self.nombre_video = ''
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Selecciona...", "","Video Files (*.avi *.wmv)", options=options)
        if fileName:
            self.nombre_video = fileName
            self.titleEdit_nom.setText(fileName)
        
    def initUI(self):
        self.nombre_video = ''
        self.show = False
        self.tabs = QTabWidget()
        self.tabIn = QWidget()
        self.tabs.addTab(self.tabIn,"ROIS")
        self.addWidget(self.tabs)
        
        self.titleEdit_nom = QtWidgets.QLineEdit()
        self.titleEdit_nom.setDisabled(1)
        self.titleEdit_nom.setPlaceholderText("Selecciona un archivo") 
        self.addWidget(self.titleEdit_nom)
        
        buttonS = QPushButton('Seleccionar Video')
        buttonV = QPushButton('Configurar')
        buttonV.clicked.connect(self.initRois)
        buttonS.clicked.connect(self.openFile)
        self.addWidget(buttonS)
        self.addWidget(buttonV)