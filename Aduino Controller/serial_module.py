import serial
import time

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

if __name__ == "__main__":
	ser = initConnection("COM4", 9600)  
	while True:
		sendData(ser, [255, 0], 3)
		time.sleep(1)
		sendData(ser, [0, 0], 3)
		time.sleep(1)
