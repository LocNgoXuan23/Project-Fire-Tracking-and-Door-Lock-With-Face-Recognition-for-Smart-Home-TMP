import cv2
import time
import math 

def drawFocus(img, minPoint, maxPoint, centerPoint, dispW, dispH, distanceThreshold):
    
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

def getDistance(point1, point2):
    return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))

if __name__ == '__main__':
    print(getDistance([5, 3], [1, 2]))
