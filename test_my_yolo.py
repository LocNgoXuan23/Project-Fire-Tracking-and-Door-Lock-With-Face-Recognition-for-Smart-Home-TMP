import cv2
import torch
# from load_custom_model import loadCustomModel
import numpy as np
import time

# model = loadCustomModel(path='best.pt', conf=0.4, iou=0.7)
# model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
model = torch.hub.load('ultralytics/yolov5', 'custom', path="yolov5n.pt")
dispW=640
dispH=480
flip=4
pTime = 0
camSet = 0
cap = cv2.VideoCapture(camSet)

def drawFocus(img, minPoint, maxPoint):
    print(minPoint, maxPoint)
    center = [int((maxPoint[0] + minPoint[0])/2), int((maxPoint[1] + minPoint[1])/2)]
    cv2.circle(img, (center[0], center[1]), 1, (0, 255, 0), 8)
    cv2.line(img, (0, center[1]), (dispW, center[1]), (0, 255, 0), 2)
    cv2.line(img, (center[0], 0), (center[0], dispH), (0, 255, 0), 2)
    cv2.circle(img, (int(dispW / 2), int(dispH / 2)), 1, (0, 0, 255), 8)
    cv2.line(img, (center[0], center[1]), (int(dispW / 2), int(dispH / 2)), (0, 255, 0), 4)
    return img

def predictImg(img):
    img = img[..., ::-1]
    results = model(img)
    datas = results.pandas().xyxy[0].values.tolist()
    img = np.squeeze(results.render())[..., ::-1]
    img = np.array(img)

    if len(datas) != 0:
        max_perimeter = 0
        minPoint, maxPoint = [0, 0], [0, 0]
        for data in datas:
            perimeter = int((data[2] - data[0]) * 2 + (data[3] - data[1]) * 2)
            if perimeter > max_perimeter:
                max_perimeter = perimeter
                minPoint, maxPoint = [int(data[0]), int(data[1])], [int(data[2]), int(data[3])]
        img = drawFocus(img, minPoint, maxPoint)
    else: 
        print("No Detection !!!!")

    return img

def getFPS(img, pTime):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'{int(fps)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
    return img, pTime

while(True):
    success, img = cap.read()

    img = cv2.flip(img, flip)

    img, pTime = getFPS(img, pTime)

    img = predictImg(img)

    cv2.imshow('YOLO', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cap.release()
cv2.destroyAllWindows()

