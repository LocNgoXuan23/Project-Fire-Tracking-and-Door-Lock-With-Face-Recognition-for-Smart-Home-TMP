import cv2
import numpy as np
import face_recognition
import os
import time
import sys
sys.path.insert(1, '..')
from my_utils import getConfig, updateConfig
from handle_encode_data import getEncodeList
from engine import getPerimeter, getCenterPoint, checkDetection

def getInitialValue(numOfSample = 5, currentSample = 0, path=''):
	numOfSample = numOfSample
	currentSample = currentSample
	currentMember = getConfig(path=path)['currentMember']
	encodeListKnown, classNames = getEncodeList(path=path)

	return numOfSample, currentSample, currentMember, encodeListKnown, classNames

def myFaceRecognition(img, encodeListKnown, classNames):
	imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
	imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

	facesCurFrame = face_recognition.face_locations(imgS)
	encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
	max_perimeter = 0
	minPoint, maxPoint = [0, 0], [0, 0]

	isTrueFace = False

	if len(facesCurFrame) != 0:
		for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
			name = 'Undefine'
			# Check EncodeListKnown empty
			if len(encodeListKnown) != 0:
				matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
				faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
				matchIndex = np.argmin(faceDis)

				if matches[matchIndex]:
					name = classNames[matchIndex].upper()
					print(name)
				else:
					name = 'Undefine'
					print(name)
			else:
				name = 'Undefine'
				print("No Data !!")

			y1, x2, y2, x1 = faceLoc
			y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
			cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
			cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
			perimeter = getPerimeter([x1, y1, x2, y2])
			if perimeter > max_perimeter:
				max_perimeter = perimeter
				minPoint, maxPoint = [x1, y1], [x2, y2]
				if name != 'Undefine':
					isTrueFace = True
		
		centerPoint = getCenterPoint(minPoint, maxPoint)
		cv2.circle(img, (centerPoint[0], centerPoint[1]), 1, (0, 255, 0), 8)

		return img, minPoint, maxPoint, centerPoint, True, isTrueFace
	else:
		return img, None, None, None, False, isTrueFace

def collectingData(img, currentMember, currentSample, numOfSample, state, encodeListKnown, classNames, path=''):
	newPath = os.path.join(path, 'data', f'member_{currentMember - 1}', f'{currentSample}.member_{currentMember - 1}.png')
	cv2.imwrite(newPath, img)
	print(f'Read Sample {currentSample}')
	time.sleep(1)
	currentSample += 1
	if currentSample == numOfSample:
		currentSample = 0
		state = 0
		encodeListKnown, classNames = getEncodeList(path=path)
	
	return currentMember, currentSample, numOfSample, state, encodeListKnown, classNames

def startCollectingData(currentMember, path=''):
	newPath = os.path.join(path, 'data', f'member_{currentMember}')
	if os.path.exists(newPath):
		pass
	else:
		os.mkdir(newPath)
		updateConfig(path=path)
		currentMember = getConfig(path=path)['currentMember']
		print(f'currentMember: {currentMember}')
	return currentMember

# if __name__ == '__main__':
# 	state, numOfSample, currentSample, currentMember, encodeListKnown, classNames = getInitialValue()
# 	cap = cv2.VideoCapture(0)

# 	while True:
# 		success, img = cap.read()

# 		# Face Recognition
# 		if state == 0:
# 			img = myFaceRecognition(img, encodeListKnown, classNames)
			
# 		# Data Collection
# 		if state == 1:
# 			currentMember, currentSample, numOfSample, state, encodeListKnown, classNames = collectingData(img, currentMember, currentSample, numOfSample, state, encodeListKnown, classNames)

# 		# Start Data Collection
# 		if cv2.waitKey(1) & 0xFF == ord('1'):
# 			state = 1
# 			currentMember = startCollectingData(currentMember)

# 		# Start Face Recognition
# 		if cv2.waitKey(1) & 0xFF == ord('0'):
# 			state = 0

# 		cv2.imshow('Webcam', img)
# 		if cv2.waitKey(1) & 0xFF == ord('q'):
# 			break

if __name__ == '__main__':
	numOfSample, currentSample, currentMember, encodeListKnown, classNames = getInitialValue()
	img = cv2.imread("Screenshot 2022-04-13 033025.png")

	img, minPoint, maxPoint, centerPoint, isDetection = myFaceRecognition(img, encodeListKnown, classNames)

	img = checkDetection(isDetection, img, centerPoint, 640, 480, 100)

	cv2.imshow("test img", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
