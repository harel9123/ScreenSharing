# This file will contain functions that are related to 
# preforming events on the controlled machine.

def click(code, pos):
	if code == 513:
		win32api.SetCursorPos(pos)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1], 0, 0)

	elif code == 514:
		win32api.SetCursorPos(pos)	
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1], 0, 0)

	elif code == 516:
		win32api.SetCursorPos(pos)	
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos[0], pos[1], 0, 0)

	elif code == 517:
		win32api.SetCursorPos(pos)	
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos[0], pos[1], 0, 0)

def move(pos):
	win32api.SetCursorPos(pos)