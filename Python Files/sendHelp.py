import socket
import base64
import win32api
from time import sleep
from PyQt4 import QtGui, QtCore
from sys import argv, exit
from os import getcwd
import pythoncom, pyHook
import thread
from multiprocessing import Process, Queue
from constants import *
import sys

events = []

localQueue = Queue()

width = 0
height = 0
startingWidth = 0
startingHeight = 0

def setGlobalVars(dimensions):
	'''
		*This function sets all the global variables to the screen dimensions.
		*Input: Screen dimensions.
		*Output: None.
	'''
	global width, height, startingWidth, startingHeight
	width = dimensions[0]
	height = dimensions[1]
	startingWidth = dimensions[2]
	startingHeight = dimensions[3]

def pyHookHandle(mainQueue, dimensions):
	'''
		*This function is used to detect events in the computer.
		*Input: A queue of messages, dimensions of the screen.
		*Output: None.
	'''
	print 'pyHookHandle Process successfully created !'
	hm = pyHook.HookManager() # create a hook manager
	hm.KeyDown = OnKeyboardEvent # watch for all key events
	hm.MouseAll = OnMouseEvent # watch for all mouse events
	hm.HookKeyboard() # set the hook
	hm.HookMouse()
	while True:
		while not localQueue.empty():
			mainQueue.put(localQueue.get())
		pythoncom.PumpWaitingMessages()

def parseEvent(event, code):
	'''
		*This function parses a pyHook event to the protocol.
		*Input: An event to parse, message code.
		*Output: String of the parsed event.
	'''
	parsedVer = ''
	if code:
		msgName = str(event.Message)
		info = str(chr(event.KeyID))
		parsedVer = '[' + msgName + ', ' + info + ']'
	else:
		if event.Wheel != 0:
			msgName = str(event.Message * event.Wheel)
		else:
			msgName = str(event.Message)
		pos = (event.Position[0] - startingWidth, event.Position[1] - startingHeight)
		pos = str(pos)
		parsedVer = '[' + msgName + ', ' + pos + ']'
	return parsedVer

def addEvent(event, code):
	'''
		*This function adds a parsed event to the events queue.
		*Input: A queue of messages, dimensions of the screen.
		*Output: None.
	'''
	global localQueue
	parsedEvent = parseEvent(event, code)
	localQueue.put(parsedEvent)

def OnMouseEvent(event):
	'''
		*This function is called whenever a mouse event occurs.
		*Input: A pyHook event object.
		*Output: Returns True as a success code.
	'''
	pos = event.Position
	#if (pos[0] > startingWidth and pos[0] < width + startingWidth and pos[1] > startingHeight and pos[1] < height + startingHeight):
	if event.WindowName == 'python':
		addEvent(event, 0)
	return True

def OnKeyboardEvent(event):
	'''
		*This function is called whenever a key press event occurs.
		*Input: A pyHook event object.
		*Output: Returns True as a success code.
	'''
	if event.WindowName == 'python':
		addEvent(event, 1)
	return True

def dataTransportation(dimensions, IP):
	'''
		*This function controls the transportation of the events data of the connection.
		*Input: dimensions of the screen and the server ip.
		*Output: None.
	'''
	mainQueue = Queue()
	connectionEstablished = False
	dataCon = None
	while not connectionEstablished:
		try:
			dataCon = socket.socket()
			dataCon.connect( ( IP, dataPort ) )
			connectionEstablished = True
		except:
			print 'Data Connection Failed (8889) !'
			sleep(1)
			continue

	print 'Data Connection Established (8889) !'

	p = Process(target = pyHookHandle, args = (mainQueue, dimensions, ))
	p.start()

	while True:
		data = mainQueue.get()
		dataCon.send(data)
		dataCon.recv(1)
	p.join()

class StreamScreen(QtGui.QMainWindow):
	def __init__(self, dimensions, ):
		'''
			*This class inherits from QMainWindow and will be used to show the stream.
		'''
		super(StreamScreen, self).__init__()
		self.initializeConnection()
		self.setDimensions(dimensions)
		self.showFullScreen()

	def setDimensions(self, dimensions, ):
		'''
			*This function sets the dimensions of the stream screen.
			*Input: The dimensions of the screen.
			*Output: None.
		'''
		width = win32api.GetSystemMetrics(0)
		height = win32api.GetSystemMetrics(1)
		self.setGeometry(0, 0, width - 1, height - 1)
		self.pic = QtGui.QLabel(self)
		startingWidth = abs(width - self.width) / 2
		startingHeight = abs(height - self.height) / 2
		self.pic.setGeometry(startingWidth, startingHeight, self.width - 1, self.height - 1)

		dimensions.append(self.width)
		dimensions.append(self.height)
		dimensions.append(startingWidth)
		dimensions.append(startingHeight)

	def initializeConnection(self, ):
		'''
			*This function creates a connection between the peers.
			*Input: None.
			*Output: None.
		'''
		self.streamCon = socket.socket()
		self.streamCon.connect( ( serverIP, streamPort ) )
		print 'Stream Connection Established (8888) !'
		firstConData = self.streamCon.recv(50)
		firstConData = firstConData.split(', ')
		self.width = int(firstConData[0][1:])
		self.height = int(firstConData[1][:-1])

	def receiveScreen(self, ):
		'''
			*This function handles the received data from the peer, a screenshot of his screen
			 and sets the window to show that screenshot.
			*Input: None.
			*Output: None.
		'''
		data = ''
		temp = ' '
		self.streamCon.send('go')
		sizeToRec = 65535
		while temp[-1] != ')':
			temp = self.streamCon.recv(sizeToRec)
			data += temp
		data = data[1:-1]
		try:
			data = base64.b64decode(data)
		except:
			self.streamCon.send('no')
			return
		finally:
			self.streamCon.send('ok')

		pixmap = QtGui.QPixmap()
		pixmap.fill(QtCore.Qt.black)
		success = pixmap.loadFromData(data, format = "PNG")

		if success:
			self.pic.setPixmap(pixmap)

	def run(self, ):
		'''
			*This function sets a timer that calls receiveScreen infinitely.
			*Input: None.
			*Output: None.
		'''
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.receiveScreen)
		self.timer.start(0)


def main():
	if len(sys.argv) != 2:
		print "Usage: script_name IP_OF_SERVER"
		return;
	global serverIP
	serverIP = sys.argv[1]

	app = QtGui.QApplication(argv) # Creation of Qt app
	dimensions = []
	gui = StreamScreen(dimensions)

	p = Process(target = dataTransportation, args = (dimensions, serverIP, )) # New process to handle the events data
	p.start()

	gui.run()
	retVal = app.exec_()
	p.join()
	exit(retVal)

if __name__ == '__main__':
	main()