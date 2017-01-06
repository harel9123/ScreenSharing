import socket
import re
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('127.0.0.1', 5252)

s.sendto('a', addr)

abc = 'abcdefghijklmnopqrstuvwxyz'
temp = ''
data = ''

before = datetime.datetime.now()
while ')' not in temp:
	temp = s.recvfrom(65556)[0]
	data += temp
after = datetime.datetime.now()

print str(after - before)

alls = re.findall(abc, data)

print len(alls)
print len(data)

s.close()