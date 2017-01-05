import Tkinter as tk
from PIL import ImageTk, Image
import socket
import struct
import base64
from threading import Thread
import win32api
from cStringIO import StringIO
from time import sleep

def foo(arg):
	arg.mainloop()

IP = '10.20.170.73'
IP = '127.0.0.1'
PORT = 8888

s = socket.socket()
s.connect( ( IP , PORT ) )

root = tk.Tk()
#root.overrideredirect(1)

counter = 0

panel = tk.Label(root)

while True:
	max_size = 65535
	data = ''
	temp = 'a' * max_size
	c = 0
	while len(temp) == max_size or c == 0:
		l = int(s.recv(5))
		#print l
		s.send('go')
		temp = s.recv(l)
		print len(temp), c
		data += temp
		c += 1
	try:
		data = base64.b64decode(data)
	except:
		s.send('fail')
		continue
	finally:
		coords = win32api.GetCursorPos()
		s.send('ok' + str(coords))
	img = ImageTk.PhotoImage( Image.open( StringIO(data) ) )
	panel.configure(image = img)
	panel.image = img
	panel.pack(side = "bottom", fill = "both", expand = "yes")
	if counter == 0:
		thread = Thread(target = foo, args = (root, ))
		thread.start()
	counter += 1
	s.send('success')