from PIL import Image, ImageGrab
import socket
from cStringIO import StringIO
from time import sleep
import base64
import win32api, win32con
import thread
import Events
import Queue
from constants import *

q = Queue.Queue()

def getEncodedScreen():
	data = StringIO()
	img = ImageGrab.grab()
	img.save(data, 'png')
	return base64.b64encode(data.getvalue())

def parseData(data):
	data = data[1:-1]
	data = data.split(', ')
	code = None
	info = None
	if len(data) == 3:
		code = int(data[0])
		x = int(data[1][1:])
		y = int(data[2][:-1])
		info = (x, y)
	else:
		code = int(data[0])
		info = str(data[1])
	return (code, info)

def handleEvents():
	while True:
		if not q.empty():
			data = q.get()
			code, info = parseData(data)

			Events.handleEvents(code, info)

def dataTransportation():
	dataSocket = socket.socket()
	dataSocket.bind( ( listenIP , dataPort ) )
	print 'Data Socket Bound !'
	dataSocket.listen(1)
	print 'Data Socket Listening !'
	dataCon, dataAddr = dataSocket.accept()
	print 'Data Connection Established (8889) !'

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
	streamSocket.bind( ( listenIP , streamPort ) )
	print 'Stream Socket Bound !'
	streamSocket.listen(1)
	print 'Stream Socket Listening !'
	strmCon, strmAddr = streamSocket.accept()
	print 'Stream Connection Established (8888) !'

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

if __name__ == "__main__":
	main()