import socket
import datetime
from PIL import ImageGrab

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 5252))

#con, addr = s.accept()

data, addr = s.recvfrom(1)

length = 10000

abc = 'abcdefghijklmnopqrstuvwxyz'

newSt = length * abc + ')'

print len(newSt)

l = len(newSt)
st = ''

before = datetime.datetime.now()
for x in range(l / 4096 + 1):
	st = newSt[:4096]
	newSt = newSt[4096:]
	s.sendto(st, addr)
after = datetime.datetime.now()

print str(after - before)

s.close()