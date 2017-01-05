import socket
import base64
import win32api
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import argv, exit
from os import getcwd

IP = '10.0.0.1'
IP = '127.0.0.1'
PORT = 8888

s = socket.socket()
s.connect( ( IP , PORT ) )

app = QtGui.QApplication(argv)
window = QtGui.QMainWindow()
window.setGeometry(30, 30, 1920, 1080)

counter = 0

pic = QtGui.QLabel(window)
pic.setGeometry(0, 0, 1920, 1080)

window.show()

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

timer = QtCore.QTimer()
timer.timeout.connect(foo)
timer.start(0)

exit(app.exec_())