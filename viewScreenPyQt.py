import socket
import base64
import win32api
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import argv, exit
from os import getcwd
import pythoncom, pyHook
import Queue
import thread
from multiprocessing import Process
from constants import *

events = []

q = Queue.Queue()

def pyHookHandle():
	hm = pyHook.HookManager()# create a hook manager
	#hm.KeyDown = OnKeyboardEvent# watch for all key events
	hm.MouseAll = OnMouseEvent
	#hm.HookKeyboard()# set the hook
	hm.HookMouse()
	pythoncom.PumpMessages()

def parseEvent(event):
	msgName = str(event.Message)
	pos = str(event.Position)
	parsedVer = '[' + msgName + ', ' + pos + ']'
	return parsedVer

def addEvent(event):
	parsedEvent = parseEvent(event)
	q.put(parsedEvent)

def OnMouseEvent(event):
	addEvent(event)
	return True

def dataTransportation():
	connectionEstablished = False
	while connectionEstablished:
		try:
			dataCon = socket.socket()
			dataCon.connect( ( serverIP, dataPort ) )
		except:
			print 'Data Connection Failed (8889) !'
			sleep(1)
			continue
		connectionEstablished = True

	print 'Data Connection Established (8889) !'

	p = Process(target = pyHookHandle, args = ())
	p.start()

	while True:
		if not q.empty():
			data = q.get()
			dataCon.send(data)
			print 'Data sent: ' + data
			dataCon.recv(1)

# TODO: Listen to another port on another thread
# 		Add sendingtest.py to this file

class StreamScreen(QtGui.QMainWindow):
	def __init__(self, ):
		super(StreamScreen, self).__init__()
		self.setDimensions()
		self.initializeConnection()
		self.show()

	def setDimensions(self):
		width = win32api.GetSystemMetrics(0)
		height = win32api.GetSystemMetrics(1)
		self.setGeometry(30, 30, width - 1, height - 1)
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
			print 'Screen received !'
		except:
			self.streamCon.send('no')
			return
		finally:
			self.streamCon.send('ok')
		p = open('p.png', 'wb')
		p.write(data)
		p.close()

		self.pic.setPixmap(QtGui.QPixmap(getcwd() + '/p.png'))
		print 'Changed screen'

	def run(self, ):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.receiveScreen)
		self.timer.start(0)

def streamTransportation():
	pass

def main():
	app = QtGui.QApplication(argv)
	gui = StreamScreen()

	thread.start_new_thread(dataTransportation, ())

	gui.run()
	exit(app.exec_())

if __name__ == '__main__':
	main()