import time 
import serial

def initConnection(portNo, baudRate):
	try:
		ser = serial.Serial(portNo, baudRate)
		print("Device Connected")
		return ser
	except:
		print("Not Connected")


if __name__ == "__main__":
	ser = initConnection("COM4", 9600) 
	while True:
		while (ser.inWaiting() == 0):
			pass
		dataPacket = ser.readline()
		print(dataPacket)
