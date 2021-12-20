import socket
from threading import Thread

BUFFER_SIZE = 2000
host = socket.gethostname()
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self, ip, port , conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn=conn
        print "[+] New LB socket thread started for " + ip + ":" + str(port)

    def run(self):
        port=0;
        while True:
            # decompose first command to notice which worker must notify
            data = self.conn.recv(2000)
            print "LB received data:", data
            #close connection if receive exit
            if data == "exit":
                self.conn.close()
                break;
            list = data.split(',')
            print list[0]
            if list[0] == "L":
                port = 9000
            if list[0] == "D":
                port = 9500
            if list[0]=="P":
                port = 9700

            tcpService = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpService.connect((host, port))
            tcpService.send(data) # send first request
            data = tcpService.recv(BUFFER_SIZE)#receive response from worker
            print "lb :",data
            self.conn.send(data)# send response to client
            #this loop continue until client wants to exit from worker
            while True :
                data = self.conn.recv(2000)
                print "LB received data from "+list[0]+" :", data
                #close connection if receive exit
                if data=="exit" :
                    self.conn.close()
                    break;
                #close connection with worker if receive exit + name of worker (L,P,D)
                if data=="exit "+list[0] :
                    self.conn.send("exit from service "+list[0])
                    tcpService.send("exit")
                    print "connection between LB and library close"
                    tcpService.close()
                    break
                else :
                    #echo
                    tcpService.send(data)
                    data1 = tcpService.recv(BUFFER_SIZE)
                    print "lb :", data1
                    self.conn.send(data1)



# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 8000 # listen to port 8000
BUFFER_SIZE = 2000

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []
tcpServer.listen(15)
while True:

    (connection, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port,connection) # thread for each connection from client
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()