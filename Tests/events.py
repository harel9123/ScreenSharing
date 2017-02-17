import pythoncom, pyHook
from time import sleep
import Queue
import thread

# q = Queue()
moved = False
isClicked = (0, 0, 0)
MOUSE_DOWN = 1
MOUSE_UP = 2

LEFT = 1
RIGHT = 2

def OnMouseEvent(event):
    # called when mouse events are received
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Time:',event.Time
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Position:',event.Position
    print 'Wheel:',event.Wheel
    print 'Injected:',event.Injected
    print '---'
    return True

def OnKeyboardEvent(event):
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Ascii:', event.Ascii
    print 'Key:', event.Key
    print 'KeyID:', event.KeyID
    print 'ScanCode:', event.ScanCode
    print 'Extended:', event.Extended
    print 'Injected:', event.Injected
    print 'Alt', event.Alt
    print 'Transition', event.Transition
    print '---'

def pyHookHandle():
	hm = pyHook.HookManager()# create a hook manager
	hm.KeyDown = OnKeyboardEvent# watch for all key events
	hm.MouseAll = OnMouseEvent
	hm.HookKeyboard()# set the hook
	hm.HookMouse()
	pythoncom.PumpMessages()# wait forever

pyHookHandle()