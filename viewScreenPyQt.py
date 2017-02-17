import socket
import base64
import win32api
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import argv, exit
from os import getcwd
import pythoncom, pyHook
import thread
from multiprocessing import Process, Queue
from constants import *

events = []

localQueue = Queue()

def pyHookHandle(mainQueue):
	print 'pyHookHandle Process successfully created !'
	hm = pyHook.HookManager() # create a hook manager
	hm.KeyDown = OnKeyboardEvent # watch for all key events
	hm.MouseAll = OnMouseEvent
	hm.HookKeyboard() # set the hook
	hm.HookMouse()
	while True:
		while not localQueue.empty():
			mainQueue.put(localQueue.get())
		pythoncom.PumpWaitingMessages()

def parseEvent(event, code):
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
		pos = str(event.Position)
		parsedVer = '[' + msgName + ', ' + pos + ']'
	return parsedVer

def addEvent(event, code):
	global localQueue
	parsedEvent = parseEvent(event, code)
	localQueue.put(parsedEvent)


def OnMouseEvent(event):
	# if event.WindowName == 'python':
		# addEvent(event, 0)
	return True

def OnKeyboardEvent(event):
	if event.WindowName == 'python':
		addEvent(event, 1)
	return True

def dataTransportation():
	mainQueue = Queue()
	connectionEstablished = False
	dataCon = None
	while not connectionEstablished:
		try:
			dataCon = socket.socket()
			dataCon.connect( ( serverIP, dataPort ) )
			connectionEstablished = True
		except:
			print 'Data Connection Failed (8889) !'
			sleep(1)
			continue

	print 'Data Connection Established (8889) !'

	p = Process(target = pyHookHandle, args = (mainQueue, ))
	p.start()

	while True:
		data = mainQueue.get()
		dataCon.send(data)
		dataCon.recv(1)
	p.join()

class StreamScreen(QtGui.QMainWindow):
	def __init__(self, ):
		super(StreamScreen, self).__init__()
		self.setDimensions()
		self.initializeConnection()
		self.showFullScreen()

	def setDimensions(self, ):
		width = win32api.GetSystemMetrics(0)
		height = win32api.GetSystemMetrics(1)
		self.setGeometry(0, 0, width - 1, height - 1)
		self.pic = QtGui.QLabel(self)
		self.pic.setGeometry(0, 0, width - 1, height - 1)

	def initializeConnection(self, ):
		self.streamCon = socket.socket()
		self.streamCon.connect( ( serverIP, streamPort ) )
		print 'Stream Connection Established (8888) !'

	def receiveScreen(self, ):
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
		success = pixmap.loadFromData(data, format = "PNG")

		if success:
			self.pic.setPixmap(pixmap)

	def run(self, ):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.receiveScreen)
		self.timer.start(0)

def streamTransportation():
	pass

def main():
	app = QtGui.QApplication(argv)
	gui = StreamScreen()

	# thread.start_new_thread(dataTransportation, ())

	p = Process(target = dataTransportation, args = ())
	p.start()

	gui.run()
	retVal = app.exec_()
	p.join()
	exit(retVal)

if __name__ == '__main__':
	main()