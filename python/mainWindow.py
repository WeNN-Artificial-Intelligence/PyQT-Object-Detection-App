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

from object_detection.YOLOv3.YOLOv3_416.YOLOv3 import *

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
        
        self.stopBtn.clicked.connect(self.stopFeed)
        self.startBtn.clicked.connect(self.startFeed)

        self.worker1 = Worker1()
        
        self.worker1.ImageUpdate.connect(self.imageUpdateSlot)
    
    def imageUpdateSlot(self,img):
        self.streamLabel.setPixmap(QPixmap.fromImage(img))
        
    def startFeed(self):
        self.worker1.start()
        
    def stopFeed(self):
        self.worker1.stop()
        
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    yoloInstance = YOLOv3()
    def run(self):
        self.ThreadActive = True
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 0 is the system webcam
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                frame = cv2.flip(frame,1)
                frame, res = self.yoloInstance.detectObjects(frame)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(image.data, image.shape[1],image.shape[0], QImage.Format_RGB888)
                pic = convertToQtFormat.scaled(832,560, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic) #sends a message to mainWindow class
        capture.release()
    def stop(self):
        self.ThreadActive = False
        self.quit()
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    App.exec_()
    
