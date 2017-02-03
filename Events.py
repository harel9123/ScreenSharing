from constants import *

# This file will contain functions that are related to 
# preforming events on the controlled machine.

def mouseEvents(code, pos):
	move(pos)

	if code == M_LeftDown or code == M_LeftUp:
		LM(code - M_LeftDown + 1, pos)

	elif code == M_RightDown or code == M_RightUp:
		RM(code - M_RightDown + 1, pos)

	# Add more mouse events in the future

# Left mouse
def LM(code, pos):
	if code == 1:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1], 0, 0)
	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1], 0, 0)

# Right mouse
def RM(code, pos):
	if code == 1:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos[0], pos[1], 0, 0)
	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos[0], pos[1], 0, 0)

# Change cursor position
def move(pos):
	win32api.SetCursorPos(pos)