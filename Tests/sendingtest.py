import socket
from multiprocessing import Process
import pythoncom, pyHook

s = socket.socket()
s.connect(('127.0.0.1', 9595))

def parseEvent(event):
	msgName = str(event.MessageName)
	pos = str(event.Position)
	prasedVer = '[' + msgName + ', ' + pos + ']'
	s.send(prasedVer)
	s.recv(1)

def OnMouseEvent(event):
	parseEvent(event)
	return True

def pyHookHandle():
	# print "IN PROCESS"
	hm = pyHook.HookManager()# create a hook manager
	#hm.KeyDown = OnKeyboardEvent# watch for all key events
	hm.MouseAll = OnMouseEvent
	#hm.HookKeyboard()# set the hook
	hm.HookMouse()
	pythoncom.PumpMessages()


p = Process(target = pyHookHandle, args = ())
p.join()