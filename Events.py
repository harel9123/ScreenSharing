import win32api, win32con
from constants import *
from time import sleep

# This file will contain functions that are related to 
# preforming events on the controlled machine.

def handleEvents(code, info):
	if code == K_KeyDown:
		keyboardEvents(code, info)
	else:
		mouseEvents(code, info)

def mouseEvents(code, pos):
	move(pos)

	if code == M_LeftDown or code == M_LeftUp:
		LM(code - M_LeftDown + 1, pos)

	elif code == M_RightDown or code == M_RightUp:
		RM(code - M_RightDown + 1, pos)

	elif abs(code) == M_Wheel:
		MW(code, pos)

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

def MW(code, pos):
	if code == M_Wheel:
		win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, pos[0], pos[1], M_WheelUp, 0)
	else:
		win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, pos[0], pos[1], M_WheelDown, 0)

def keyboardEvents(code, info):
	KD(code, info)

def KD(code, info):
	info = hex(ord(info))
	win32api.keybd_event(info, 0, 0, 0)
	sleep(.05)
	win32api.keybd_event(info, 0, win32con.KEYEVENTF_KEYUP, 0)

# Change cursor position
def move(pos):
	win32api.SetCursorPos(pos)