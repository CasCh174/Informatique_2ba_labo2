from socket import *

HOST = '172.17.33.80'
PORT = 8000
s = socket (AF_INET, SOCK_STREAM)
s.connect (( HOST, PORT)) #connect to connect to the server
                        #port number has to match with the one from the server
while True :
    message = input ('Your message: ').encode()
    s.send(message)
    print ('Awaiting reply')
    reply = s.recv (1024).decode()
    print ('Received', reply)

s.close ()
