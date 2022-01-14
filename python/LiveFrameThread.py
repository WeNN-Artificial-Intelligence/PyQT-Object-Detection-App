# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 17:54:58 2022

@author: atik_
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from object_detection.YOLOv5.YOLOv5 import *
from object_detection.YOLOv3.YOLOv3_416.YOLOv3 import *
class LiveFrameThread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    yoloV3Instance = YOLOv3() # default
    methodInstance = yoloV3Instance
    def run(self):
        self.ThreadActive = True
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 0 is the system webcam
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
             frame = cv2.flip(frame,1)
             frame = self.methodInstance.detectObjects(frame)
             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             convertToQtFormat = QImage(image.data, image.shape[1],image.shape[0], QImage.Format_RGB888)
             pic = convertToQtFormat.scaled(832,560, Qt.KeepAspectRatio)
             self.ImageUpdate.emit(pic) #sends a message to mainWindow class
        capture.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()