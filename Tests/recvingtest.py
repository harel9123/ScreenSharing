import socket
import win32api, win32con
import thread
import Queue

s = socket.socket()
s.bind(('0.0.0.0', 9595))
s.listen(1)
con, addr = s.accept()

q = Queue()

def parse(data):
	data = data[1:]
	data = data[:-1]
	data = data.split(', ')
	code = data[0]
	pos = data[1]
	pos = pos[1:]
	pos = pos[:-1]
	pos = pos.split(', ')
	pos = (int(pos[0]), int(pos[1]))
	return (int(code), pos)

def click(code, pos):
	if code == 513:
		win32api.SetCursorPos(pos)
	    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1] ,0 ,0)

	elif code == 514:
		win32api.SetCursorPos(pos)	
	    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1], 0, 0)

def move(pos):
	win32api.SetCursorPos(pos)

def handle():
	while True:
		if not q.empty():
			data = q.get()
			print data
			data = parse(data)
			if data[0] == 513 || data[0] == 514:
				click(data[0], data[1])
			elif data[0] == 512:
				move(data[1])
				
thread.start_new_thread(handle, ())

while True:
	data = con.recv(50)
	con.send('k')
	q.put(data)