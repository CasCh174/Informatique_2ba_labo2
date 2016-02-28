from socket import *


print ('Hi! ')

HOST = 'localhost' #localhost
#lan 192.168.1.1
PORT = 8800 #place of a computer where information goes in and out
s= socket (AF_INET , SOCK_STREAM ) #defines how the socket is gonna work
s.bind((HOST, PORT))
s.listen (1) #how many connections it can receive at one time
conn , addr = s.accept () #accepts the connnection
#whenever it receives a connection : two data: 1 == ? , 2 == ip address
print ('connected by : ', addr)

while True :
    data = conn.recv (1024).decode() #max bites of data == 1024
    print ('Received ', data) #data == message the user types
    reply = input("Reply:  ").encode()
    conn.sendall(reply) #sendall is going to send to all nodes connected, send is only going to send to one specific node
    

conn.close() #not usefull right now because always true
