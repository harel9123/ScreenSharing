import socket
from multiprocessing import Process
import pythoncom, pyHook

s = socket.socket()
s.connect(('10.20.170.34', 9595))

movesCounter = 0

def parseEvent(event):
	global movesCounter
	msgName = str(event.Message)
	pos = str(event.Position)
	parsedVer = '[' + msgName + ', ' + pos + ']'
	s.send(parsedVer)
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

def main():
	pyHookHandle()
	# p = Process(target = pyHookHandle, args = ())
	# p.start()
	# p.join()	

if __name__ == '__main__':
	main()