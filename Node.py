import sys
import socket
import math
import pickle

def sendVector():
    for i in range(len(sv)):
        try:
            sw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sw.connect(('localhost', sv[i]))
            # sw.setblocking(False)
            serialized_dtv = pickle.dumps(dtv)
            sw.sendall(serialized_dtv)
            sw.close()   
        except: KeyboardInterrupt
      
p = sys.argv[1]
PORT = int(p)

dtv = {} ### distance vector
dtv[PORT] = 0
sv = [] ### send vector to immediate neighbours

flag = False ### flag for difference between distance vectors

with open(p + '.costs', 'r') as c:
    lines = c.readlines()
    n = int(lines[0])
    for i in range(1, len(lines)):
        dtv[int(lines[i][:4])] = int(lines[i][5:])
        sv.append(int(lines[i][:4]))

for i in range(n):
    if 3000 + i in dtv:
        continue
    else:
        dtv[3000 + i] = math.inf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', PORT))
s.listen(n)
s.settimeout(5)

imn = 3000 ### immediate vector port 
sendVector()

try:
    while True:
        for i in range(len(sv)):
            client, address = s.accept()
            recv_data = client.recv(1024)
            usdtv = pickle.loads(recv_data)
            client.close()

            imn = next(iter(usdtv))
            for j in usdtv: 
                if dtv[j] > dtv[imn] + usdtv[j]: ### bellman-ford
                    dtv[j] = dtv[imn] + usdtv[j]
                    flag = True

        if flag:
            sendVector()
            flag = False

except socket.timeout:
    # s.shutdown(socket.SHUT_RDWR)
    s.close()
    for i in dtv:
        distance = p + " -" + str(i) + " | " + str(dtv[i])
        print(distance)