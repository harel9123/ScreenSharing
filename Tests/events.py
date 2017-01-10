import pythoncom, pyHook
from time import sleep
import Queue

q = Queue()
moved = False
isClicked = (0, 0, 0)
MOUSE_DOWN = 1
MOUSE_UP = 2

LEFT = 1
RIGHT = 2

def OnMouseEvent(event):
	global isClicked
	global q
    print 'MessageName:', event.MessageName
    print 'Message:', event.Message
    if event.Message == "mouse left down":
    	isClicked = (MOUSE_DOWN, LEFT, event.Position)
    	q.put(isClicked)
    elif event.Message == "mouse left up":
    	isClicked = (MOUSE_UP, LEFT, event.Position)
    	q.put(isClicked)
    print 'Position:', event.Position
    print '---'
    return True

def pyHookHandle():
	hm = pyHook.HookManager()# create a hook manager
	#hm.KeyDown = OnKeyboardEvent# watch for all key events
	hm.MouseAll = OnMouseEvent
	#hm.HookKeyboard()# set the hook
	hm.HookMouse()
	pythoncom.PumpMessages()# wait forever

pyHookHandle()