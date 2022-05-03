import cv2 
from face_recognition_module import getInitialValue, myFaceRecognition, collectingData, startCollectingData

if __name__ == '__main__':
	state, numOfSample, currentSample, currentMember, encodeListKnown, classNames = getInitialValue()
	cap = cv2.VideoCapture(0)

	while True:
		success, img = cap.read()
		# Face Recognition
		if state == 0:
			img = myFaceRecognition(img, encodeListKnown, classNames)
		# Data Collection
		if state == 1:
			currentMember, currentSample, numOfSample, state, encodeListKnown, classNames = collectingData(img, currentMember, currentSample, numOfSample, state, encodeListKnown, classNames)

		# Start Data Collection
		if cv2.waitKey(1) & 0xFF == ord('1'):
			state = 1
			currentMember = startCollectingData(currentMember)

		# Start Face Recognition
		if cv2.waitKey(1) & 0xFF == ord('0'):
			state = 0

		cv2.imshow('Webcam', img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break