from socket import *


HOST = 'localhost' #172.17.33.80
PORT = 5001
s = socket (AF_INET, SOCK_DGRAM)
s.connect (( HOST, PORT)) #connect to connect to the server
                        #port number has to match with the one from the server

HOSTCLIENT = 'localhost' #localhost
#lan 192.168.1.1
PORTCLIENT = 8810 #place of a computer where information goes in and out
s.bind((HOSTCLIENT, PORTCLIENT))
s.listen (1) #how many connections it can receive at one time
conn , addr = s.accept () #accepts the connnection
#whenever it receives a connection : two data: 1 == ? , 2 == ip address
print ('connected by : ', addr)


while True :
    message = input ('Your message: ')
    messageformatted = '{} {} {}'.format(HOSTCLIENT, PORTCLIENT, message)
    messageformatted.encode()
    s.send(messageformatted)
    print ('Awaiting reply')
    reply = s.recv (1024).decode()
    print ('Received', reply)

s.close ()
