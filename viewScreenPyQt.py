import socket
import base64
import win32api
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import argv, exit
from os import getcwd

#IP = '10.0.0.1'
#IP = '127.0.0.1'
PORT = 8888

def run(IP):
	s = socket.socket()
	s.connect( ( IP , PORT ) )

	width = win32api.GetSystemMetrics(0)
	height = win32api.GetSystemMetrics(1)

	#app = QtGui.QApplication(argv)
	window = QtGui.QMainWindow()
	window.setGeometry(30, 30, width - 1, height - 1)

	pic = QtGui.QLabel(window)
	pic.setGeometry(0, 0, width - 1, height - 1)

	window.show()

	timer = QtCore.QTimer()
	timer.timeout.connect(foo)
	timer.start(0)

	#exit(app.exec_())



def foo():
	data = ''
	temp = ''
	c = 0
	s.send('go')
	sizeToRec = 65535
	while ')' not in temp:
		temp = s.recv(sizeToRec)
		data += temp
		#print len(data), c
		#data += temp
		c += 1
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