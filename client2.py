import socket

host = socket.gethostname()
port = 8000
BUFFER_SIZE = 2010
MESSAGE =""

tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB.connect((host, port))

while MESSAGE != 'exit':
    MESSAGE = raw_input("tcpClientB: Enter message to continue/ Enter exit:")
    if MESSAGE == 'exit':
        break
    tcpClientB.send(MESSAGE)
    data = tcpClientB.recv(BUFFER_SIZE)
    print " Client received data:", data


tcpClientB.close()