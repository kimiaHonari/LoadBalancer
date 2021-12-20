import socket

host = socket.gethostname()
port = 8000
BUFFER_SIZE = 2010
MESSAGE=""

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

while MESSAGE != 'exit':
    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")
    if MESSAGE=='exit':
        break
    tcpClientA.send(MESSAGE)
    data = tcpClientA.recv(BUFFER_SIZE)
    print " Client received data:", data


tcpClientA.close()