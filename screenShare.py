from PIL import Image, ImageGrab
import socket
from cStringIO import StringIO
from time import sleep
import base64
import win32api, win32con
import thread
import Events
import Queue

IP = '0.0.0.0'
streamPort = 8888
dataPort = 8889

q = Queue.Queue()

def getEncodedScreen():
	data = StringIO()
	img = ImageGrab.grab()
	img.save(data, 'png')
	return base64.b64encode(data.getvalue())

def parseData(data):
	data = data[1:-1]
	data = data.split(', ')
	code = int(data[0])
	x = int(data[1][1:])
	y = int(data[2][:-1])
	pos = (x, y)
	return (code, pos)

def handleEvents():
	while True:
		if not q.empty():
			data = q.get()
			code, pos = parseData(data)
			# If mouse event then ->
			Events.mouseEvents(code, pos)
			# else
			# keyboardEvents(data)
			# else
			# anyotherEvent ?

def dataTransportation():
	dataSocket = socket.socket()
	dataSocket.bind( ( IP , dataPort ) )
	dataSocket.listen(1)
	dataCon, dataAddr = dataSocket.accept()

	thread.start_new_thread(handleEvents, ())

	while True:
		try:
			data = dataCon.recv(1024)
			q.put(data)
			dataCon.send('.')
		except:
			return

def streamTransportation():
	streamSocket = socket.socket()
	streamSocket.bind( ( IP , streamPort ) )
	streamSocket.listen(1)
	strmCon, strmAddr = streamSocket.accept()

	thread.start_new_thread(dataTransportation, ())

	while True:
		data = getEncodedScreen()
		approval = strmCon.recv(2)
		if approval != "go":
			continue
		data = '(' + data + ')'
		strmCon.send(data)

		ack = strmCon.recv(15)
		if ack[:2] == 'ok':
			continue
			
	strmCon.close()

def main():
	streamTransportation()
	