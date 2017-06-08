# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:01:20 2017

@author: 
"""
#imports native
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
# Custom Dependencies
from tabs.TabIn import TabIn
from tabs.TabIm import TabIm
from tabs.TabAq import TabAq
from tabs.TabPr import TabPr
from tabs.TabRe import TabRe

class MainTabs(QWidget):
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabIn = QWidget()
        self.tabIm = QWidget()
        self.tabAq = QWidget()
        self.tabPr = QWidget()
        self.tabGr = QWidget()
        self.tabRe = QWidget()
        
        # Content Tabs
        self.tabInLayout = TabIn()
        self.tabImLayout = TabIm()
        self.tabAqLayout = TabAq()
        self.tabPrLayout = TabPr()
        self.tabReLayout = TabRe()
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tabIn,"INICIO")
        self.tabs.addTab(self.tabAq,"ADQUISICÓN")
        self.tabs.addTab(self.tabRe,"AREAS")
        self.tabs.addTab(self.tabPr,"PROCESAMIENTO")
        self.tabs.addTab(self.tabIm,"RESULTADOS")
 
        # Set asing layout
        self.tabIn.layout = self.tabInLayout
        self.tabIm.layout = self.tabImLayout
        self.tabAq.layout = self.tabAqLayout
        self.tabPr.layout = self.tabPrLayout
        self.tabRe.layout = self.tabReLayout
        
        # SetLayout Tabs
        self.tabIn.setLayout(self.tabIn.layout)
        self.tabAq.setLayout(self.tabAq.layout)
        self.tabPr.setLayout(self.tabPr.layout)
        self.tabRe.setLayout(self.tabRe.layout)
        self.tabIm.setLayout(self.tabIm.layout)
 
        # Add tabs to Main
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)