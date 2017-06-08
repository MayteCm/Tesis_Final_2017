# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author: 
"""
#imports native
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox)
from PyQt5 import QtGui
import cv2,datetime,os
import numpy as np
import pyqtgraph as pg
import xlsxwriter
from matplotlib import pyplot as plt

class TabPr(QVBoxLayout):
    
    def __init__(self):      
        super().__init__()
        self.initUI()

    def initReproduccir(self):   

        if self.nombre_video and self.nombre_video != '':
            #abrir el archivo de los valores de ROIS
            archivo = open("./tabs/rois.conf", "r")
            #numero de líneas en el archivo
            tam=len(archivo.readlines())
            #ubicar e puntero al final del archivo
            archivo.seek(0)
            mm=np.zeros((20))
            for i in range(tam):
                line=archivo.readline()
                #lee una linea
                line=line.replace('\n','')
                #remplaza un retorno de carro con un espacio
                l=float(line)
                l=int(l)
                # convierte a l de tipo entero
                #print(l)
                mm[i]=l
             
            #print(mm)
            archivo.close()
    
            cap = cv2.VideoCapture(self.nombre_video)
            
            while(cap.isOpened()):
                
                ret, frame = cap.read()
                
                if ret:
                    cv2.putText(frame, "Q para salir",(10,50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 1, 255))
                    cv2.putText(frame, "Time " + str('%.0f sec' % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000.)),(10,100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 1, 255))

                    cv2.imshow('Procesamiento',frame)
                    cv2.namedWindow('Procesamiento',cv2.WINDOW_NORMAL)
                
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
            cap.release()
            cv2.destroyAllWindows()
        
        else:
            QtGui.QMessageBox.critical(None, "Alerta","Selecciona un video",QtGui.QMessageBox.Ok)
    
    def initProcesar(self):   
        if self.nombre_video and self.nombre_video != '': 
            #print(os.getcwd())
            archivo = open("./tabs/rois.conf", "r")#abrir el archivo de los valores de ROIS
            
            tam=len(archivo.readlines())#numero de líneas en el archivo
            
            archivo.seek(0)#ubicar e puntero al final del archivo
            
            mm=np.zeros((20))
            
            for i in range(tam):
                line=archivo.readline()#lee una linea
                line=line.replace('\n','')#remplaza un retorno de carro con un espacio
                l=float(line)
                l=int(l)# convierte a l de tipo entero
                #print(l)
                mm[i]=l
            
            #print(mm)
            archivo.close()
            
            cap = cv2.VideoCapture(self.nombre_video)
            cnt = np.ndarray(0)
            X = 0
            Y = 0
            cIzquierda=0
            cDerecha=0
            cCentro=0
            cArriba=0
            cAbajo=0
            tIzquierda=0
            tDerecha=0
            tCentro=0
            tArriba=0
            tAbajo=0
            
            # estatus de lugar
            brazoA = False
            brazoC = False
            centro = False
            
            # contador por lugar
            brazoACount = 0
            brazoCCount = 0
            centroCount = 0
            
            # valor anterior
            _tba = 0
            _tbc = 0
            _ttc = 0
            
            linePoints = []
            heatMapPoints = []
            interesPoints = []
        
            foreground = cv2.imread('./tabs/base.png')
            
            kernel = np.ones((5, 5), np.uint8)                        
            foreground_gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(foreground_gray, 240, 255, cv2.THRESH_BINARY)                        
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            output = np.zeros(foreground.shape, dtype=foreground.dtype)
            lastFrame = None
            self.totalTime = 0
            
            while(cap.isOpened()):
                ret, frame = cap.read()
                
                if ret:
                    lastFrame = frame
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    #contraste gamma    
                    gamma = 2
                    tmpImg = gray.copy()
                    #Normalizar imagen
                    img2 = tmpImg/255;
                    #Aplicar transformacion gamma
                    img2 = np.power(img2,gamma)
                    #Regresar al intervalo [0,255]
                    img2 = np.uint8(255*img2)
                    
                    mask = np.ndarray(np.shape(img2),dtype=np.uint8)
                    mask[:,:] = 0
                    
                    mask[int(mm[0]) : int(mm[1]), int(mm[2]): int(mm[3])]     = img2[int(mm[0]) : int(mm[1]), int(mm[2]): int(mm[3])]
                    mask[int(mm[4]) : int(mm[5]), int(mm[6]): int(mm[7])]     = img2[int(mm[4]) : int(mm[5]), int(mm[6]): int(mm[7])]
                    mask[int(mm[8]) : int(mm[9]), int(mm[10]): int(mm[11])]   = img2[int(mm[8]) : int(mm[9]), int(mm[10]): int(mm[11])]
                    mask[int(mm[12]) : int(mm[13]), int(mm[14]): int(mm[15])] = img2[int(mm[12]) : int(mm[13]), int(mm[14]): int(mm[15])]
                    mask[int(mm[16]) : int(mm[17]), int(mm[18]): int(mm[19])] = img2[int(mm[16]) : int(mm[17]), int(mm[18]): int(mm[19])]
                
                    kernelTam = (55,55)
                    grayBlur = cv2.GaussianBlur(mask, kernelTam, 0)
                    _, thresh = cv2.threshold(grayBlur, 120, 255, cv2.THRESH_BINARY)
                    
                    ##Se definen las áreas de interés dentro de la imagen ya binarizada (0's y 1's)
                    areaIzquierda = thresh[int(mm[0]) : int(mm[1]), int(mm[2]): int(mm[3])]
                    areaDerecha = thresh[int(mm[4]) : int(mm[5]), int(mm[6]): int(mm[7])]
                    #areaCentro = thresh[int(mm[8]) : int(mm[9]), int(mm[10]): int(mm[11])]
                    areaArriba = thresh[int(mm[12]) : int(mm[13]), int(mm[14]): int(mm[15])]
                    areaAbajo = thresh[int(mm[16]) : int(mm[17]), int(mm[18]): int(mm[19])]
                
                    _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)###**
                
                    #start = time.time()
                    
                    if len(contours) < 1:   
                        #TODO more pythonic way of the check
                        cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2, cv2.LINE_AA)
                        # contorno Verde
                        cv2.circle(frame, (X, Y), 5, (0, 0, 255), -1)
                        #centro rojo
                    else:
                        # c:Contorno, contours: contornos
                        cnt = contours[np.argmax(map(cv2.contourArea, contours))]
                        M = cv2.moments(cnt)
                        if M["m00"] != 0:    
                            X = int(M["m10"] / M["m00"])
                            Y = int(M["m01"] / M["m00"])
                    # contorno Verde     
                    
                    
                    cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2, cv2.LINE_AA)
                    #centro rojo
                    cv2.circle(frame, (X, Y), 5, (0, 0, 255), -1)
                    #texto rojo  
                    cv2.putText(thresh, "center", (X - 20, Y - 20),cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 1, 255), 2)
                    
                    #si es didtinto de vacio que es la ubicacion del punto inicial
                    if (len(cnt != 0)): 
                        area = cv2.contourArea(cnt)
                        #__________________IZQUIERDA
                        if mm[2] <= X <= mm[3]: 
                            if mm[0] <= Y <= mm[1]:
                                #Para preguntar la cantidad de pixeles en el areaIzquierda sumo los 1's (representan a la rata) y los comparo con la cantidad
                                #del área total, si la razón entre éstas dos medidas es mayor o igual a 75% se suma el tiempo a la variable
                                cuantos= sum(sum(areaIzquierda>0))
                                if ((cuantos/area)>=0.75):
                                    #print ('area:' + str(area) + '\t' + str(cuantos))
                                    cIzquierda = cIzquierda+1####################??????????
                                    #print("izquierda")
                                    #print(cIzquierda)
                                    tIzquierda = tIzquierda + (1/20)
                                    #print(tIzquierda)
                        #__________________DERECHA               
                        if mm[6] <= X <= mm[7]:
                            if mm[4] <= Y <= mm[5]:
                                cuantos = sum(sum(areaDerecha>0))
                                if ((cuantos/area)>=0.75):
                                    cDerecha = cDerecha+1####################??????????
                                    #print("dererecha")
                                    #print( cDerecha)
                                    tDerecha = tDerecha + (1/20)
                                    #print(tDerecha)
                        #__________________CENTRO                
                        if mm[10] <= X <= mm[11]:
                            if mm[8]<= Y <= mm[9]:
                                #print( cCentro)
                                cCentro = cCentro + 1####################??????????
                                #print("centro")
                                #print( cCentro)
                                tCentro = tCentro + (1/20)
                                #print(tCentro)
                        #__________________ARRIBA
                        if mm[14] <= X <= mm[15]:
                            if mm[12] <= Y < mm[13]:
                                cuantos = sum(sum(areaArriba>0))
                                if ((cuantos/area)>=0.75):
                                    cArriba = cArriba+1####################??????????
                                    #print("arriba")
                                    #print(cArriba)
                                    tArriba = tArriba + (1/20)
                                    #print(tArriba)
                        #__________________ABAJO
                        if mm[18] < X < mm[19]:
                            if mm[16] < Y < mm[17]: 
                                cuantos = sum(sum(areaAbajo))
                                if ((cuantos/area)>=0.75):
                                    cAbajo = cAbajo+1####################??????????
                                    #print("abajo")
                                    #print( cAbajo)
                                    tAbajo = tAbajo + (1/20)
                                    #print(tAbajo)
                            
                        #Tiempo total en brazos abiertos
                        tba=(tAbajo + tArriba )                
                        #print('tba:' + str(tba))
                        #Tiempo total en brazos cerrados 
                        tbc=(tIzquierda + tDerecha)
                        #print('tbc:' + str(tbc))
                        #Tiempo total en el centro
                        ttc=(tCentro)
                        #print('ttc:' + str(ttc)) 
                        
                        # veces por posicion
                        if _ttc < ttc:
                            if not centro:
                                centro = True
                                brazoA = False
                                brazoC = False
                                centroCount += 1
                                #print('static ttc')
                            
                        if _tbc < tbc:
                            if not brazoC:
                                brazoC = True
                                brazoA = False
                                centro = False
                                brazoCCount += 1
                                #print('static tbc')
                        
                        if _tba < tba:
                            if not brazoA:
                                brazoA = True
                                centro = False
                                brazoC = False
                                brazoACount += 1
                                #print('static tba')
                        
                        #asignacion punto anterior
                        _tba = tba
                        _tbc = tbc
                        _ttc = ttc
                        
                    cv2.putText(frame, "Q para salir",(10,50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 1, 255))
                    cv2.putText(frame, "S tracker sheed",(10,25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 1, 255))
                    cv2.putText(frame, "Time " + str('%.0f sec' % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000.)),
                                (10,100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 1, 255))
                    
                    _x = X
                    _y = Y
                    
                    if _x < X or _y < X:
                        heatMapPoints.append({'x':X,'y':Y,'n':0})
                        linePoints.append({'x':X,'y':Y})
                        interesPoints.append([X,Y])
                        
                    count = 0
                    for obj in heatMapPoints:
                        if (obj['x'] < X+20 and obj['x'] > X-20) and (obj['y'] < Y+20 and obj['y'] > Y-20):
                            obj['n'] += 1
                            heatMapPoints[count] = obj
                        
                    if self.b1.isChecked() == True:
                            
                        for obj in linePoints:
                            cv2.circle(frame, (obj['x'], obj['y']), 3, (0, 255, 0), -1)#centro rojo
                        cv2.imshow('Procesamiento',frame)
                    
                    else:
                        cv2.imshow('Procesamiento',frame)
                    cv2.namedWindow('Procesamiento',cv2.WINDOW_NORMAL)
                
                    c = cv2.waitKey(1)

                    if 'q' == chr(c & 255):
                        self.data = [tba,tbc,ttc,brazoACount,brazoCCount,centroCount]
                        self.totalTime = (self.data[0]+self.data[1]+self.data[2])
                        self.fillTable()
                        break
                    
                    elif 's' == chr(c & 255):
                        self.b1.setChecked(not self.b1.isChecked())
                
                else:
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.data = [tba,tbc,ttc,brazoACount,brazoCCount,centroCount]
                        self.totalTime = (self.data[0]+self.data[1]+self.data[2])
                        self.fillTable()
                        break
                    
            #make folder
            self.folder = str(datetime.date.today())+'_'+str(datetime.datetime.now().strftime("%H-%M-%S"))
            newpath = './resultados/'+self.folder
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                    
            #puntos de interes ##########################################
            if len(interesPoints)> 5:
                Z = np.vstack(interesPoints)
                Z = np.float32(Z)
                # define criteria and apply kmeans()
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                ret,label,center=cv2.kmeans(Z,5,None,criteria,1,cv2.KMEANS_RANDOM_CENTERS)
                centers = center.tolist()
                tmp = lastFrame.copy()
                for arr in centers:
                    #print(arr)
                    cv2.circle(tmp, (int(arr[0]),int(arr[1])), 20, (0, 0, 255), -1)
                file1 = './resultados/'+self.folder+'/'+str(datetime.datetime.now().strftime("%H-%M-%S"))+'_puntos.png'
                cv2.imwrite(file1, tmp)
                
            #recorrido ##########################################
            if len(linePoints) > 0:
                tmp = lastFrame.copy()
                for obj in linePoints:
                    cv2.circle(tmp, (obj['x'], obj['y']), 3, (0, 255, 0), -1)
                file2 = './resultados/'+self.folder+'/'+str(datetime.datetime.now().strftime("%H-%M-%S"))+'_recorrido.png'
                cv2.imwrite(file2, tmp)
                
            #heatMap ##########################################
            if len(heatMapPoints) > 0:
                heatMapPoints = sorted(heatMapPoints, key=lambda x : x['n'], reverse=False)
                tmp = lastFrame.copy()
                if len(heatMapPoints) > 0:
                    max = heatMapPoints[len(heatMapPoints)-1]['n']                    
                    if max == 0 :
                        max = 1
                    color = 255/max                    
                for obj in heatMapPoints:
                    if (obj['x'] < X+20 and obj['x'] > X-20) and (obj['y'] < Y+20 and obj['y'] > Y-20):
                        obj['n'] += 1
                        heatMapPoints[count] = obj
                    cv2.circle(output, (obj['x'],obj['y']), 20, (0, 255-(obj['n']*color), 255), -1)
                opacity = 0.4
                cv2.addWeighted(output, opacity, tmp, 1 - opacity, 0, tmp)
                file3 = './resultados/'+self.folder+'/'+str(datetime.datetime.now().strftime("%H-%M-%S"))+'_heatMap.png'
                cv2.imwrite(file3, tmp)
                
            self.totalTime = (self.data[0]+self.data[1]+self.data[2])
            self.buildGraph()
            cap.release()
            cv2.destroyAllWindows()
        else:
            QtGui.QMessageBox.critical(None, "Alerta","Selecciona un video",QtGui.QMessageBox.Ok)
    
    def openFile(self):
        self.nombre_video = ''
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Selecciona...", "","Video Files (*.avi *.wmv)", options=options)
        if fileName:
            self.nombre_video = fileName
            self.titleEdit_nom.setText(fileName)
        
    def quitVideo(self):
        print('quitVideo')
        #self.dialog.close()
        
    def showVideo(self):
        #print('showVideo')
        if self.nombre_video and self.nombre_video != '':
            self.initVideo()
        else:
            QtGui.QMessageBox.critical(None, "Alerta","Selecciona un archivo",QtGui.QMessageBox.Ok)
            
    def toExcel(self):
        if len(self.data) > 0 :
            #print(self.data)
                        
            # Create a workbook and add a worksheet.
            file = './resultados/'+self.folder+'/'+str(datetime.datetime.now().strftime("%H-%M-%S"))+'_LE.xlsx'
            workbook = xlsxwriter.Workbook(file)
            worksheet = workbook.add_worksheet()
            
            # Some data we want to write to the worksheet.
            expenses = (
                ["TBA",  self.data[0] ],
                ["TBC",  self.data[1] ],
                ["TC",  self.data[2] ],
                ["EBA",  self.data[3] ],
                ["EBC",  self.data[4] ],
                ["EC",  self.data[5] ],
                ["IA",  1-(((self.data[0]/self.totalTime)+(self.data[3]/(self.data[3]+self.data[4])))/2) ],
            )
            
            # Start from the first cell. Rows and columns are zero indexed.
            row = 0
            col = 0
            
            # Iterate over the data and write it out row by row.
            for item, cost in (expenses):
                worksheet.write(row, col,     item)
                worksheet.write(row + 1, col, cost)
                col += 1
            
            workbook.close()
            QtGui.QMessageBox.information(None, "Exito","Se genero excel",QtGui.QMessageBox.Ok)
            
        else:
            QtGui.QMessageBox.critical(None, "Alerta","Aun no hay datos",QtGui.QMessageBox.Ok)
            
    def fillTable(self):
        
        self.tableWidget.setItem(0,0, QTableWidgetItem(str(self.data[0])))
        self.tableWidget.setItem(0,1, QTableWidgetItem(str(self.data[1])))
        self.tableWidget.setItem(0,2, QTableWidgetItem(str(self.data[2])))
        self.tableWidget.setItem(0,3, QTableWidgetItem(str(self.data[3])))
        self.tableWidget.setItem(0,4, QTableWidgetItem(str(self.data[4])))
        self.tableWidget.setItem(0,5, QTableWidgetItem(str(self.data[5])))
        self.tableWidget.setItem(0,6, QTableWidgetItem(str(1-(((self.data[0]/self.totalTime)+(self.data[3]/(self.data[3]+self.data[4])))/2))))
            
    def buildGraph(self):
        
        x = np.arange(1)

        bg1 = pg.BarGraphItem(x=x,x1=x+0,y1=self.data[0],width=0.1, brush=(0, 0, 255))
        bg2 = pg.BarGraphItem(x=x,x1=x+1,y1=self.data[1],width=0.1, brush=(0, 255, 0))
        bg3 = pg.BarGraphItem(x=x,x1=x+2,y1=self.data[2],width=0.1, brush=(255, 0, 0))
        bg4 = pg.BarGraphItem(x=x,x1=x+3,y1=self.data[3],width=0.1, brush=(0, 0, 255))
        bg5 = pg.BarGraphItem(x=x,x1=x+4,y1=self.data[4],width=0.1, brush=(0, 255, 0))
        bg6 = pg.BarGraphItem(x=x,x1=x+5,y1=self.data[5],width=0.1, brush=(255, 0, 0))
        bg7 = pg.BarGraphItem(x=x,x1=x+6,y1=1-(((self.data[0]/self.totalTime)+(self.data[3]/(self.data[3]+self.data[4])))/2),width=0.1, brush=(255, 0, 0))
                   
        self.grafica.addItem(bg1)
        self.grafica.addItem(bg2)
        self.grafica.addItem(bg3)
        self.grafica.addItem(bg4)
        self.grafica.addItem(bg5)
        self.grafica.addItem(bg6)
        self.grafica.addItem(bg7)
        
    
    def initUI(self):
        
        self.nombre_video = ''
        self.data = [0,0,0,0,0,0]
        self.tabs = QTabWidget()
        self.tabIn = QWidget()
        self.tabs.addTab(self.tabIn,"Procesamiento")
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["TBA", "TBC", "TC", "EBA", "EBC", "EC","IA"])
        self.tableWidget.move(0,0)
        
        self.content = QHBoxLayout()
        self.content.addWidget(self.tableWidget)
    
        self.grafica = pg.PlotWidget(title="Resultados")
    
        self.content.addWidget(self.grafica)
        
        self.addItem(self.content)
        
        file = QtWidgets.QPushButton("Seleccionar archivo")
        file.clicked.connect(self.openFile)
        
        buttonBlue = QPushButton('Procesamiento')
        buttonBlue.clicked.connect(self.initProcesar)
        
        buttonE = QPushButton('Excel')
        buttonE.clicked.connect(self.toExcel)
         
        buttonR = QPushButton('Reproducir')
        buttonR.clicked.connect(self.initReproduccir)
        
        
        self.titleEdit_nom = QtWidgets.QLineEdit()
        self.titleEdit_nom.setDisabled(1)
        self.titleEdit_nom.setPlaceholderText("Selecciona un archivo") 
            
        self.b1 = QCheckBox("Tracker sheed")
        self.b1.setChecked(False)
        
        self.addWidget(self.b1)
        
        self.addWidget(self.titleEdit_nom)
        
        self.addWidget(file)
        self.addWidget(buttonR)
        self.addWidget(buttonBlue)
        self.addWidget(buttonE)
        
        
        
        