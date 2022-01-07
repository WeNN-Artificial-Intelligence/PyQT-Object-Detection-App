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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        loadUi("../ui/mainWindow.ui",self)
        
        ##define
        self.stopBtn = self.findChild(QPushButton, "stopPushButton")
        self.startBtn = self.findChild(QPushButton, "startPushButton")
        self.detectionsListView = self.findChild(QListView, "detectionDetailListView")
        self.detectionDetailListView = self.findChild(QListView, "detectionDetailListView")
        self.streamLabel = self.findChild(QLabel, "streamLabel")
        
        self.stopBtn.clicked.connect(self.stopFeed)
        self.startBtn.clicked.connect(self.startFeed)
#        self.VBL = QVBoxLayout()
        
 #       self.feedLabel = QLabel()
  #      self.VBL.addWidget(self.feedLabel)
        
   #     self.cancelBtn = QPushButton("Cancel")
        
    #    self.VBL.addWidget(self.cancelBTN)
        
        self.worker1 = Worker1()
        
        self.worker1.ImageUpdate.connect(self.imageUpdateSlot)
     #   self.setLayout(self.VBL)
    
    def imageUpdateSlot(self,img):
        self.streamLabel.setPixmap(QPixmap.fromImage(img))
    def startFeed(self):
        self.worker1.start()
    def stopFeed(self):
        self.worker1.stop()
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 0 is the system webcam
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_image = cv2.flip(image,1)
                convertToQtFormat = QImage(flipped_image.data, flipped_image.shape[1],flipped_image.shape[0], QImage.Format_RGB888)
                pic = convertToQtFormat.scaled(720,480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic) #sends a message to mainWindow class
        capture.release()
    def stop(self):
        self.ThreadActive = False
        self.quit()
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    #App.exec_()
    
