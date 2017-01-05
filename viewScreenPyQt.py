from PIL import Image
import socket
import struct
import base64
from threading import Thread
import win32api
from cStringIO import StringIO
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys, os

IP = '10.0.0.1'
IP = '127.0.0.1'
PORT = 8888

s = socket.socket()
s.connect( ( IP , PORT ) )

app = QtGui.QApplication(sys.argv)
window = QtGui.QMainWindow()
window.setGeometry(30, 30, 1920, 1080)

counter = 0

pic = QtGui.QLabel(window)
pic.setGeometry(0, 0, 1920, 1080)

window.show()

def foo():
	max_size = 65535
	data = ''
	temp = 'a' * max_size
	temp = ''
	c = 0
	s.send('go')
	while ')' is not in temp:
		data += s.recv()
		print len(data), c
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

	pic.setPixmap(QtGui.QPixmap(os.getcwd() + '/p.png'))
	#counter += 1
	#s.send('success')

#thread = Thread(target = foo)
#thread.start()

timer = QtCore.QTimer()
timer.timeout.connect(foo)
timer.start(0)

sys.exit(app.exec_())