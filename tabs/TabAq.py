# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author:
"""
#imports native
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QHBoxLayout, QFileDialog)
import pyqtgraph as pg
#módulos que se implementan
from PyQt5.QtGui import (QPixmap,QImage,QLCDNumber)#QSystemTrayIcon,QIcon,QRect
from PyQt5.QtCore import (Qt, QSize, QTimer)
#from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from time import strftime
#lobrerías que se utilizan
import cv2,threading
from PyQt5 import QtGui

class TabAq(QHBoxLayout):
    
    def __init__(self):      
        super().__init__()
        self.initUI()
#--------------------------------funciónES-----------------------------------     
#   funcion Selección_camara
    def setup_camera(self,opCam=0):
        self.setup_camera_status = True
        #Inicialización_de_camara
        self.capture = cv2.VideoCapture(opCam)
        self.capture.set(cv2.CAP_PROP_FOCUS,0.0)
        #Medidas
        self.capture.set(3, self.video_size.width())
        self.capture.set(4, self.video_size.height())
        self.save = False
        #Tramas
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(41.666)
                
#   función Previsualizar_Video
    def display_video_stream(self):
        #Leer el frame de la camra y proyectarlo 
        _, self.frame = self.capture.read()
        if(self.save == True):
            self.out.write(self.frame)
            
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)#colores_RGB
        self.frame = cv2.flip(self.frame, 1)#girar_imagen
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],# 
                       self.frame.strides[0], QImage.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(image))
        
#   función Detener_Video 
    def stop(self):
        self.display_video_stream.stop()   
        
#   función Inicializar_Video
    def cargar_video(self):
        #Variable para parte de video
       self.video = QtWidgets.QLabel()
       self.video.setFixedSize(self.video_size) 
       
    def openFile(self):
        self.nombre_video = ''
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"Selecciona...", "","AVI Files (*.avi)", options=options)
        if fileName:
            self.nombre_video = fileName
            self.titleEdit_nom.setText(fileName)
            
           
    
#  función Slider_Brillo                       
    def changedBrightnessValue(self,value):
        #brightness = (value - 0)/(255 - 0)
        brightness = (value - 0)
        #print (brightness) 
        self.capture.set(10,brightness)

#  función Slider_Contraste                                  
    def changedContrastValue(self,value):
        contrast = (value - 0)
        #print (contrast) 
        self.capture.set(cv2.CAP_PROP_CONTRAST,contrast)
        
#  función Slider_Contraste                                  
    def changedSaturationValue(self,value):
        saturation = (value - 0)
        #print (saturation) 
        self.capture.set(cv2.CAP_PROP_SATURATION,saturation)        
        
#  función Slider_Ganancia                                
    def changedGainValue(self,value):
        gain = (value - 0)
        #print (gain) 
        self.capture.set(cv2.CAP_PROP_GAIN,gain)

#   función Guardar_Video
    def save_video(self):
        #inicialia min y seg de LCD
        if self.setup_camera_status:
            if self.nombre_video:
                if self.titleEdit_time.text() and self.titleEdit_time.text() != '': 
                    #print(self.titleEdit_time.text())
                    set_time = (self.titleEdit_time.text()).split(':')
                    self.minutos = set_time[0]
                    self.segundos = set_time[1]
                    if self.segundos != '00':                   
                        self.seg=0
                        self.min=0
                        #asignación_de_tiempo_del_video_&_split
                        #print(set_time)
                        #print(self.minutos)
                        #print(self.segundos)
                        #muestra_tiempo(LCD)_formato
                        self.lcd.display(strftime(str(self.min)+":"+str(self.seg)))
                        #inicializa_tiempo
                        self.Time()
                        #inicializa_la_escritura_y_guardado_de_tramas
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        #asignación_nombre_del_video_(.avi)_con_Resol(640x480)
                        self.out = cv2.VideoWriter( self.nombre_video,fourcc, 24, (640,480))
                        self.save = True;
                    else:    
                        QtGui.QMessageBox.critical(None, "Alerta","Tiempo invalido",QtGui.QMessageBox.Ok)
                else:
                    QtGui.QMessageBox.critical(None, "Alerta","No has introduccido el tiempo",QtGui.QMessageBox.Ok)
            else:
                QtGui.QMessageBox.critical(None, "Alerta","No has Seleccionado un Archivo",QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.critical(None, "Alerta","No has iniciado la camara",QtGui.QMessageBox.Ok)
        
#   función Tiempo    
    def Time(self):
        #inicialización_hilo
        self.t=threading.Timer(1.0, self.Time)
        self.t.start()
        #comparación_tiempo_asignado_con_el_transcurrido
        if( (self.seg==(int(self.segundos))) & (self.min==(int(self.minutos)))):
            self.stop_threading()#detener_hilo
        #muestra_tiempo(LCD)_formato    
        self.lcd.display(strftime(str(self.min)+":"+str(self.seg)))
        #incremento_min_y_seg
        self.seg=self.seg+1
        if (self.seg==60):
            self.seg=00
            self.min=self.min+1
                      
#   función Detener_Video            
    def stop_threading(self):
        if self.setup_camera_status:
            self.t.cancel()#cancela_hilo
            self.save = False;#detener_guardado_de_video
            self.out.release();

#   función Split_Resolusión        
    def onResol(self,text):
        #print(text)
        divide = text.split('X')
        #print(divide)
        self.ancho = divide[0]
        #print(self.ancho)
        self.alto = divide[1]
        #print(self.alto)
                
#   función Asignar_nombre_video             
    def nombrar(self,text_nomb):
        self.nombre_video = text_nomb
        
#   funcion reproducir_video
    def reproducir_video_3(self):
        self.video3 = cv2.VideoCapture('LE07.wmv')
        cont=0
        while(self.video3.isOpened()):
            #print(cont)
            ret, self.frame_3 = self.video3.read()
            #print('leido')
#            gray = cv2.cvtColor(frame_3, cv2.COLOR_BGR2GRAY)
#            kernelTam = (25,25)
#            grayBlur = cv2.GaussianBlur(gray, kernelTam, 0)
#            _, thresh = cv2.threshold(grayBlur, 170, 255, cv2.THRESH_BINARY) 
            #print(type(self.frame_3))
            image_3 = QImage(self.frame_3,self.frame_3.shape[1],self.frame_3.shape[0], 
                       self.frame_3.strides[0], QImage.Format_RGB888)
            #print('qimage')
            self.video_3.setPixmap(QPixmap.fromImage(image_3)) 
            #print('en pixmap')
            cv2.waitKey(1)
            cont=cont+1
        

 #   función Inicializar_Video
    def cargar_video_3(self):
        #Variable para parte de video
       self.video_3 = QtWidgets.QLabel("Hola")
       self.video_3.setFixedSize(self.video_size_3)
            
    def initUI(self):
        self.nombre_video = ''
        self.setup_camera_status = False
        logo = QtWidgets.QLabel()
        logo.setGeometry(100, 90, 400, 412)
        logo.setPixmap(QPixmap("./tabs/1.png"))
        
        
#   Creación_de_botones,funciones y características [CONTENEDOR Contenido_2/MEDIA/GBOTONES] 
        b_video = QtWidgets.QPushButton("VIDEO")
        b_video.clicked.connect(self.setup_camera)
        b_iniciar = QtWidgets.QPushButton("INICIAR")
        b_iniciar.clicked.connect(self.save_video)
        
        b_terminar = QtWidgets.QPushButton("TERMINAR")
        b_terminar.clicked.connect(self.stop_threading)
        
        b_video.setFixedWidth(100)
        b_iniciar.setFixedWidth(100)
        b_terminar.setFixedWidth(100)
                
        #creción de Sliders y etiquetas [CONTENEDOR CONTROLES/CONTROL*]
        eti_controles = QtWidgets.QLabel("CONTROLES")
        
        #BRILLO       
        brillo = QtWidgets.QSlider(Qt.Horizontal)
        eti_brillo = QtWidgets.QLabel("BRILLO")
        brillo.setFixedWidth(200)
        brillo.valueChanged[int].connect(self.changedBrightnessValue)#función asosiada al mov
        brillo.setMaximum(255)
        
        #CONTRASTE
        contraste = QtWidgets.QSlider(Qt.Horizontal)
        eti_contraste = QtWidgets.QLabel("CONTRASTE")
        contraste.setFixedWidth(200)
        contraste.valueChanged[int].connect(self.changedContrastValue)#función asosiada al mov
        contraste.setMaximum(255)
        
        #SATURACIÓN
        saturacion = QtWidgets.QSlider(Qt.Horizontal)
        eti_saturacion = QtWidgets.QLabel("SATURACIÓN")
        saturacion.setFixedWidth(200)
        saturacion.valueChanged[int].connect(self.changedSaturationValue)#función asosiada al mov
        saturacion.setMaximum(255)
        
        #GANANCIA        
        ganancia = QtWidgets.QSlider(Qt.Horizontal)
        eti_gain = QtWidgets.QLabel("GANANCIA")
        ganancia.setFixedWidth(200)
        ganancia.valueChanged[int].connect(self.changedGainValue)#función asosiada al mov
        ganancia.setMaximum(255)
#______________________________________________________-        
        #CONTENEDOR CONTROL/ARCHIVO*
        self.titleEdit_nom = QtWidgets.QLineEdit()
        self.titleEdit_nom.setFixedWidth(200)
        self.titleEdit_nom.setDisabled(1)
        self.titleEdit_nom.setPlaceholderText("Selecciona un archivo") 
        title_nom = QtWidgets.QLabel('NOMBRE :')
#__________________________________________________
        self.titleEdit_time = QtWidgets.QLineEdit()
        title_time = QtWidgets.QLabel('TIEMPO :')
        self.titleEdit_time.setPlaceholderText("00:00") 
        self.titleEdit_time.setFixedWidth(200)

        #cronometro
        self.t= []
#        self.lcd = QtGui.QLCDNumber(self)
        self.lcd = QLCDNumber()
        self.lcd.resize(250,100)
        self.lcd.setFixedWidth(100)
        self.minutos=0
        self.segundos=0
        self.min=0
        self.seg=0
        tiempo = QtWidgets.QFormLayout()
        tiempo.addWidget(self.lcd)
        tiempo.addWidget(title_time)
        tiempo.addWidget(self.titleEdit_time)        
#______________________________________________________
        #Se crea los contenedores Contenido_2 - MEDIA - CONTROLES .ARCHIVO
        Contenido_2 = QtWidgets.QHBoxLayout()        
        media = QtWidgets.QVBoxLayout()
        
        #Cuadro de bonotnes dentro de media
        Gbotones = QtWidgets.QHBoxLayout()
        control = QtWidgets.QFormLayout()
        controles = QtWidgets.QVBoxLayout()
        archivo = QtWidgets.QFormLayout()
        #archivo_3ar camara
        selec_cam = QtWidgets.QFormLayout()
        # Tamaño de pantalla de video
        self.video_size = QSize (640, 480)
        #Creacion se componentes
        Gbotones.addWidget(b_video)        
        Gbotones.addWidget(b_iniciar)
        Gbotones.addWidget(b_terminar)
        
        file = QtWidgets.QPushButton("Seleccionar archivo")
        file.clicked.connect(self.openFile)
        Gbotones.addWidget(file)
    
        #Componentes que se agregan a media y acontroles    
        self.cargar_video()
        media.addWidget(self.video)
        media.addLayout(Gbotones) 
       
        control.addWidget(eti_controles)
        control.addRow(eti_brillo,brillo)
        control.addRow(eti_contraste,contraste)
        control.addRow(eti_saturacion,saturacion)
        control.addRow(eti_gain,ganancia)

        archivo.addWidget(title_nom)
        archivo.addWidget(self.titleEdit_nom)

        
        #archivo_3 DE LA CAMARA COMBO BOX
        cameras=np.zeros(10)
        cont=0;
        for i in range(10):
            capture = cv2.VideoCapture(i)
            if (capture.isOpened()):
                cameras[cont]=1
                cont=cont+1
        cam=int(sum(cameras))
        
        self.combo_cam = QtWidgets.QComboBox()
        for i in range(cam):
            self.combo_cam.addItem("Camara " + str(i))
# -------------------------------------------------------****************************
        self.combo_cam.activated[int].connect(self.setup_camera)
# -------------------------------------------------------**************************** 
        #combo box de resolución
        self.combo_resol = QtWidgets.QComboBox()
        self.resol = ["1280 X 720","640 X 480","320 X 240"]
        self.combo_resol.activated[str].connect(self.onResol) 
        self.ancho=640
        self.alto=480
        self.combo_resol.addItems(self.resol)
        

        #etiquetas de selec_cam
        eti_cam= QtWidgets.QLabel("Selección: ")
        #etiquetas de selec_resol
        eti_resol= QtWidgets.QLabel("Resolución: ")
            

        #self.combo_cam.move(50, 50)
        selec_cam.addWidget(eti_cam)      
        selec_cam.addWidget(self.combo_cam)
        selec_cam.addWidget(eti_resol)
        selec_cam.addWidget(self.combo_resol)
        
        #contenedor Controles 
        controles.addLayout(control)
        controles.addLayout(selec_cam)
        controles.addLayout(tiempo)
        controles.addLayout(archivo)
    
        #Se agregan contenedores de media izq y contenedor de controles der
        
        #Contenido_2.addLayout(media)
        #Contenido_2.addLayout(controles)
        
        #Se agrega a tab2 que es la principal Contenido_2
        
        logo = QtWidgets.QLabel()
        logo.setGeometry(100, 90, 400, 412)
        logo.setPixmap(QPixmap("./tabs/1.png"))
        self.addWidget(logo)

        self.addLayout(media)
        self.addLayout(controles)