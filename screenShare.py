from PIL import Image, ImageGrab
import socket
from cStringIO import StringIO
from time import sleep
import base64
import win32api

def getEncodedScreen():
	data = StringIO()
	img = ImageGrab.grab()
	img.save(data, 'png')
	return base64.b64encode(data.getvalue())

IP = '0.0.0.0'
PORT = 8888

s = socket.socket()
s.bind( ( IP , PORT ) )
s.listen(1)
con, addr = s.accept()

while True:
	data = getEncodedScreen()
	approval = con.recv(2)
	if approval != "go":
		continue
	data = '(' + data + ')'
	con.send(data)

	ack = con.recv(15)
	if ack[:2] == 'ok':
		ack = ack[2:]
		ack = ack.split(',')
		ack[0] = ack[0].strip('(')
		ack[1] = ack[1].strip(')')
		x = int(ack[0])
		y = int(ack[1])
		#win32api.SetCursorPos( ( x, y ) )
		continue

con.close()