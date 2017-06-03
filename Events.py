import win32api, win32con
from constants import *
from time import sleep

# This file will contain functions that are related to 
# preforming events on the controlled machine.

def handleEvents(code, info):
	'''
		*This function handles all events and calls the right handler according to the message code.
	'''
	if code == K_KeyDown or code == K_KeySysDown:
		keyboardEvents(code, info)
	else:
		mouseEvents(code, info)

def mouseEvents(code, pos):
	'''
		*This function handles mouse events and calls the right mouse event.
	'''
	move(pos)

	if code == M_LeftDown or code == M_LeftUp:
		LM(code - M_LeftDown + 1, pos)

	elif code == M_RightDown or code == M_RightUp:
		RM(code - M_RightDown + 1, pos)

	elif abs(code) == M_Wheel:
		MW(code, pos)


def keyboardEvents(code, info):
	'''
		*This function handles Keyboard events.
	'''
	KD(code, info)


def LM(code, pos):
	'''
		*This function preforms a Left-Mouse click in the given position.
	'''
	if code == 1:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1], 0, 0)
	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1], 0, 0)


def RM(code, pos):
	'''
		*This function preforms a Right-Mouse click in the given position.
	'''
	if code == 1:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, pos[0], pos[1], 0, 0)
	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, pos[0], pos[1], 0, 0)


def MW(code, pos):
	'''
		*This function preforms a Mouse-Wheel scroll event in the given position.
	'''
	if code == M_Wheel:
		win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, pos[0], pos[1], M_WheelUp, 0)
	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, pos[0], pos[1], M_WheelDown, 0)


def KD(code, info):
	'''
		*This function preforms a Keyboard event of the given info (button key).
	'''
	info = ord(info)
	win32api.keybd_event(info, 0, 0, 0)
	sleep(.05)
	win32api.keybd_event(info, 0, win32con.KEYEVENTF_KEYUP, 0)


def move(pos):
	'''
		*This function changes the position of the cursor.
	'''
	win32api.SetCursorPos(pos)