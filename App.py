# Dependencies
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QSystemTrayIcon
from PyQt5.QtGui import QIcon
from tabs.MainTabs import MainTabs

class App(QMainWindow):
    
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ANALYXITY')
        self.setWindowIcon(QIcon('1.png')) 
        self.setGeometry(100, 90, 1200, 600)
        self.table_widget = MainTabs(self)
        self.setCentralWidget(self.table_widget)
        self.show()
        self.systray = QSystemTrayIcon(QIcon("1.png"), self)
        self.systray.show()
        self.systray.showMessage("ANALIXITY","INICIALIZANDO")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())