from PIL import Image, ImageGrab
import socket
from cStringIO import StringIO
from time import sleep
import base64
import win32api

IP = '0.0.0.0'
PORT = 8888

s = socket.socket()
s.bind( ( IP , PORT ) )
s.listen(1)
con, addr = s.accept()

while True:
	data = StringIO()
	img = ImageGrab.grab()
	img.save(data, 'png')
	data = base64.b64encode(data.getvalue())
	l = len(data)
	sent = 0
	max_size = 65535
	approval = con.recv(2)
	if approval != "go":
		continue

	'''for x in range( ( l / max_size ) + 1 ):
		sent += max_size
		toSend = data[ : max_size]
		#print len(toSend), x
		data = data[max_size : ]
		l = len(toSend)
		l = str(l)
		#print l
		if len(l) < 5:
			l = '0' + l
		con.send(l)
		ack = con.recv(2)
		if ack != 'go':
			break
		#print ack #For delay
		t = con.send( toSend )
		#print t, x'''
	data = '(' + data + ')'
	con.send(data)

	ack = con.recv(15)
	#print ack
	if ack[:2] == 'ok':
		ack = ack[2:]
		ack = ack.split(',')
		ack[0] = ack[0].strip('(')
		ack[1] = ack[1].strip(')')
		x = int(ack[0])
		y = int(ack[1])
		win32api.SetCursorPos( ( x, y ) )
		continue

con.close()