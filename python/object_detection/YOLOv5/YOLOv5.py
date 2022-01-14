# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 16:21:12 2022

@author: atik_
"""
import torch
from pathlib import Path
import sys

class YOLOv5:
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        model_file_path = (self.base_path).resolve()
        sys.path.insert(0, model_file_path)
        print(model_file_path)
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        #self.model = model = torch.hub.load(model_file_path , 'custom', path=str(model_file_path/'visdroneSmall832.pt'), source='local', force_reload=True) 
        
    def detectObjects(self, frame):
         result = self.model(frame)
         result.render()  # updates results.imgs with boxes and labels
         return result.imgs[0]