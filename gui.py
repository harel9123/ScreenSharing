from PyQt4 import QtGui, QtCore
#import RCGui - The gui of the Remotecontrol menu
#import netDevice
import viewScreenPyQt
import screenShare
import sys
from os import system
import threading

class IntroWindow(QtGui.QMainWindow):

	def __init__(self, ):
		super(IntroWindow, self).__init__()
		self.setGeometry(0, 0, 200, 200)
		self.center()
		self.setup()
		self.show()

	def center(self):
		frameGm = self.frameGeometry()
		point = QtCore.QPoint(0, 0)
		screen = QtGui.QApplication.desktop().screenNumber(point)
		centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def setup(self):

		'''
		self.username = QtGui.QLineEdit(self)
		self.username.setPlaceholderText("Username")

		self.password = QtGui.QLineEdit(self)
		self.password.setPlaceholderText("Password")

		self.btn = QtGui.QPushButton("Connect", self)
		'''

		self.ip = QtGui.QLineEdit(self)
		self.ip.setPlaceholderText("IP")

		self.viewBTN = QtGui.QPushButton("Connect", self)
		self.viewBTN.clicked.connect(self.handleViewer)

		self.streamBTN = QtGui.QPushButton("Stream", self)
		self.streamBTN.clicked.connect(self.handleStream)

		self.ip.move(50, 50)
		#self.password.move(50, 80)
		self.viewBTN.move(50, 80)
		self.streamBTN.move(50, 110)		

	def handleStream(self):
		self.close()
		f = screenShare.run
		t = threading.Thread(target = f,)
		t.start()
		t.join()

	def handleViewer(self):
		ip = self.ip.text()
		self.close()
		f = viewScreenPyQt.run
		t = threading.Thread(target = f, args = (ip, ))
		t.start()
		t.join()
		
	def handleConnect(self):
		uname = self.username.text()
		passwd = self.password.text()
		#msg = netDev.connect(uname, passwd)
		#Call Network Class Connect Function
		#if msg[0] != "Success":
		#	errorHandle(msg)
		#else:
		#	self.close()
		#	RCGui.run(msg[1])

	def errorHandle(self, msg = "Operation has failed !"):
		msgbox = QtGui.QMessageBox()
		msgbox.setWindowTitle("Error")
		msgbox.setText(msg)
		msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
		retval = msgbox.exec_()


def main():
	app = QtGui.QApplication(sys.argv)
	w = IntroWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()