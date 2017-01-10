import pythoncom, pyHook

def OnMouseEvent(event):
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Position:',event.Position
    print '---'
    return True

hm = pyHook.HookManager()# create a hook manager
hm.MouseAll = OnMouseEvent
hm.HookMouse()
pythoncom.PumpMessages()