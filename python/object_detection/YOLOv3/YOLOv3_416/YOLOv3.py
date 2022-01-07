"""
@author: Ilker Atik
"""
import cv2
import numpy as np
from pathlib import Path

class YOLOv3:
    def __init__(self):
        self.base_path = Path(__file__).parent
        
        self.readLabels()
        self.createColorList()
        self.readModelAndLayers()
    def readLabels(self):
        label_file_path = (self.base_path / "model/labels.txt").resolve()
        label_file = open(label_file_path, 'r')
        self.labels = [word.replace('"','').replace("'",'') for word in label_file.read().split(',')]
        label_file.close()
        
    def createColorList(self):
        self.colors = ["0,255,0","0,0,255","255,0,0","0,120,30","0,30,120","50,50,50","50,0,50","50,50,100"]
        self.colors = [np.array(color.split(",")).astype("int") for color in self.colors]
        self.colors = np.array(self.colors)
        self.colors = np.tile(self.colors,(10,1)) #copying color list 10 times to fill the array with same numbers vertically
    
    def readModelAndLayers(self):
        model_file_path = (self.base_path / "model/").resolve()
        self.model = cv2.dnn.readNetFromDarknet(str(model_file_path/"yolov3.cfg"),str(model_file_path/"yolov3.weights"))
        self.layers = self.model.getLayerNames()
        self.output_layers = [self.layers[int(layer)-1] for layer in self.model.getUnconnectedOutLayers()]
    
    def detectObjects(self, frame):
        """
        Parameters
        ----------
        frame : image frame to detect objects on.

        Returns
        -------
        returns image with bounding boxes drawn and list of detections respectively.

        """
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        frame_blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), swapRB=True,crop=False)
        self.model.setInput(frame_blob)
        detection_layers = self.model.forward(self.output_layers)
    
        ids_list = []
        boxes_list = []
        confidences_list = []
        for detection_layer in detection_layers:
            for object_detection in detection_layer:
                scores = object_detection[5:]
                predicted_id = np.argmax(scores)
                confidence = scores[predicted_id]
                if confidence > 0.20: #draw bounding box if confidence is higher than ..
                    label = self.labels[predicted_id]
                    bounding_box = object_detection[0:4] * np.array([frame_width,frame_height,frame_width,frame_height])
                    (box_center_x, box_center_y,box_width, box_height) = bounding_box.astype("int")
    
                    start_x = int(box_center_x - (box_width/2))
                    start_y = int(box_center_y - (box_height/2))
    
                    ## non-maximum surpression step 1 ##
                    ids_list.append(predicted_id)
                    confidences_list.append(float(confidence))
                    boxes_list.append([start_x,start_y,int(box_width),int(box_height)])
                    ## non-maximum surpression step 1 ##
    
        ## non-maximum surpression step 2 ##
        max_ids = cv2.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)
        for max_id in max_ids:
            max_class_id = max_id[0]
            box = boxes_list[max_class_id]
            start_x = box[0]
            start_y = box[1]
            box_width = box[2]
            box_height = box[3]
    
            predicted_id = ids_list[max_class_id]
            self.label = self.labels[predicted_id]
            confidence = confidences_list[max_class_id]
        ## non-maximum surpression step 2 ##
    
            end_x = start_x + box_width
            end_y = start_y + box_height
    
            box_color = self.colors[predicted_id]
            box_color = [int(each) for each in box_color]
    
            label = "{}: {:.2f}%".format(label,confidence*100)
            #print("predicted object: {}".format(label))
    
            cv2.rectangle(frame, (start_x, start_y),(end_x, end_y),box_color,2)
            cv2.putText(frame, label, (start_x, start_y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color,1)
        
        return frame, max_ids
            
            
            
            
            
            