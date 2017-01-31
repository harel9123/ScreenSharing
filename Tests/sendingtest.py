import socket
from multiprocessing import Process
import pythoncom, pyHook

IP = '10.0.0.10'
# IP = '127.0.0.1'

s = socket.socket()
s.connect((IP, 9595))

def parseEvent(event):
	pos = str(event.Position)
	msgName = str(event.Message)
	parsedVer = '[' + msgName + ', ' + pos + ']'
	s.send(parsedVer)
	# print parsedVer
	s.recv(1)

def OnMouseEvent(event):
	#print parsedVer
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