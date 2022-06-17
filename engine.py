import cv2
import time
import math 
import serial

def getCenterPoint(minPoint, maxPoint):
	return [int((maxPoint[0] + minPoint[0])/2), int((maxPoint[1] + minPoint[1])/2)]

def getPerimeter(data):
	# data[0] = xmin
	# data[1] = ymin
	# data[2] = xmax
	# data[3] = ymax
	return abs(int((data[2] - data[0])) * 2 + abs((data[3] - data[1])) * 2)

def drawFocus(img, centerPoint, dispW, dispH, distanceThreshold):
	cv2.circle(img, (centerPoint[0], centerPoint[1]), 1, (0, 255, 0), 8)
	cv2.line(img, (0, centerPoint[1]), (dispW, centerPoint[1]), (0, 255, 0), 2)
	cv2.line(img, (centerPoint[0], 0), (centerPoint[0], dispH), (0, 255, 0), 2)
	cv2.circle(img, (int(dispW / 2), int(dispH / 2)), distanceThreshold, (0, 0, 255), 4)
	cv2.line(img, (centerPoint[0], centerPoint[1]), (int(dispW / 2), int(dispH / 2)), (0, 255, 0), 4)
	return img

def getFPS(img, pTime):
	cTime = time.time()
	fps = 1 / (cTime - pTime)
	pTime = cTime
	cv2.putText(img, f'{int(fps)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
				(255, 0, 0), 5)
	return img, pTime

def checkDetection(isDetection, img, centerPoint, dispW, dispH, distanceThreshold):
	if isDetection:
		img = drawFocus(img, centerPoint, dispW, dispH, distanceThreshold)
		distance = getDistance(centerPoint, [int(dispW / 2), int(dispH / 2)])
		# print(distance)
		if distance > distanceThreshold:
			# print("Tracking !!!!!")
			pass
	else:
		# print("Nothing!!!")
		pass
	return img

def getDistance(point1, point2):
	return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))

def controllerServo(midpoint, centerPoint,distanceThreshold, isDetection):
	if isDetection:
		# LR, UD -1, 1
		# 2, 1 (2 = -1)
		if getDistance(midpoint, centerPoint) > distanceThreshold:
			if centerPoint[0] < midpoint[0] and centerPoint[1] < midpoint[1]:
				return 2, 2
			elif centerPoint[0] > midpoint[0] and centerPoint[1] < midpoint[1]:
				return 1, 2
			elif centerPoint[0] < midpoint[0] and centerPoint[1] > midpoint[1]:
				return 2, 1
			elif centerPoint[0] > midpoint[0] and centerPoint[1] > midpoint[1]:
				return 1, 1
			else:
				return 0, 0
		else:
			return 0, 0
	else:
		return 0, 0

def initConnection(portNo, baudRate):
	try:
		ser = serial.Serial(portNo, baudRate)
		print("Device Connected")
		return ser
	except:
		print("Not Connected")

def sendData(se, data, digits):
	myString = "$"
	for d in data:
		myString += str(d).zfill(digits)
	try:
		se.write(myString.encode())
		print(myString)
	except:
		print("Data Transmission Failed")

if __name__ == '__main__':
	ser = initConnection("COM4", 9600)  
	while True:
		sendData(ser, [0, 0], 3)
		time.sleep(3)
		sendData(ser, [180, 180], 3)
		time.sleep(3)