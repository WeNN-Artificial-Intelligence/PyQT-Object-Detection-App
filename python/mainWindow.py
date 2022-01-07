"""
Created on Fri Jan  7 21:19:43 2022

@author: Ilker Atik
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        self.feedLabel = QLabel()
        self.VBL.addWidget(self.feedLabel)
        
        self.cancelBTN = QPushButton("Cancel")
        self.cancelBTN.clicked.connect(self.cancelFeed)
        self.VBL.addWidget(self.cancelBTN)
        
        self.worker1 = Worker1()
        self.worker1.start()
        self.worker1.ImageUpdate.connect(self.imageUpdateSlot)
        self.setLayout(self.VBL)
    
    def imageUpdateSlot(self,img):
        self.feedLabel.setPixmap(QPixmap.fromImage(img))
    
    def cancelFeed(self):
        self.Worker1.stop()
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        capture = cv2.VideoCapture(0) # 0 is the system webcam
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_image = cv2.flip(image,1)
                convertToQtFormat = QImage(flipped_image.data, flipped_image.shape[1],flipped_image.shape[0], QImage.Format_RGB888)
                pic = convertToQtFormat.scaled(720,480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic) #sends a message to mainWindow class
    def stop():
        self.ThreadActive = False
        self.quit()
if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    #App.exec_()
    
