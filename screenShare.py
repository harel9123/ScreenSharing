from PIL import Image, ImageGrab
import socket
from cStringIO import StringIO
from time import sleep
from base64 import b64encode
import win32api

IP = '0.0.0.0'
PORT = 8888

def run():
	s = socket.socket()
	s.bind( ( IP , PORT ) )
	s.listen(1)
	con, addr = s.accept()

	while True:
		data = StringIO()
		img = ImageGrab.grab()
		img.save(data, 'png')
		data = b64encode(data.getvalue())
		l = len(data)
		sent = 0
		max_size = 65535
		approval = con.recv(2)
		if approval != "go":
			continue

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

run()