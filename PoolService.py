import socket
from threading import Thread
from threading import Lock

listOfStudentNumber=[]
mutex = Lock()
import datetime
from random import randint
import time
#checkif request has 7 digit number
def hasNumbers(inputString):
    p=0
    q=0
    n=0
    for char in inputString :
        q=q+1
        if char.isdigit() :
            if n==0 :
                p=q-1
            n=n+1

            if p+1==q :
                p=q
            else :
                return 0
            if n==7 :
                return 1


# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self, ip, port ,conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn=conn
        print "[+] New PoolServer socket thread started for " + ip + ":" + str(port)

    def run(self):

        flag=0;
        while True:
            data = self.conn.recv(2000)
            print "P : received data:", data
            #close connection if receive exit
            if data == "exit":
                self.conn.close()
                break;
            print "Pool : ", listOfStudentNumber
            #hasnumber function check if request hast student number
            if hasNumbers(data) :
                #split command L,922...
                list=data.split(',')
                # check if command is not correct
                if list[0]!="P" :
                    self.conn.send("P : " + "Command is not correct")
                    continue
                # check if student number exist in a list
                if any(list[1] in s for s in listOfStudentNumber):
                    #write in a file
                    mutex.acquire()
                    fo = open("LogP.txt", "a")
                    fo.write(datetime.date.today().ctime()+"   P    "+list[1]+" Login to system"+"\n" )
                    fo.close()
                    mutex.release()
                    #end
                    #wait for random millisecond
                    RandomIndex = randint(0, 1500)
                    time.sleep(RandomIndex/1000)
                    result="P : " + "has been registered before"
                    # send result
                    self.conn.send(result)
                else :

                    mutex.acquire()
                    fo = open("LogP.txt", "a")
                    listOfStudentNumber.append(list[1])
                    fo.write(datetime.date.today().ctime() + "   P    " + list[1] + " Register to system"+"\n" )
                    fo.close()
                    mutex.release()

                    RandomIndex = randint(0, 1500)

                    time.sleep(RandomIndex/1000)
                    result="P : " + "registration completed"
                    self.conn.send(result)
            #if request doesn't have student number echo request
            else :
                #log
                mutex.acquire()
                fo = open("LogP.txt", "a")
                fo.write(datetime.date.today().ctime() + "   P    " +"Client request: "+ data+"\n" )
                fo.close()
                mutex.release()
                #end
                RandomIndex = randint(0, 1500)
                time.sleep(RandomIndex/1000)
                #echo
                self.conn.send("P : " + data)




# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 9700 # listen to port 9700
BUFFER_SIZE = 2000

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(8)
    (connection, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port,connection)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()