#!/usr/bin/env python3
# chat.py
# author: Sébastien Combéfis
# version: February 15, 2016

import socket
import sys
import threading

class Chat:
    def __init__(self, host=socket.gethostname(), port=5000):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__myadress = (host, port)
        self.__s = s
        print('Écoute sur {}:{}'.format(host, port))
        
        
    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/register': self._register,
            '/connected': self._connected,
            '/list': self._list,
            '/send': self._send
        }
        self.__serveradress = (socket.gethostname(), 5000)
        self.__running = True
        self.__address = None
        self.__clientlist= []
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                     print ("Unexpected error:", sys.exc_info()[0])
            else:
                print('Command inconnue:', command)
    def _list(self):
        print(self.__clientlist)
    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()
    def _add(self, host, port, pseudo):
        self.__clientlist[:] = (host, port, pseudo)
        
    def _quit(self):
        self.__address = None   
    def _send(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totals__serevraddressent += sent
            except OSError:
                print('Erreur lors de la réception du message.')
    def _connectedlist(self, host, port):
        addressClient = (host, int(port))
        if addressClient is not None:
            try:
                param = str(self.__clientlist)
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], addressClient)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')
    def _join(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                #rm socket__serevraddress.gethostbyaddr()[0] because adding .home to the name 
                self.__address = (tokens[0], int(tokens[1]))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")

        self.__serveradress = (socket.gethostname(), 5000)

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                message = data.decode()
                print(message)
                addmsg = message.split(' ')
                if addmsg[0] == 'register':
                    self._add(addmsg[1], addmsg[2], addmsg[3])
                if  addmsg[0] == 'connected':
                    self._connectedlist(addmsg[1], addmsg[2])
                if addmsg[0] == 'chat':
                    clientadresschat = (addmsg[1], addmsg[2])
                    print(addmsg[3])
                    reply = input("Reply:  ")
                    if reply == '/endchat':
                        print('Conversation closed')
                    else:
                        msgreply = reply.encode()
                        totalsent = 0
                        while totalsent < len(msgreply):
                            sent = self.__s.sendto(msgreply[totalsent:], clientadresschat)
                            totalsent += sent
                    
            except socket.timeout:
                pass
            except OSError:
                return
    def _register(self, pseudo):
        if self.__serveradress is not None:
            try:
                param = 'register {} {} {}'.format(self.__myadress[0], self.__myadress[1],pseudo)
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress)
                    totalsent += sent
                print('Client registered to the server')
            except OSError:
                print('Erreur lors de la réception du message.')

                
    def _connected(self):
        if self.__serveradress is not None:
            try:
                param = 'connected {} {}'.format(*self.__myadress)
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.') 

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
