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
ser = initConnection("COM4", 9600)  
numOfSample, currentSample, currentMember, encodeListKnown, classNames = getInitialValue(path=FACE_RECOGNITION_PATH)
state = 0
dispW=640
dispH=480
flip=4
pTime = 0
camSet = 0
distanceThreshold = 100
cap = cv2.VideoCapture(camSet)

while(True):
	success, img = cap.read()

	img = cv2.flip(img, flip)

	img, pTime = getFPS(img, pTime)

	'''CHECK STATE'''
	# Fire Detection
	if state == 0:
		img, minPoint, maxPoint, centerPoint, isDetection = fireDetection(img, model)
		img = checkDetection(isDetection, img, centerPoint, dispW, dispH, distanceThreshold)
		LR, UD = controllerServo([int(dispW / 2), int(dispH / 2)], centerPoint, distanceThreshold, isDetection)
		sendData(ser, [LR, UD, 0], 3)
	# Face Detection
	if state == 1:
		img, minPoint, maxPoint, centerPoint, isDetection, isTrueFace = myFaceRecognition(img, encodeListKnown, classNames)
		img = checkDetection(isDetection, img, centerPoint, dispW, dispH, distanceThreshold)
		LR, UD = controllerServo([int(dispW / 2), int(dispH / 2)], centerPoint, distanceThreshold, isDetection)
		isOpen = 0
		if (isTrueFace):
			isOpen = 1
		sendData(ser, [LR, UD, isOpen], 3)

	# CollectingData
	if state == 2:
		currentMember, currentSample, numOfSample, state, encodeListKnown, classNames = collectingData(img, currentMember, currentSample, numOfSample, state, encodeListKnown, classNames, path=FACE_RECOGNITION_PATH)

	'''EVENT'''
	# Start Data Collection
	if cv2.waitKey(1) & 0xFF == ord('2'):
		if state != 2:
			state = 2
			print("Start Data Collection")
			time.sleep(2)
			currentMember = startCollectingData(currentMember, path=FACE_RECOGNITION_PATH)

	# Start Face Recognition
	if cv2.waitKey(1) & 0xFF == ord('1'):
		if state != 1:
			state = 1
			print("Start Face Recognition")
			time.sleep(2)

	# Start Fire Detection
	if cv2.waitKey(1) & 0xFF == ord('0'):
		if state != 0:
			state = 0
			print("Start Fire Detection")
			time.sleep(2)

	cv2.imshow('YOLO', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print("Stop Camera !!")
		time.sleep(2)
		break
  
cap.release()
cv2.destroyAllWindows()