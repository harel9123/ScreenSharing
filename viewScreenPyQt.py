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
	# print 'Message:', event.Message
	# if event.Message == "mouse left down":
	# 	isClicked = (MOUSE_DOWN, LEFT, event.Position)
	# 	q.put(isClicked)
	# elif event.Message == "mouse left up":
	# 	isClicked = (MOUSE_UP, LEFT, event.Position)
	# 	q.put(isClicked)
	print 'Position:', event.Position
	# print '---'
	return True

def pyHookHandle():
	hm = pyHook.HookManager()# create a hook manager
	#hm.KeyDown = OnKeyboardEvent# watch for all key events
	hm.MouseAll = OnMouseEvent
	#hm.HookKeyboard()# set the hook
	hm.HookMouse()
	while True:
		pythoncom.PumpMessages()# wait forever

IP = '10.20.170.115'
IP = '127.0.0.1'
PORT = 8888

s = socket.socket()
s.connect( ( IP , PORT ) )

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

app = QtGui.QApplication(argv)
window = QtGui.QMainWindow()
window.setGeometry(30, 30, width - 1, height - 1)

counter = 0

pic = QtGui.QLabel(window)
pic.setGeometry(0, 0, width - 1, height - 1)

window.show()

def foo():
	data = ''
	temp = ''
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

	pic.setPixmap(QtGui.QPixmap(getcwd() + '/p.png'))

thread.start_new_thread( pyHookHandle, () )

timer = QtCore.QTimer()
timer.timeout.connect(foo)
timer.start(0)

exit(app.exec_())