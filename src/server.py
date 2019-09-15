import socket
s = socket.socket()

port = 42069

s.bind(('', port))
print("socket binded to port %s" %(port))

s.listen(5)
print("socket is listening")

while True:
    conn, addr = s.accept()
    data = conn.recv(1024).decode().strip('\n')
    if len(data) > 0:
        print('received from ' + str(addr[0]) + ':' + str(addr[1]) + ': ' + data)
        conn.send(('received: ' + data + '\n').encode())
    conn.close()
    
