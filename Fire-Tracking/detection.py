import numpy as np
import cv2
import sys
sys.path.insert(1, '..')
from engine import getPerimeter, getCenterPoint
from load_custom_model import loadCustomModel

def fireDetection(img, model):
    img = img[..., ::-1]
    results = model(img)
    datas = results.pandas().xyxy[0].values.tolist()
    img = np.squeeze(results.render())[..., ::-1]
    img = np.array(img)

    if len(datas) != 0:
        max_perimeter = 0
        minPoint, maxPoint = [0, 0], [0, 0]
        for data in datas:
            perimeter = getPerimeter(data)
            # perimeter = int((data[2] - data[0]) * 2 + (data[3] - data[1]) * 2)
            if perimeter > max_perimeter:
                max_perimeter = perimeter
                minPoint, maxPoint = [int(data[0]), int(data[1])], [int(data[2]), int(data[3])]
        # centerPoint = [int((maxPoint[0] + minPoint[0])/2), int((maxPoint[1] + minPoint[1])/2)]
        centerPoint = getCenterPoint(minPoint, maxPoint)
        return img, minPoint, maxPoint, centerPoint, True
    else: 
        # print("No Detection !!!!")
        return img, None, None, None, False

    