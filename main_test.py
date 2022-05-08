import cv2
import sys
import torch
import time
sys.path.insert(1, 'Fire-Tracking')
sys.path.insert(2, 'Face-Recognition')
from load_custom_model import loadCustomModel
from detection import fireDetection
from face_recognition_module import myFaceRecognition, getInitialValue, collectingData, startCollectingData
from engine import drawFocus, getFPS, getDistance, checkDetection, controllerServo, initConnection, sendData

FIRE_TRACKING_PATH = 'Fire-Tracking'
FACE_RECOGNITION_PATH = 'Face-Recognition'

model = loadCustomModel(path=f'{FIRE_TRACKING_PATH}/best.pt', conf=0.55, iou=0.7)
# model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

PORT = "COM4"
# ser = initConnection("COM4", 9600)  
numOfSample, currentSample, currentMember, encodeListKnown, classNames = getInitialValue(path=FACE_RECOGNITION_PATH)
state = 0
dispW=640
dispH=480
flip=4
pTime = 0
camSet = 0
# camSet='nvarguscamerasrc wbmode=1 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=20/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=2 brightness=-.1 saturation=1.2 ! appsink'
distanceThreshold = 100
cap = cv2.VideoCapture(camSet)

while(True):
	success, img = cap.read()

	img = cv2.flip(img, flip)

	img, pTime = getFPS(img, pTime)

	img, minPoint, maxPoint, centerPoint, isDetection = fireDetection(img, model)
	img = checkDetection(isDetection, img, centerPoint, dispW, dispH, distanceThreshold)
	

	cv2.imshow('YOLO', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print("Stop Camera !!")
		time.sleep(2)
		break
  
cap.release()
cv2.destroyAllWindows()