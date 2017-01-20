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
from multiprocessing import Process

moved = False
isClicked = (0, 0, 0)
MOUSE_DOWN = 1
MOUSE_UP = 2

LEFT = 1
RIGHT = 2

def OnMouseEvent(event):
	# global isClicked
	# global q
	# print 'MessageName:', event.MessageName
	print 'Message:', event.Message
	# if event.Message == "mouse left down":
	# 	isClicked = (MOUSE_DOWN, LEFT, event.Position)
	# 	q.put(isClicked)
	# elif event.Message == "mouse left up":
	# 	isClicked = (MOUSE_UP, LEFT, event.Position)
	# 	q.put(isClicked)
	#print 'Position:', event.Position
	# print '---'
	return True

def pyHookHandle():
	print "IN PROCESS"
	hm = pyHook.HookManager()# create a hook manager
	#hm.KeyDown = OnKeyboardEvent# watch for all key events
	hm.MouseAll = OnMouseEvent
	#hm.HookKeyboard()# set the hook
	hm.HookMouse()
	pythoncom.PumpMessages()

IP = '10.20.170.30'
IP = '127.0.0.1'
PORT = 8888

class StreamScreen(QtGui.QMainWindow):
	def __init__(self, ):
		super(StreamScreen, self).__init__()
		width = win32api.GetSystemMetrics(0)
		height = win32api.GetSystemMetrics(1)
		self.setGeometry(30, 30, width - 1, height - 1)
		self.pic = QtGui.QLabel(self)
		self.pic.setGeometry(0, 0, width - 1, height - 1)

		self.show()

	def foo(self, ):
		data = ''
		temp = 'empty'
		s.send('go')
		sizeToRec = 65535
		while temp[-1] != ')':
			temp = s.recv(sizeToRec)
			data += temp
		data = data[1:]
		data = data[:len(data) - 1]
		try:
			data = base64.b64decode(data)
		except:
			s.send('fail')
			return
		finally:
			coords = win32api.GetCursorPos()
			s.send('ok' + str(coords))
		p = open('p.png', 'wb')
		p.write(data)
		p.close()

		self.pic.setPixmap(QtGui.QPixmap(getcwd() + '/p.png'))

	def run(self, ):
		timer = QtCore.QTimer()
		timer.timeout.connect(self.foo)
		timer.start(0)

		exit(app.exec_())

if __name__ == '__main__':
	s = socket.socket()
	s.connect( ( IP , PORT ) )

	app = QtGui.QApplication(argv)
	gui = StreamScreen()

	p = Process(target = pyHookHandle, args = ())
	p.start()

	gui.run()
	p.join()