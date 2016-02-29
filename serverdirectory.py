

import socket
import sys
import threading


class Chat:
    def __init__(self, host=socket.gethostname(), port=5000):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__myadress = (host, port)
        print (self.__myadress)     #pour le serveur ca renvoit ('CharlesCasti', 5000) pour les client ('host',port)
        self.__s = s
        print('Écoute sur {}:{}'.format(host, port))


    def run(self):  #handlers contient les méthodes dispo pour les clients =/= toutes les méthodes
                    #quand est ce que le client ou serveur passe par ici ?
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/register': self._register,
            '/connected': self._connected,
            '/list': self._list,
            '/send': self._send,
            '/chat': self._startchat

        }
        self.__serveradress = (socket.gethostname(), 5000)      #ca donne l'adresse du serveur au client
        print (self.__serveradress)
        self.__running = True       #tjrs vrai jusqu'a exit
        self.__address = None
        self.__clientlist= []
        self.__clientpseudo = ''
        threading.Thread(target=self._receive).start()
        while self.__running:       #if self.__running is true, alors on lit la commande demandée par l'utilisateur
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)    #on prend self._command(param si il y en a)
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
    def _add(self, host, port, pseudo):         #uniquement si un client fait register --> le serveur l ajoute a la liste des clients dispo + pseudo
        self.__clientlist.append((host, port, pseudo))
        self.__clientpseudo = pseudo


    def _quit(self):
        self.__address = None
    def _send(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totals__serevraddressent += sent            #sereeeevr
            except OSError:
                print('Erreur lors de la réception du message.')
    def _connectedlist(self, host, port):
        addressClient = (host, int(port))   #pour savoir a qui envoyer la liste clientlist
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
                addmsg = message.split(' ')     #le message recu est mis dans une liste pour pouvoir l analyser
                if addmsg[0] == 'register':
                    self._add(addmsg[1], addmsg[2], addmsg[3])
                if  addmsg[0] == 'connected':
                    self._connectedlist(addmsg[1], addmsg[2])  #le serveur ouvre self.connectedlist avec les arguments (addmsg[1] et ...)
                if addmsg[0] == 'startchat':
                    receiver = addmsg[3]
                    for client in self.__clientlist:
                        if client[2] == receiver:
                            receiveradress= (client[0], client[1])
                    self._clientadresschat = (addmsg[1], addmsg[2])
                    print(addmsg[1])
                    print(addmsg[2])
                    print(addmsg[3])
                    print(*receiveradress)
                    clientadresschat = (receiveradress[0], int(receiveradress[1]))
                    backadress =(addmsg[1], int(addmsg[2])) #the adress of the client that asked to chat
                    reply = input("Reply:  ")
                    #reply = ('chat {} {} {} {}'.format(receiveradress[0], int(receiveradress[1]), receiver, ''))
                    if reply == '/endchat':
                        print('Conversation closed')
                    else:
                        msgreply = reply.encode()
                        totalsent = 0
                        while totalsent < len(msgreply):
                            sent = self.__s.sendto(msgreply[totalsent:], backadress)
                            totalsent += sent
                if addmsg[0] == 'chat':

                    backadress = addmsg[1], int(addmsg[2])
                    backclient = addmsg[3]
                    print(backclient, ' : ', message)


                    print('ouaip')
                    #self._clientadresschat = (addmsg[1], addmsg[2])

                    print(backadress)

                    #clientadresschat = (receiveradress[0], int(receiveradress[1]))
                    #clientadresschat =(addmsg[1])

                    #inmsg = input("Reply:  ")
                    inmsg = 'lolo'
                    reply = ('chat {} {} {}'.format(self.__myadress[0],self.__myadress[1], self.__clientpseudo, inmsg))
                    if reply == '/endchat':
                        print('Conversation closed')
                    else:
                        msgreply = reply.encode()
                        totalsent = 0
                        while totalsent < len(msgreply):
                            sent = self.__s.sendto(msgreply[totalsent:], backadress)
                            totalsent += sent


            except socket.timeout:
                pass
            except OSError:
                return

    def _startchat(self, receiver):
        if self.__serveradress is not None:
            try:
                param = 'startchat {} {} {}'.format(self.__myadress[0], self.__myadress[1], receiver)
                message = param.encode()
                totalsent = 0

                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')



    def _register(self, pseudo):        #permet aux clients d'ajouter un pseudo et le serveur va enregistrer les donnees du client dans la liste clientlist
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


    def _connected(self):       #permet de recuperer la liste des clients actifs sur le chat
        if self.__serveradress is not None:
            try:            
                param = 'connected {} {}'.format(*self.__myadress)    #envoyer l'adresse IP et le numero de port du client au serveur pour pouvoir renvoyer la liste a la bonne adresse par apres  
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress) #client.socketduclient.sendto
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
