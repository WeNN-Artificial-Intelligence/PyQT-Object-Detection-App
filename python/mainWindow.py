"""
Created on Fri Jan  7 21:19:43 2022

@author: Ilker Atik
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import *
import cv2

from object_detection.YOLOv5.YOLOv5 import *
from object_detection.YOLOv3.YOLOv3_416.YOLOv3 import *

from LiveFrameThread import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        loadUi("../ui/mainWindow.ui",self)
        self.setWindowTitle("WeNN")
        ##define
        self.stopBtn = self.findChild(QPushButton, "stopPushButton")
        self.startBtn = self.findChild(QPushButton, "startPushButton")
        self.detectionsListView = self.findChild(QListView, "detectionDetailListView")
        self.detectionDetailListView = self.findChild(QListView, "detectionDetailListView")
        self.streamLabel = self.findChild(QLabel, "streamLabel")
        self.modelComboBox = self.findChild(QComboBox, "modelComboBox")
        
        self.stopBtn.clicked.connect(self.stopFeed)
        self.startBtn.clicked.connect(self.startFeed)

        self.liveFrameThread = LiveFrameThread()
        
        self.liveFrameThread.ImageUpdate.connect(self.imageUpdateSlot)
    
    def imageUpdateSlot(self,img):
        self.streamLabel.setPixmap(QPixmap.fromImage(img))
        
    def startFeed(self):
        selectedModel = self.modelComboBox.currentText()
        if(selectedModel == "YOLOv3"):
            self.liveFrameThread.methodInstance = YOLOv3()
            print("annen")
        elif (selectedModel == "YOLOv5"):
            self.liveFrameThread.methodInstance = YOLOv5()
            print("bab")
        elif(selectedModel == "YOLOv5 UYZ Custom Model"):
            self.liveFrameThread.methodInstance = YOLOv5()
            print("wwe")
        self.liveFrameThread.start()
        
    def stopFeed(self):
        self.liveFrameThread.stop()
        

        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    App.exec_()
    
