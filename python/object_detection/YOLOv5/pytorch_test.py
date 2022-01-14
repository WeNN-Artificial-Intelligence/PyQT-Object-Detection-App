import torch
# Model

model = torch.hub.load('./', 'custom', path='visdrone416Best.pt', source='local')  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = '0000303_00401_d_0000185.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)
# Results
results.save()